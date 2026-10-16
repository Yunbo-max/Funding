import importlib.util
import json
import tempfile
import unittest
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1] / 'skills/funding-autopilot/scripts/funding.py'
spec = importlib.util.spec_from_file_location('funding', MODULE)
funding = importlib.util.module_from_spec(spec)
spec.loader.exec_module(funding)

NOW = datetime(2026, 10, 16, 14, 0, tzinfo=timezone.utc)


def example_profile():
    return {'cv_sha256': 'a' * 64, 'fields_verified': True,
            'research_terms': ['agent verification', 'machine learning'],
            'residence_country': 'GB', 'phd_submitted_on': '2026-09-01',
            'phd_awarded_on': None, 'host_confirmed': False,
            'new_pi_confirmed': False, 'preferred_routes': ['independent', 'new_pi']}


def example_call():
    return {'id': 'fixture-2027', 'round': '2027', 'title': 'Fictional fellowship, not open',
            'funder': 'Fixture Foundation', 'official_url': 'https://example.org/test',
            'verified_at': NOW.isoformat(), 'call_status': 'open',
            'routes': ['independent', 'new_pi'],
            'scope_terms': ['agent verification'], 'salary_support': 'yes',
            'requirements': {'requires_phd_submission_by': '2027-02-18',
                             'requires_phd_award_by': None, 'requires_host': False,
                             'requires_new_pi': False,
                             'eligible_residence_countries': ['GB'],
                             'internal_deadline_status': 'confirmed_none',
                             'manual_gate_status': 'pass'},
            'deadlines': {'funder': '2027-02-18T23:59:00+00:00', 'internal': None},
            'evidence': [{'field': f, 'url': 'https://example.org/test', 'locator': f'Section: {f}'}
                         for f in ('scope', 'eligibility', 'deadline')],
            'sections': [{'id': 'summary', 'max_words': 5, 'required': True},
                         {'id': 'plan', 'max_words': 100, 'required': True}],
            'required_documents': ['cv', 'host_letter']}


class FundingGateTests(unittest.TestCase):
    def test_cv_is_mandatory(self):
        with self.assertRaisesRegex(ValueError, 'CV'):
            funding.shortlist({}, [example_call()], NOW)

    def test_independent_eligible_when_encoded_gates_pass(self):
        row = funding.assess(example_profile(), example_call(), 'independent', NOW)
        self.assertEqual(row['status'], 'eligible')
        self.assertGreater(row['fit_score_not_probability'], 0)

    def test_new_pi_requires_real_confirmation(self):
        row = funding.assess(example_profile(), example_call(), 'new_pi', NOW)
        self.assertEqual(row['status'], 'conditional')
        self.assertTrue(any('new PI' in reason for reason in row['reasons']))

    def test_expectation_does_not_count_as_submitted(self):
        profile = example_profile()
        profile['phd_submitted_on'] = None
        profile['expected_phd_submission_on'] = '2026-11-15'
        row = funding.assess(profile, example_call(), 'independent', NOW)
        self.assertEqual(row['status'], 'conditional')

    def test_future_milestone_not_counted_as_actual(self):
        profile = example_profile()
        profile['phd_submitted_on'] = '2026-11-15'
        self.assertEqual(funding.assess(profile, example_call(), 'independent', NOW)['status'], 'conditional')

    def test_awarded_phd_is_separate(self):
        call = example_call()
        call['requirements']['requires_phd_award_by'] = '2027-01-01'
        self.assertEqual(funding.assess(example_profile(), call, 'independent', NOW)['status'], 'conditional')

    def test_unverified_source_has_no_eligible_status(self):
        call = example_call()
        call['verified_at'] = '2026-01-01T00:00:00+00:00'
        self.assertEqual(funding.assess(example_profile(), call, 'independent', NOW)['status'], 'unverified')

    def test_missing_evidence_blocks(self):
        call = example_call()
        call['evidence'] = []
        self.assertEqual(funding.assess(example_profile(), call, 'independent', NOW)['status'], 'unverified')

    def test_internal_deadline_can_block_early(self):
        call = example_call()
        call['requirements']['internal_deadline_status'] = 'verified'
        call['deadlines']['internal'] = '2026-10-15T17:00:00+01:00'
        self.assertEqual(funding.assess(example_profile(), call, 'independent', NOW)['status'], 'expired')

    def test_residence_mismatch_blocks(self):
        profile = example_profile()
        profile['residence_country'] = 'FR'
        self.assertEqual(funding.assess(profile, example_call(), 'independent', NOW)['status'], 'ineligible')

    def test_unreviewed_cv_does_not_pass(self):
        profile = example_profile()
        profile['fields_verified'] = False
        self.assertEqual(funding.assess(profile, example_call(), 'independent', NOW)['status'], 'conditional')

    def test_requires_timezone(self):
        with self.assertRaisesRegex(ValueError, 'timezone'):
            funding.parse_datetime('2027-02-18T23:59:00')

    def test_shortlist_keeps_conditional_separate(self):
        data = funding.shortlist(example_profile(), [example_call()], NOW)
        self.assertEqual([r['status'] for r in data['results']], ['eligible', 'conditional'])


