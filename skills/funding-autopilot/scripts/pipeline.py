#!/usr/bin/env python3
"""Local, private funding opportunity ledger. No HTTP, model calls or submissions."""
from __future__ import annotations

import argparse
import hashlib
import html
import importlib.util
import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

VERSION = '0.4.0'
STAGES = {
    'discovered': {'shortlisted', 'archived'},
    'shortlisted': {'selected', 'archived'},
    'selected': {'preparing', 'archived'},
    'preparing': {'prepared', 'archived'},
    'prepared': {'drafting', 'preparing', 'archived'},
    'drafting': {'draft_ready', 'archived'},
    'draft_ready': {'submitted', 'drafting', 'archived'},
    'submitted': {'under_review', 'awarded', 'rejected', 'withdrawn'},
    'under_review': {'awarded', 'rejected', 'withdrawn'},
    'awarded': set(), 'rejected': set(), 'withdrawn': set(), 'archived': {'discovered'},
}
OUTCOME_STAGES = {'submitted', 'awarded', 'rejected', 'withdrawn'}
PRIVATE_PARTS = {'private', 'applications', 'output', 'outputs'}


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def read_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def atomic_write(path: Path, data: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + '.tmp')
    temporary.write_text(data, encoding='utf-8')
    temporary.replace(path)


def save_json(path: Path, data: dict):
    atomic_write(path, json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True) + '\n')


def require_private(path: Path):
    # Fail closed even on a traversal or symlink through an apparent private/ path.
    # All state, reports and proposals are required to live under private/.
    if 'private' not in path.resolve(strict=False).parts:
        raise ValueError('sensitive outputs require a resolved private/ directory')


def safe_url(value: str) -> str:
    parsed = urlparse(str(value))
    if parsed.scheme != 'https' or not parsed.netloc or parsed.username or parsed.password:
        raise ValueError('an HTTPS URL without embedded credentials is required')
    return parsed.geturl()


def record_key(call: dict) -> str:
    # Stable across aggregators, whitespace and title changes. A distinct round
    # remains a distinct opportunity even when the programme title repeats.
    funder = str(call.get('funder') or '').strip().casefold()
    identifier = str(call.get('id') or '').strip().casefold()
    round_id = str(call.get('round') or '').strip().casefold()
    if not all([funder, identifier, round_id]):
        raise ValueError('call requires funder, id and round for deduplication')
    normalized = '\x1f'.join(' '.join(p.split()) for p in (funder, identifier, round_id))
    return 'call-' + hashlib.sha256(normalized.encode('utf-8')).hexdigest()[:20]


def load_state(path: Path) -> dict:
    if not path.exists():
        return {'schema_version': VERSION, 'calls': {}, 'created_at': now_utc()}
    state = read_json(path)
    if not isinstance(state, dict) or not isinstance(state.get('calls'), dict):
        raise ValueError('ledger must contain a calls object')
    return state


def ingest(state: dict, candidates: list, timestamp: str | None = None) -> dict:
    """Save discovered calls without pretending input data has been verified."""
    timestamp = timestamp or now_utc()
    if not isinstance(candidates, list):
        raise ValueError('input must be a JSON array of candidate calls')
    new, repeated = [], []
    for obj in candidates:
        if not isinstance(obj, dict):
            raise ValueError('candidate must be a JSON object')
        official_url = safe_url(obj.get('official_url') or '')
        key = record_key(obj)
        source = {'url': official_url, 'observed_at': timestamp,
                  'via': str(obj.get('discovered_via') or 'agent/web').strip()[:100]}
        if key in state['calls']:
            old = state['calls'][key]
            # Never silently replace existing official-call text/verified values.
            if source['url'] not in {s['url'] for s in old['sources']}:
                old['sources'].append(source)
            old['last_seen'] = timestamp
            repeated.append(key)
        else:
            state['calls'][key] = {
                'key': key, 'call': {k: v for k, v in obj.items() if k != 'discovered_via'},
                'sources': [source], 'first_seen': timestamp, 'last_seen': timestamp,
                'stage': 'discovered', 'route': None, 'evaluations': {},
                'history': [{'at': timestamp, 'event': 'discovered', 'source': official_url}],
            }
            new.append(key)
    return {'added': new, 'existing': repeated, 'total': len(state['calls'])}


