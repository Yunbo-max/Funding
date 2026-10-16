#!/usr/bin/env python3
"""User-facing local Funding Autopilot workflow; an AI host handles live source review and writing."""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

# This file is inside skills/funding-autopilot/scripts/ alongside funding.py and pipeline.py.
import funding
import pipeline

VERSION = '0.3.0'


def moment():
    return datetime.now(timezone.utc)


def root_private(workspace):
    root = Path(workspace).expanduser().resolve() / 'private'
    pipeline.require_private(root / 'profile.json')
    return root


def save(path, obj):
    pipeline.require_private(path)
    pipeline.save_json(path, obj)


def profile_at(root):
    path = root / 'profile.json'
    if not path.exists():
        raise ValueError('Run setup with an uploaded CV before personalized searching or applying')
    profile = funding.read_json(path)
    if not profile.get('cv_sha256'):
        raise ValueError('Profile does not contain evidence of an uploaded CV')
    return profile


def csv_list(value):
    return [x.strip() for x in (value or '').split(',') if x.strip()]


def setup(args, root):
    path = root / 'profile.json'
    if path.exists() and not args.replace:
        raise ValueError('Profile already exists. Use setup-review/setup-confirm, or --replace with a new CV')
    routes = csv_list(args.routes)
    if not routes or not set(routes).issubset({'independent', 'new_pi'}):
        raise ValueError('Routes must be independent and/or new_pi')
    for value in (args.expected_thesis, args.submitted_thesis, args.phd_awarded, args.start_after):
        if value:
            funding.parse_date(value)
    profile = funding.intake(args.cv, path)
    profile['research_terms'] = csv_list(args.topics)
    profile['preferred_routes'] = routes
    profile['residence_country'] = args.residence or None
    profile['expected_phd_submission_on'] = args.expected_thesis or None
    profile['phd_submitted_on'] = args.submitted_thesis or None
    profile['phd_awarded_on'] = args.phd_awarded or None
    profile['preferences'] = {'funding_goal': args.goal or 'research funding or fellowship',
                              'avoid_current_group': bool(args.new_group),
                              'salary_required': bool(args.salary),
                              'target_regions': csv_list(args.regions),
                              'start_after': args.start_after or None}
    profile['fields_verified'] = False
    profile['profile_status'] = 'needs_user_review'
    save(path, profile)
    return {'status': 'setup_pending_review', 'profile_path': str(path), 'cv_hash': profile['cv_sha256'],
            'topics': profile['research_terms'], 'routes': profile['preferred_routes'],
            'next': 'Run setup-review, correct facts, then setup-confirm --confirm-reviewed'}


def setup_review(root):
    profile = profile_at(root)
    fields = ('research_terms', 'preferred_routes', 'residence_country',
              'expected_phd_submission_on', 'phd_submitted_on', 'phd_awarded_on', 'preferences',
              'fields_verified', 'profile_status')
    return {'cv_uploaded': bool(profile.get('cv_sha256')), 'cv_name': profile.get('cv_file'),
            'extracted_characters': profile.get('text_characters'),
            'review_fields': {key: profile.get(key) for key in fields},
            'warning': 'These fields are user-supplied or unreviewed; compare them with your uploaded CV.'}


def setup_confirm(args, root):
    if not args.confirm_reviewed:
        raise ValueError('Explicit --confirm-reviewed required after reviewing CV and profile facts')
    profile = profile_at(root)
    if not profile.get('research_terms'):
        raise ValueError('Add CV-supported research topics before confirming personalized search profile')
    profile['fields_verified'] = True
    profile['profile_status'] = 'user_reviewed'
    profile['confirmed_at'] = moment().isoformat()
    save(root / 'profile.json', profile)
    return {'status': 'profile_confirmed_by_user', 'next': 'search (UKRI RSS) or search --input-file <host-discovered-leads.json>'}