class WritingTests(unittest.TestCase):
    def valid_proposal(self):
        return {'call_id': 'fixture-2027', 'sections': {'summary': 'Test plan.', 'plan': 'We test the proposed approach.'},
                'documents': ['cv', 'host_letter'],
                'evidence_index': [{'id': 'cv:p2', 'kind': 'cv', 'locator': 'CV page 2', 'verified': True}],
                'claims': [{'id': 'c1', 'text': 'Applicant led published work.', 'evidence_ids': ['cv:p2']}],
                'approval': {'applicant': False, 'pi': False, 'host': False}}

    def test_valid_structured_draft_still_needs_human_review(self):
        row = funding.audit(self.valid_proposal(), example_call(), NOW)
        self.assertEqual(row['status'], 'structured_draft_passed_human_review_required')
        self.assertTrue(row['human_review_required'])

    def test_word_limit_and_placeholders(self):
        proposal = self.valid_proposal()
        proposal['sections']['summary'] = 'one two three four five six [TO CONFIRM]'
        row = funding.audit(proposal, example_call(), NOW)
        self.assertEqual(row['status'], 'needs_repair')
        self.assertTrue(any('word limit' in issue for issue in row['issues']))
        self.assertTrue(any('placeholder' in issue for issue in row['issues']))

    def test_missing_attachment_and_evidence(self):
        proposal = self.valid_proposal()
        proposal['documents'] = ['cv']
        proposal['evidence_index'][0]['verified'] = False
        row = funding.audit(proposal, example_call(), NOW)
        self.assertTrue(any('documents' in issue for issue in row['issues']))
        self.assertTrue(any('unverified evidence' in issue for issue in row['issues']))

    def test_prepare_creates_call_specific_blank_draft(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / 'private/proposal.md'
            result = funding.prepare(example_call(), out, NOW)
            text = out.read_text(encoding='utf-8')
            self.assertEqual(result['section_count'], 2)
            self.assertIn('## summary', text)
            self.assertIn('## plan', text)
            self.assertIn('host_letter', text)
            self.assertIn('HUMAN/PI/HOST REVIEW', text)

    def test_prepare_rejects_unverified_call(self):
        with tempfile.TemporaryDirectory() as td:
            call = example_call()
            call['verified_at'] = None
            with self.assertRaisesRegex(ValueError, 'source verification'):
                funding.prepare(call, Path(td) / 'private/proposal.md', NOW)

    def test_intake_rejects_short_cv(self):
        with tempfile.TemporaryDirectory() as td:
            file = Path(td) / 'cv.txt'
            file.write_text('short', encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'Insufficient'):
                funding.intake(file, Path(td) / 'private/profile.json')

    def test_intake_outputs_unverified_local_profile(self):
        with tempfile.TemporaryDirectory() as td:
            cv = Path(td) / 'cv.txt'
            cv.write_text('Education: Test University. Research experience in reliable ' * 4, encoding='utf-8')
            out = Path(td) / 'private/profile.json'
            data = funding.intake(cv, out)
            self.assertTrue(out.exists())
            self.assertFalse(data['fields_verified'])
            self.assertEqual(len(data['cv_sha256']), 64)
            self.assertTrue(Path(data['extracted_text_file']).exists())


if __name__ == '__main__':
    unittest.main()