def choose_candidates(state: dict, limit: int = 10, include_archived: bool = False):
    if limit < 1 or limit > 200:
        raise ValueError('limit must be from 1 to 200')
    eligible = [r for r in state['calls'].values()
                if r['stage'] == 'discovered' or (include_archived and r['stage'] == 'archived')]
    eligible.sort(key=lambda r: (r['first_seen'], r['key']))
    batch = eligible[:limit]
    return {'selected': [{'key': r['key'], 'title': r['call'].get('title'),
                          'official_url': r['call'].get('official_url'),
                          'stage': r['stage']} for r in batch],
            'deferred': len(eligible) - len(batch), 'eligible_for_batch': len(eligible)}


def load_rules():
    # Sibling funding.py owns conservative primary-source/degree/host gating.
    module_path = Path(__file__).with_name('funding.py')
    spec = importlib.util.spec_from_file_location('funding_gate', module_path)
    if spec is None or spec.loader is None:
        raise ValueError('funding.py eligibility rules are not available')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def rank(state: dict, profile: dict, as_of: datetime | None = None):
    if not profile.get('cv_sha256'):
        raise ValueError('the user must upload a CV before ranking')
    if not profile.get('fields_verified'):
        # Allow gap triage, but never eligible status. Enforced by funding.assess.
        pass
    rules = load_rules()
    as_of = as_of or datetime.now(timezone.utc)
    rows = []
    for record in state['calls'].values():
        if record['stage'] in {'awarded', 'rejected', 'withdrawn'}:
            continue
        for route in profile.get('preferred_routes') or ['independent', 'new_pi']:
            result = rules.assess(profile, record['call'], route, as_of)
            record['evaluations'][route] = result
            rows.append({'key': record['key'], **result})
    priority = {'eligible': 0, 'conditional': 1, 'unverified': 2, 'ineligible': 3, 'expired': 4}
    rows.sort(key=lambda r: (priority.get(r['status'], 10),
                             -(r['fit_score_not_probability'] or 0), r['key'], r['route']))
    return {'evaluated_at': as_of.isoformat(), 'evaluations': rows,
            'note': 'An assessment requires real official-source verification by the host; these are encoded rule checks, not acceptance probabilities.'}


def advance(state: dict, key: str, to_stage: str, route: str | None = None,
            confirmed: bool = False, evidence_ref: str | None = None,
            note: str | None = None, timestamp: str | None = None):
    record = state['calls'].get(key)
    if record is None:
        raise ValueError('unknown call key')
    old = record['stage']
    if to_stage not in STAGES.get(old, set()):
        raise ValueError(f'invalid transition: {old} -> {to_stage}')
    active_route = route or record.get('route')
    if to_stage in {'selected', 'preparing', 'prepared', 'drafting', 'draft_ready', 'submitted'}:
        if active_route not in {'independent', 'new_pi'}:
            raise ValueError('select an independent or new_pi route first')
    if to_stage == 'selected':
        if (record['evaluations'].get(active_route) or {}).get('status') not in {'eligible', 'conditional'}:
            raise ValueError('selected route must have eligible or conditional evaluation')
    if to_stage in {'draft_ready', 'submitted'}:
        if (record['evaluations'].get(active_route) or {}).get('status') != 'eligible':
            raise ValueError('draft ready/submission requires an eligible assessed route')
        rules = load_rules()
        call = record['call']
        if rules.call_source_problems(call, datetime.now(timezone.utc)):
            raise ValueError('official-call evidence is missing/stale; recheck before preparing or submitting')
        if call.get('call_status') == 'closed':
            raise ValueError('official call has been marked closed')
        for label, when in (call.get('deadlines') or {}).items():
            if label in {'funder', 'internal'} and when and rules.parse_datetime(when) < datetime.now(timezone.utc):
                raise ValueError(f'{label} deadline passed; recheck route before continuing')
    if to_stage == 'prepared' and (not confirmed or not (evidence_ref and evidence_ref.strip())):
        raise ValueError('preparation requires applicant-reviewed plan and evidence reference')
    if to_stage in OUTCOME_STAGES:
        if not confirmed or not (evidence_ref and evidence_ref.strip()):
            raise ValueError('outcome/submission requires explicit confirmation and receipt reference')
    if route and record.get('route') and route != record['route']:
        raise ValueError('cannot silently switch an already selected application route')
    record['stage'] = to_stage
    if active_route:
        record['route'] = active_route
    record['history'].append({'at': timestamp or now_utc(), 'event': to_stage,
                              'previous': old, 'route': active_route,
                              'confirmation': bool(confirmed), 'evidence_ref': evidence_ref,
                              'note': note})
    return {'key': key, 'previous': old, 'stage': to_stage, 'route': record.get('route')}