def load_adapter():
    src = Path(__file__).resolve().parent.parent / 'sources' / 'ukri_rss.py'
    spec = importlib.util.spec_from_file_location('funding_ukri_rss', src)
    if spec is None or spec.loader is None:
        raise ValueError('UKRI source adapter not installed')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def search(args, root):
    profile = profile_at(root)
    if args.input_file:
        contents = funding.read_json(args.input_file)
        leads = contents['results'] if isinstance(contents, dict) and isinstance(contents.get('results'), list) else contents
        if not isinstance(leads, list):
            raise ValueError('Imported source must contain a JSON array of funding leads')
        source = 'agent_supplied_source_records'
    else:
        adapter = load_adapter()
        payload = Path(args.feed_file).read_bytes() if args.feed_file else adapter.get_bytes(adapter.FEED)
        # A single bounded RSS fetch avoids repeated external calls.
        all_leads = adapter.parse_feed(payload, limit=min(100, args.limit * 5))['results']
        terms = csv_list(args.query) if args.query else profile.get('research_terms', [])
        leads = [c for c in all_leads if not terms or any(
            term.casefold() in (c.get('title', '') + ' ' + c.get('description', '')).casefold()
            for term in terms)]
        source = 'ukri_official_rss_recent_items_only'
    # Keep intentionally bounded results; imported content must not control filesystem paths.
    selected = leads[:args.limit]
    ledger_path = root / 'ledger.json'
    ledger = pipeline.load_state(ledger_path)
    result = pipeline.ingest(ledger, selected)
    save(ledger_path, ledger)
    return {'source': source, 'search_terms': csv_list(args.query) or profile.get('research_terms', []),
            'found': len(leads), 'ingested': len(selected), 'added': result['added'],
            'already_seen': len(result['existing']),
            'warning': 'Discovery leads are NOT verified/eligible calls. Run batch then verify using official guidance.'}


def verify(args, root):
    profile_at(root)
    state_path = root / 'ledger.json'
    state = pipeline.load_state(state_path)
    old = state['calls'].get(args.key)
    if old is None:
        raise ValueError('Unknown call key; first search or import the funding lead')
    incoming = funding.read_json(args.call_file)
    if str(incoming.get('id', '')).strip().casefold() != str(old['call'].get('id', '')).strip().casefold():
        raise ValueError('Programme identifier differs; do not silently reassign a discovered call')
    if str(incoming.get('funder', '')).strip().casefold() != str(old['call'].get('funder', '')).strip().casefold():
        raise ValueError('Funder identity differs from discovered record')
    origin = urlparse(old['call'].get('official_url', ''))
    target = urlparse(incoming.get('official_url', ''))
    if origin.hostname != target.hostname or target.scheme != 'https':
        raise ValueError('Official host changed; review the new source before merging')
    problems = funding.call_source_problems(incoming, moment())
    if problems:
        raise ValueError('Official call record incomplete or stale: ' + '; '.join(problems))
    if old['stage'] not in {'discovered', 'shortlisted'}:
        raise ValueError('Cannot rewrite a selected/submitted application; create a new version')
    new_key = pipeline.record_key(incoming)
    if new_key != args.key and new_key in state['calls']:
        raise ValueError('A record for that verified round already exists; reconcile duplicates manually')
    entry = state['calls'].pop(args.key)
    entry['key'] = new_key
    entry['call'] = incoming
    entry['evaluations'] = {}
    entry['history'].append({'at': moment().isoformat(), 'event': 'official_call_structured',
                             'previous_key': args.key, 'new_key': new_key,
                             'note': 'Document structure checked; source truth still requires agent/human review'})
    if incoming['official_url'] not in {x['url'] for x in entry['sources']}:
        entry['sources'].append({'url': incoming['official_url'], 'via': 'official_guidance_review',
                                 'observed_at': moment().isoformat()})
    state['calls'][new_key] = entry
    save(state_path, state)
    return {'key': new_key, 'previous_key': args.key, 'status': 'structured_call_recorded',
            'next': 'Rank against the reviewed CV and validate the actual official text; do not assume a grant is awarded.'}


def rank(args, root):
    profile = profile_at(root)
    path = root / 'ledger.json'
    state = pipeline.load_state(path)
    data = pipeline.rank(state, profile)
    save(path, state)
    save(root / 'rankings' / 'latest.json', data)
    return {'checked_at': data['evaluated_at'], 'results': data['evaluations'][:args.limit],
            'remaining': max(0, len(data['evaluations']) - args.limit),
            'warning': 'Eligibility is conditional on independent official rule and institutional review; fit is NOT acceptance probability.'}


