"""End-to-end local workspace tests with fictional calls; no real CV or grant submission."""
import importlib.util
import json
import tempfile
import unittest
from argparse import Namespace
from datetime import datetime, timedelta, timezone
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/funding-autopilot/scripts'
import sys
sys.path.insert(0, str(SCRIPT))
import workspace as app
import pipeline


def params(**kw):
    return Namespace(**kw)


def call(slug='demo-fellowship'):
    date = (datetime.now(timezone.utc)+timedelta(days=120)).isoformat()
    return dict(id=slug, funder='Fictional Foundation', round='2027',
                title='Fictional Research Fellowship (NOT REAL)',
                official_url='https://example.org/grants/demo-fellowship',
                verified_at=datetime.now(timezone.utc).isoformat(), call_status='open',
                routes=['independent','new_pi'], salary_support='yes', scope_terms=['AI agents'],
                deadlines={'funder': date, 'internal': None},
                requirements={'requires_host':False,'requires_new_pi':False,
                              'internal_deadline_status':'confirmed_none','manual_gate_status':'pass'},
                evidence=[{'field':k,'url':'https://example.org/grants/demo-fellowship','locator':k}
                          for k in ('scope','eligibility','deadline')],
                sections=[{'id':'summary','max_words':60,'required':True},
                          {'id':'plan','max_words':250,'required':True}],
                required_documents=['cv'])


