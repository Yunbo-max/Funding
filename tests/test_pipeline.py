"""Offline regressions for the discovery -> shortlist -> application ledger."""
import importlib.util
import json
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

MODULE = Path(__file__).resolve().parents[1] / 'skills/funding-autopilot/scripts/pipeline.py'
spec = importlib.util.spec_from_file_location('pipeline', MODULE)
pipeline = importlib.util.module_from_spec(spec)
sys.modules['pipeline'] = pipeline
spec.loader.exec_module(pipeline)


def candidate(**changes):
    d = {'id': 'opportunity-1', 'funder': 'Funding Example', 'round': '2027',
         'official_url': 'https://example.org/official/call', 'title': 'Research Call',
         'discovered_via': 'official-search',
         'verified_at': '2026-10-16T12:00:00+00:00', 'call_status': 'open',
         'routes': ['independent', 'new_pi'],
         'deadlines': {'funder': '2028-02-18T23:59:00+00:00', 'internal': None},
         'requirements': {'internal_deadline_status': 'confirmed_none'},
         'evidence': [{'field': item, 'url': 'https://example.org/official/call', 'locator': f'§{item}'}
                      for item in ('scope', 'eligibility', 'deadline')]}
    d.update(changes)
    return d


class FakeRules:
    @staticmethod
    def assess(profile, call, route, now):
        status = 'eligible' if profile.get('fields_verified') and route == 'independent' else 'conditional'
        return {'status': status, 'route': route, 'fit_score_not_probability': 65, 'title': call['title'],
                'id': call['id'], 'reasons': ['fixture, not a real grant']}

    @staticmethod
    def call_source_problems(call, now):
        return [] if call.get('verified_at') else ['unverified']

    @staticmethod
    def parse_datetime(value):
        return datetime.fromisoformat(value.replace('Z', '+00:00'))


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.state = {'schema_version': pipeline.VERSION, 'calls': {}}
        self.key = pipeline.record_key(candidate())

    def test_stable_dedup_across_search_sources(self):
        a = candidate()
        b = candidate(funder='  FUNDING   EXAMPLE  ', title='Slightly changed title',
                      official_url='https://example.org/new-location', discovered_via='another portal')
        res = pipeline.ingest(self.state, [a, b], timestamp='2026-10-16T00:00:00+00:00')
        self.assertEqual(len(res['added']), 1)
        self.assertEqual(len(res['existing']), 1)
        self.assertEqual(len(self.state['calls']), 1)
        item = self.state['calls'][self.key]
        self.assertEqual(item['call']['title'], 'Research Call')
        self.assertEqual(len(item['sources']), 2)

    def test_rounds_not_collapsed(self):
        a = candidate()
        b = candidate(round='2028')
        self.assertNotEqual(pipeline.record_key(a), pipeline.record_key(b))

    def test_missing_identity_rejected(self):
        with self.assertRaisesRegex(ValueError, 'round'):
            pipeline.ingest(self.state, [candidate(round=None)])

    def test_https_and_credential_required(self):
        for url in ('http://example.org/', 'javascript:alert(1)', 'https://name:password@example.org'):
            with self.subTest(url=url), self.assertRaisesRegex(ValueError, 'HTTPS'):
                pipeline.ingest(self.state, [candidate(official_url=url)])

    def test_batch_limit_preserves_deferred(self):
        pipeline.ingest(self.state, [candidate(id=f'id-{i}') for i in range(8)])
        first = pipeline.choose_candidates(self.state, 3)
        self.assertEqual(len(first['selected']), 3)
        self.assertEqual(first['deferred'], 5)
        self.assertEqual(len(self.state['calls']), 8)

    def test_rank_needs_cv(self):
        pipeline.ingest(self.state, [candidate()])
        with self.assertRaisesRegex(ValueError, 'CV'):
            pipeline.rank(self.state, {})

    def test_rank_keeps_eligibility_separate(self):
        pipeline.ingest(self.state, [candidate()])
        profile = {'cv_sha256': 'a' * 64, 'fields_verified': True, 'preferred_routes': ['independent', 'new_pi']}
        with patch.object(pipeline, 'load_rules', return_value=FakeRules):
            report = pipeline.rank(self.state, profile)
        self.assertEqual(len(report['evaluations']), 2)
        self.assertEqual([r['status'] for r in report['evaluations']], ['eligible', 'conditional'])
        self.assertEqual(self.state['calls'][self.key]['stage'], 'discovered')

    def test_rank_unverified_profile_not_eligible(self):
        pipeline.ingest(self.state, [candidate()])
        profile = {'cv_sha256': 'a' * 64, 'fields_verified': False}
        with patch.object(pipeline, 'load_rules', return_value=FakeRules):
            report = pipeline.rank(self.state, profile)
        self.assertTrue(all(r['status'] == 'conditional' for r in report['evaluations']))

    def test_invalid_transition(self):
        pipeline.ingest(self.state, [candidate()])
        with self.assertRaisesRegex(ValueError, 'invalid transition'):
            pipeline.advance(self.state, self.key, 'awarded')

    def test_user_can_select_conditional_route_but_not_submit(self):
        pipeline.ingest(self.state, [candidate()])
        self.state['calls'][self.key]['evaluations'] = {'new_pi': {'status': 'conditional'}}
        pipeline.advance(self.state, self.key, 'shortlisted')
        pipeline.advance(self.state, self.key, 'selected', route='new_pi')
        pipeline.advance(self.state, self.key, 'drafting')
        with self.assertRaisesRegex(ValueError, 'eligible'):
            pipeline.advance(self.state, self.key, 'draft_ready')

    def test_outcome_requires_confirmation(self):
        pipeline.ingest(self.state, [candidate()])
        item = self.state['calls'][self.key]
        item['stage'] = 'submitted'
        for kwargs in ({}, {'confirmed': True}, {'evidence_ref': 'portal receipt'}):
            with self.subTest(kwargs=kwargs), self.assertRaisesRegex(ValueError, 'confirmation'):
                pipeline.advance(self.state, self.key, 'awarded', **kwargs)
        res = pipeline.advance(self.state, self.key, 'awarded', confirmed=True, evidence_ref='receipt-123')
        self.assertEqual(res['stage'], 'awarded')
        self.assertEqual(item['history'][-1]['evidence_ref'], 'receipt-123')

    def test_expired_date_blocks_submission_even_if_stored_eligible(self):
        call = candidate(deadlines={'funder': '2025-01-01T00:00:00+00:00', 'internal': None})
        pipeline.ingest(self.state, [call])
        item = self.state['calls'][self.key]
        item.update(stage='drafting', route='independent', evaluations={'independent': {'status': 'eligible'}})
        with patch.object(pipeline, 'load_rules', return_value=FakeRules):
            with self.assertRaisesRegex(ValueError, 'deadline passed'):
                pipeline.advance(self.state, self.key, 'draft_ready')

    def test_unverified_official_call_blocks_ready_draft(self):
        pipeline.ingest(self.state, [candidate(verified_at=None)])
        item = self.state['calls'][self.key]
        item.update(stage='drafting', route='independent', evaluations={'independent': {'status': 'eligible'}})
        with patch.object(pipeline, 'load_rules', return_value=FakeRules):
            with self.assertRaisesRegex(ValueError, 'evidence'):
                pipeline.advance(self.state, self.key, 'draft_ready')

    def test_untrusted_markup_is_escaped_in_html_report(self):
        pipeline.ingest(self.state, [candidate(title='<script>alert(1)</script>', funder='Acme & Co')])
        page = pipeline.report_html(self.state)
        self.assertIn('&lt;script&gt;', page)
        self.assertIn('Acme &amp; Co', page)
        self.assertNotIn('<script>', page)
        self.assertIn('Content-Security-Policy', page)
        self.assertNotIn('<script src=', page)

    def test_private_path_requirement_resolves_traversal(self):
        with tempfile.TemporaryDirectory() as d:
            private = Path(d) / 'private'
            pipeline.require_private(private / 'state.json')
            with self.assertRaisesRegex(ValueError, 'private'):
                pipeline.require_private(private / '..' / 'README.md')

    def test_atomic_state_persistence(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / 'private/state.json'
            pipeline.ingest(self.state, [candidate()])
            pipeline.save_json(path, self.state)
            self.assertEqual(pipeline.load_state(path)['calls'][self.key]['stage'], 'discovered')
            self.assertFalse(path.with_name('state.json.tmp').exists())

    def test_cli_ingest_batch_report_real_commands(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            state = root / 'private/state.json'
            candidates = root / 'candidate.json'
            candidates.write_text(json.dumps([candidate()]), encoding='utf-8')
            with patch.object(sys, 'argv', ['pipeline.py', '--state', str(state), 'ingest', '--input', str(candidates)]):
                self.assertEqual(pipeline.main(), 0)
            with patch.object(sys, 'argv', ['pipeline.py', '--state', str(state), 'batch', '--limit', '1']):
                self.assertEqual(pipeline.main(), 0)
            output = root / 'private/report.html'
            with patch.object(sys, 'argv', ['pipeline.py', '--state', str(state), 'report', '--out', str(output)]):
                self.assertEqual(pipeline.main(), 0)
            self.assertIn('Research Call', output.read_text(encoding='utf-8'))

    def test_public_state_file_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            pub = Path(d) / 'state.json'
            with patch.object(sys, 'argv', ['pipeline.py', '--state', str(pub), 'batch']):
                self.assertEqual(pipeline.main(), 2)


if __name__ == '__main__':
    unittest.main()