def apply(args, root):
    profile = profile_at(root)
    if not profile.get('fields_verified'):
        raise ValueError('Complete setup-review and setup-confirm before application drafting')
    path = root / 'ledger.json'
    state = pipeline.load_state(path)
    record = state['calls'].get(args.key)
    if not record:
        raise ValueError('Call not found; select a ranked funding opportunity')
    # Reassess to catch updated deadlines, changed profile and stale source records.
    result = funding.assess(profile, record['call'], args.route, moment())
    record['evaluations'][args.route] = result
    if result['status'] not in {'eligible', 'conditional'}:
        raise ValueError('Cannot draft a call with status ' + result['status'] + ': ' + '; '.join(result['reasons']))
    if funding.call_source_problems(record['call'], moment()):
        raise ValueError('The full current-round official guidance must be structured before drafting')
    if record.get('route') and record['route'] != args.route:
        raise ValueError('Application already assigned to another route')
    app_dir = root / 'applications' / args.key / args.route
    proposal = app_dir / 'proposal.md'
    if proposal.exists():
        return {'status': 'draft_exists_not_overwritten', 'path': str(proposal),
                'route_eligibility': result['status'], 'next': 'Continue writing and run independent review'}
    # Local deterministic stage transitions. No submission or claim of approval occurs here.
    if record['stage'] == 'discovered':
        pipeline.advance(state, args.key, 'shortlisted')
    if record['stage'] == 'shortlisted':
        pipeline.advance(state, args.key, 'selected', route=args.route)
    if record['stage'] == 'selected':
        pipeline.advance(state, args.key, 'drafting', route=args.route)
    if record['stage'] != 'drafting':
        raise ValueError('Selected call is not in a draftable stage')
    app_dir.mkdir(parents=True, exist_ok=True)
    funding.prepare(record['call'], proposal, moment())
    lines = ['# Compliance and host checklist', '', '**Not submitted. Official office review required.**', '',
             '- [ ] Full current-round call guidance re-read',
             '- [ ] Applicant role and actual PhD milestone confirmed',
             '- [ ] Correct host institution and internal deadline confirmed',
             '- [ ] Eligible salary and budget categories checked',
             '- [ ] Every factual claim traced to a source',
             '- [ ] Word/page/character limits of exact funder form satisfied',
             '- [ ] Applicant and required PI/host explicitly approve before submission', '']
    (app_dir / 'requirements.md').write_text('\n'.join(lines), encoding='utf-8')
    if args.route == 'new_pi':
        (app_dir / 'pi-outreach-draft.md').write_text(
            '# Email draft — DO NOT SEND AUTOMATICALLY\n\n'
            'Subject: Research collaboration and funding opportunity\n\n'
            'Dear Professor [TO CONFIRM],\n\n'
            'I am exploring [EVIDENCE NEEDED: project and call] and would welcome a discussion '
            'about whether our research interests align. The proposed role, salary mechanism, '
            'host commitments and deadlines would all need to be agreed before applying.\n\n'
            'Best regards,\n[TO CONFIRM]\n', encoding='utf-8')
    save(app_dir / 'application.json', {'call_key': args.key, 'call_id': record['call']['id'],
        'round': record['call']['round'], 'route': args.route,
        'eligible_status_at_drafting': result['status'], 'cv_hash': profile['cv_sha256'],
        'status': 'drafting_not_submitted', 'source_url': record['call']['official_url'],
        'created_at': moment().isoformat(), 'reviewed_by_user': False})
    save(path, state)
    return {'status': 'concept_only' if result['status'] == 'conditional' else 'draft_scaffold_created',
            'proposal': str(proposal), 'requirements': str(app_dir / 'requirements.md'),
            'pi_outreach': str(app_dir / 'pi-outreach-draft.md') if args.route == 'new_pi' else None,
            'next': 'Use the AI host to write source-supported narrative, then reviewer + form/PDF audit. Never auto-submit.'}



def ready(args, root):
    if not args.confirm_reviewed:
        raise ValueError('The applicant must explicitly confirm the final draft review')
    profile = profile_at(root)
    if not profile.get('fields_verified'):
        raise ValueError('The CV profile must first be reviewed and confirmed')
    path = root / 'ledger.json'
    state = pipeline.load_state(path)
    record = state['calls'].get(args.key)
    if not record or record.get('stage') != 'drafting':
        raise ValueError('The selected call must be in drafting stage')
    route = record.get('route')
    assessment = funding.assess(profile, record['call'], route, moment())
    record['evaluations'][route] = assessment
    if assessment['status'] != 'eligible':
        raise ValueError('Ready requires verified eligible route, not ' + assessment['status'])
    proposal_file = Path(args.proposal_json).expanduser().resolve()
    pipeline.require_private(proposal_file)
    packet = funding.read_json(proposal_file)
    audit = funding.audit(packet, record['call'], moment())
    if audit['status'] != 'structured_draft_passed_human_review_required':
        raise ValueError('Proposal audit failed: ' + '; '.join(audit['issues']))
    approvals = packet.get('approval') or {}
    req = record['call'].get('requirements') or {}
    if approvals.get('applicant') is not True:
        raise ValueError('Applicant approval still missing')
    if req.get('requires_host') and approvals.get('host') is not True:
        raise ValueError('Required host approval still missing')
    if (route == 'new_pi' or req.get('requires_new_pi')) and approvals.get('pi') is not True:
        raise ValueError('New PI approval still missing')
    result = pipeline.advance(state, args.key, 'draft_ready')
    save(path, state)
    return {'status': 'draft_ready_for_manual_submission', 'transition': result,
            'note': 'No automatic submission; official host/grants office must independently check the packet.'}