class WorkspaceTests(unittest.TestCase):
    def setUp(self):
        self.t=tempfile.TemporaryDirectory()
        self.addCleanup(self.t.cleanup)
        self.base=Path(self.t.name)
        self.private=self.base/'private'
        self.cv=self.base/'my_cv.txt'
        self.cv.write_text('PhD researcher studying trustworthy multi-agent systems, verification, and autonomous language models. '\
                           'Published research and academic software contributions. '*4, encoding='utf-8')

    def setup_profile(self):
        return app.setup(params(cv=str(self.cv), topics='AI agents,verification',routes='independent,new_pi',
                                goal='independent fellowship',residence='GB',regions='UK,EU',
                                new_group=True,salary=True,start_after=None,expected_thesis='2026-11-25',
                                submitted_thesis=None,phd_awarded=None,replace=False),self.private)

    def seed(self):
        self.setup_profile()
        app.setup_confirm(params(confirm_reviewed=True), self.private)
        leads=self.base/'leads.json'
        leads.write_text(json.dumps([dict(id='demo-fellowship',funder='Fictional Foundation',round='unverified',
                                          title='Fictional Research Fellowship',
                                          official_url='https://example.org/grants/demo-fellowship')]))
        found=app.search(params(input_file=leads,feed_file=None,limit=20,query=None),self.private)
        key=found['added'][0]
        full=self.base/'official-call.json'
        full.write_text(json.dumps(call()))
        update=app.verify(params(key=key,call_file=full),self.private)
        return update['key']

    def test_setup_requires_actual_cv_and_is_unreviewed(self):
        result=self.setup_profile()
        self.assertEqual(result['status'],'setup_pending_review')
        profile=app.profile_at(self.private)
        self.assertFalse(profile['fields_verified'])
        self.assertEqual(profile['expected_phd_submission_on'],'2026-11-25')
        self.assertIsNone(profile['phd_submitted_on'])
        self.assertTrue(profile['preferences']['avoid_current_group'])
        self.assertTrue(profile['preferences']['salary_required'])

    def test_profile_never_overwritten_silently(self):
        self.setup_profile()
        with self.assertRaisesRegex(ValueError,'already exists'):
            self.setup_profile()

    def test_setup_confirm_explicit(self):
        self.setup_profile()
        with self.assertRaisesRegex(ValueError,'confirm-reviewed'):
            app.setup_confirm(params(confirm_reviewed=False),self.private)
        self.assertEqual(app.setup_confirm(params(confirm_reviewed=True),self.private)['status'],
                         'profile_confirmed_by_user')

    def test_setup_update_preserves_cv_and_reopens_review(self):
        self.setup_profile()
        app.setup_confirm(params(confirm_reviewed=True), self.private)
        cv_hash = app.profile_at(self.private)['cv_sha256']
        result = app.setup_update(params(topics='mechanistic AI,verification',routes=None,
            goal='new research institute',regions='UK,US',residence=None,
            expected_thesis=None,submitted_thesis=None,phd_awarded=None,
            salary='no',new_group='yes',start_after=None), self.private)
        profile = app.profile_at(self.private)
        self.assertEqual(result['status'], 'updated_pending_review')
        self.assertEqual(profile['cv_sha256'], cv_hash)
        self.assertFalse(profile['fields_verified'])
        self.assertFalse(profile['preferences']['salary_required'])
        self.assertTrue(profile['preferences']['avoid_current_group'])

    def test_future_actual_phd_date_rejected_before_cv_write(self):
        with self.assertRaisesRegex(ValueError, 'in the future'):
            app.setup(params(cv=str(self.cv), topics='AI agents',routes='independent',
                    goal=None,residence=None,regions='',new_group=False,salary=False,
                    start_after=None,expected_thesis=None,submitted_thesis='2999-01-01',
                    phd_awarded=None,replace=False), self.private)
        self.assertFalse((self.private/'profile.json').exists())

    def test_setup_cv_facts_are_private_and_require_review(self):
        self.setup_profile()
        app.setup_confirm(params(confirm_reviewed=True), self.private)
        file = self.private/'facts.json'
        file.write_text(json.dumps({'cv_sha256': app.profile_at(self.private)['cv_sha256'],
              'facts':[{'id':'paper-1','category':'publication','claim':'Example research contribution',
                        'locator':'CV page 2','source_kind':'cv'}]}))
        result=app.setup_facts(params(input_file=str(file)),self.private)
        self.assertEqual(result['added'],1)
        self.assertEqual(app.setup_facts(params(input_file=str(file)),self.private)['added'],0)
        self.assertFalse(app.profile_at(self.private)['fields_verified'])
        self.assertEqual(len(app.setup_review(self.private)['cv_evidence_facts']),1)
        app.setup_confirm(params(confirm_reviewed=True), self.private)
        self.assertEqual(app.profile_at(self.private)['fact_evidence'][0]['review_state'], 'user_confirmed')

    def test_setup_facts_rejects_public_file_and_conflicting_claim(self):
        self.setup_profile()
        bad=self.base/'outside.json'
        bad.write_text(json.dumps([{'id':'p','category':'publication','claim':'Verified paper',
                                    'locator':'CV p2','source_kind':'cv'}]))
        with self.assertRaisesRegex(ValueError,'private'):
            app.setup_facts(params(input_file=str(bad)),self.private)
        safe=self.private/'in.json'
        safe.write_text(bad.read_text())
        app.setup_facts(params(input_file=str(safe)),self.private)
        safe.write_text(json.dumps([{'id':'p','category':'publication','claim':'Contradictory paper',
                                    'locator':'CV p2','source_kind':'cv'}]))
        with self.assertRaisesRegex(ValueError,'Conflicting'):
            app.setup_facts(params(input_file=str(safe)),self.private)

    def test_search_without_cv_rejected(self):
        with self.assertRaisesRegex(ValueError,'setup'):
            app.search(params(input_file=self.base/'missing.json',feed_file=None,limit=20,query=None),self.private)

    def test_lead_is_migrated_to_exact_round_after_official_check(self):
        key=self.seed()
        self.assertEqual(len(pipeline.load_state(self.private/'ledger.json')['calls']),1)
        self.assertEqual(pipeline.load_state(self.private/'ledger.json')['calls'][key]['call']['round'],'2027')

    def test_repeat_discovery_does_not_recreate_unknown_round(self):
        key = self.seed()
        leads = self.base/'same-lead.json'
        leads.write_text(json.dumps([dict(id='demo-fellowship',funder='Fictional Foundation',
             round='unverified',title='Same feed title',
             official_url='https://example.org/grants/demo-fellowship')]))
        result = app.search(params(input_file=leads,feed_file=None,limit=20,query=None),self.private)
        self.assertEqual(result['added'], [])
        self.assertEqual(result['needs_round_recheck'], [key])
        self.assertEqual(len(pipeline.load_state(self.private/'ledger.json')['calls']), 1)

    def test_rank_is_role_specific(self):
        self.seed()
        result=app.rank(params(limit=10),self.private)
        vals={r['route']:r['status'] for r in result['results']}
        self.assertEqual(vals['independent'],'eligible')
        self.assertEqual(vals['new_pi'],'conditional')

    def test_apply_creates_scaffold_and_does_not_submit(self):
        key=self.seed()
        app.rank(params(limit=10),self.private)
        result=app.apply(params(key=key,route='independent'),self.private)
        self.assertEqual(result['status'],'draft_scaffold_created')
        self.assertTrue(Path(result['proposal']).exists())
        self.assertEqual(pipeline.load_state(self.private/'ledger.json')['calls'][key]['stage'],'drafting')
        self.assertEqual(app.apply(params(key=key,route='independent'),self.private)['status'],
                         'draft_exists_not_overwritten')

    def test_conditional_new_pi_only_concept_not_ready(self):
        key=self.seed()
        app.rank(params(limit=10),self.private)
        result=app.apply(params(key=key,route='new_pi'),self.private)
        self.assertEqual(result['status'],'concept_only')
        self.assertTrue(Path(result['pi_outreach']).exists())
        with self.assertRaisesRegex(ValueError,'eligible'):
            app.ready(params(key=key,proposal_json='unused',confirm_reviewed=True),self.private)

    def test_compliance_ready_then_outcome_receipt(self):
        key=self.seed()
        app.rank(params(limit=10),self.private)
        app.apply(params(key=key,route='independent'),self.private)
        doc=self.private/'proposal.json'
        doc.write_text(json.dumps({'call_id':'demo-fellowship','sections':{'summary':'Verified claim.',
                             'plan':'A falsifiable evaluation using a strong comparative baseline.'},
                             'documents':['cv'],'evidence_index':[{'id':'cv:1','verified':True,'locator':'CV p.1'}],
                             'claims':[{'id':'c1','text':'Research record','evidence_ids':['cv:1']}],
                             'approval':{'applicant':True}}))
        good=app.ready(params(key=key,proposal_json=str(doc),confirm_reviewed=True),self.private)
        self.assertEqual(good['status'],'draft_ready_for_manual_submission')
        with self.assertRaisesRegex(ValueError,'confirmation'):
            app.outcome(params(key=key,to='submitted',confirmed=False,receipt=None,note=None),self.private)
        result=app.outcome(params(key=key,to='submitted',confirmed=True,
                                  receipt='portal-reference-123',note='Fictional test only'),self.private)
        self.assertEqual(result['transition']['stage'],'submitted')

    def test_tampered_official_host_blocked(self):
        self.setup_profile()
        app.setup_confirm(params(confirm_reviewed=True),self.private)
        leads=self.base/'leads.json'
        leads.write_text(json.dumps([dict(id='demo-fellowship',funder='Fictional Foundation',round='unverified',
                     official_url='https://example.org/grants/demo-fellowship')]))
        key=app.search(params(input_file=leads,feed_file=None,limit=10,query=None),self.private)['added'][0]
        bad=call();bad['official_url']='https://unrelated.invalid/call'
        path=self.base/'bad.json';path.write_text(json.dumps(bad))
        with self.assertRaisesRegex(ValueError,'host changed'):
            app.verify(params(key=key,call_file=path),self.private)

    def test_unverified_source_cannot_prepare_application(self):
        self.setup_profile()
        app.setup_confirm(params(confirm_reviewed=True),self.private)
        leads=self.base/'leads.json'
        leads.write_text(json.dumps([dict(id='demo-fellowship',funder='Fictional Foundation',round='unverified',
                     official_url='https://example.org/grants/demo-fellowship')]))
        key=app.search(params(input_file=leads,feed_file=None,limit=10,query=None),self.private)['added'][0]
        with self.assertRaisesRegex(ValueError,'unverified'):
            app.apply(params(key=key,route='independent'),self.private)


if __name__=='__main__':
    unittest.main()