def report_html(state: dict):
    records = list(state['calls'].values())
    counts = Counter(record.get('stage') for record in records)
    def esc(v):
        return html.escape(str(v if v is not None else '—'), quote=True)
    rows = []
    for r in sorted(records, key=lambda x: (x.get('first_seen', ''), x['key']), reverse=True):
        c = r['call']
        try:
            href = safe_url(c.get('official_url') or '')
            link = '<a href="' + esc(href) + '" rel="noopener noreferrer">official call</a>'
        except ValueError:
            link = '—'
        d = c.get('deadlines') or {}
        statuses = ', '.join(f'{route}: {e.get("status", "unverified")}'
                             for route, e in sorted(r.get('evaluations', {}).items())) or 'not checked'
        rows.append('<tr><td>' + esc(c.get('funder')) + '</td><td>' + esc(c.get('title')) +
                    '</td><td>' + esc(c.get('round')) + '</td><td>' + esc(r.get('stage')) +
                    '</td><td>' + esc(statuses) + '</td><td>' +
                    esc(d.get('internal') or d.get('funder') or 'unknown') + '</td><td>' + link + '</td></tr>')
    cards = ''.join('<div class="stat"><b>' + esc(n) + '</b><span>' + esc(status) + '</span></div>'
                    for status, n in sorted(counts.items()))
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<meta http-equiv="Content-Security-Policy" content="default-src &apos;none&apos;; style-src &apos;unsafe-inline&apos;;">'
            '<title>Funding pipeline</title><style>body{font-family:system-ui,sans-serif;max-width:1250px;margin:3rem auto;padding:0 1rem;color:#171717}'
            '.stats{display:flex;flex-wrap:wrap;gap:12px}.stat{border:1px solid #ddd;border-radius:12px;padding:14px 20px;display:grid;gap:4px}'
            '.stat b{font-size:2rem}.stat span{color:#666}table{width:100%;border-collapse:collapse;margin-top:20px}'
            'th,td{padding:11px;text-align:left;border-bottom:1px solid #ddd}th{background:#f5f5f5}tr:nth-child(even){background:#fafafa}'
            'a{color:#174c8b} .scroll{overflow-x:auto} .foot{color:#666;font-size:.85rem;margin-top:24px}</style></head><body>'
            '<h1>Funding pipeline</h1><p>Locally generated, no external assets; eligibility is not a funding decision.</p>'
            '<div class="stats">' + cards + '</div><div class="scroll"><table><thead><tr>'
            '<th>Funder</th><th>Call</th><th>Round</th><th>Stage</th><th>Eligibility by route</th><th>Next known deadline</th><th>Source</th>'
            '</tr></thead><tbody>' + ''.join(rows) + '</tbody></table></div>'
            '<p class="foot">Source records are untrusted data; status changes require confirmation. '
            'Do not publish this report unless its contents are cleared.</p></body></html>')


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--state', required=True, help='private ledger JSON path')
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('ingest')
    p.add_argument('--input', required=True, help='agent-collected candidate calls JSON array')
    p = sub.add_parser('batch')
    p.add_argument('--limit', type=int, default=10)
    p.add_argument('--include-archived', action='store_true')
    p = sub.add_parser('rank')
    p.add_argument('--profile', required=True)
    p = sub.add_parser('advance')
    p.add_argument('--key', required=True)
    p.add_argument('--to', required=True, choices=STAGES.keys())
    p.add_argument('--route', choices=['independent', 'new_pi'])
    p.add_argument('--confirm', action='store_true')
    p.add_argument('--evidence-ref')
    p.add_argument('--note')
    p = sub.add_parser('report')
    p.add_argument('--out', required=True)
    args = parser.parse_args(argv)
    try:
        path = Path(args.state)
        require_private(path)
        state = load_state(path)
        if args.command == 'ingest':
            result = ingest(state, read_json(Path(args.input)))
            save_json(path, state)
        elif args.command == 'batch':
            result = choose_candidates(state, args.limit, args.include_archived)
        elif args.command == 'rank':
            result = rank(state, read_json(Path(args.profile)))
            save_json(path, state)
        elif args.command == 'advance':
            result = advance(state, args.key, args.to, args.route, args.confirm,
                             args.evidence_ref, args.note)
            save_json(path, state)
        else:
            output = Path(args.out)
            require_private(output)
            atomic_write(output, report_html(state))
            result = {'report': str(output), 'call_count': len(state['calls']), 'private_data': True}
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
        print(json.dumps({'error': str(exc), 'code': 'PIPELINE_ERROR'}), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