def status(root):
    profile = profile_at(root)
    ledger = pipeline.load_state(root / 'ledger.json')
    return {'profile_reviewed': profile.get('fields_verified', False),
            'total_calls': len(ledger['calls']),
            'calls': [{'key': v['key'], 'title': v['call'].get('title'), 'round': v['call'].get('round'),
                       'stage': v['stage'], 'route': v.get('route'),
                       'eligibility': {k: x['status'] for k, x in v.get('evaluations', {}).items()}}
                      for v in ledger['calls'].values()]}


def outcome(args, root):
    profile_at(root)
    path = root / 'ledger.json'
    state = pipeline.load_state(path)
    result = pipeline.advance(state, args.key, args.to, confirmed=args.confirmed,
                              evidence_ref=args.receipt, note=args.note)
    save(path, state)
    return {'status': 'recorded', 'transition': result,
            'warning': 'Receipts and user confirmation are required for submitted/award/rejection/withdrawal.'}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--workspace', default='.', help='Local workspace; all personal data go into ignored private/')
    sub = p.add_subparsers(dest='command', required=True)
    s = sub.add_parser('setup', help='Read a user-supplied CV and create an unreviewed profile')
    s.add_argument('--cv', required=True)
    s.add_argument('--topics', required=True, help='Comma-separated CV-supported research topics')
    s.add_argument('--routes', default='independent,new_pi')
    s.add_argument('--goal')
    s.add_argument('--regions', default='')
    s.add_argument('--residence')
    s.add_argument('--new-group', action='store_true')
    s.add_argument('--salary', action='store_true')
    s.add_argument('--start-after')
    s.add_argument('--expected-thesis')
    s.add_argument('--submitted-thesis')
    s.add_argument('--phd-awarded')
    s.add_argument('--replace', action='store_true')
    sub.add_parser('setup-review', help='Review profile facts before confirming')
    c = sub.add_parser('setup-confirm')
    c.add_argument('--confirm-reviewed', action='store_true')
    s = sub.add_parser('search', help='Search UKRI RSS or import host-discovered funding leads')
    s.add_argument('--input-file', type=Path)
    s.add_argument('--feed-file', type=Path, help='Offline UKRI XML fixture')
    s.add_argument('--query', help='Optional comma-separated text filters; default setup topics')
    s.add_argument('--limit', type=int, default=20)
    v = sub.add_parser('verify', help='Promote a discovery lead to a source-checked specific call round')
    v.add_argument('--key', required=True)
    v.add_argument('--call-file', type=Path, required=True)
    r = sub.add_parser('rank')
    r.add_argument('--limit', type=int, default=10)
    a = sub.add_parser('apply')
    a.add_argument('--key', required=True)
    a.add_argument('--route', choices=['independent', 'new_pi'], required=True)
    r = sub.add_parser('ready', help='Audit completed proposal JSON before recording draft_ready')
    r.add_argument('--key', required=True)
    r.add_argument('--proposal-json', required=True)
    r.add_argument('--confirm-reviewed', action='store_true')
    sub.add_parser('status')
    o = sub.add_parser('outcome')
    o.add_argument('--key', required=True)
    o.add_argument('--to', required=True, choices=sorted(pipeline.STAGES.keys()))
    o.add_argument('--confirmed', action='store_true')
    o.add_argument('--receipt')
    o.add_argument('--note')
    args = p.parse_args(argv)
    try:
        root = root_private(args.workspace)
        if args.command == 'setup':
            result = setup(args, root)
        elif args.command == 'setup-review':
            result = setup_review(root)
        elif args.command == 'setup-confirm':
            result = setup_confirm(args, root)
        elif args.command == 'search':
            if args.limit < 1 or args.limit > 100:
                raise ValueError('--limit must be 1..100')
            result = search(args, root)
        elif args.command == 'verify':
            result = verify(args, root)
        elif args.command == 'rank':
            if args.limit < 1 or args.limit > 200:
                raise ValueError('--limit must be 1..200')
            result = rank(args, root)
        elif args.command == 'apply':
            result = apply(args, root)
        elif args.command == 'ready':
            result = ready(args, root)
        elif args.command == 'outcome':
            result = outcome(args, root)
        else:
            result = status(root)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
        print(json.dumps({'error': str(exc), 'code': 'WORKSPACE_ERROR'}), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
