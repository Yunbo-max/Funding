import importlib.util
import sys
import unittest
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1] / 'skills/funding-autopilot/sources/ukri_rss.py'
spec = importlib.util.spec_from_file_location('ukri_rss', MODULE)
mod = importlib.util.module_from_spec(spec)
sys.modules['ukri_rss'] = mod
spec.loader.exec_module(mod)


def feed(items):
    return ('<?xml version="1.0"?><rss version="2.0"><channel>' + ''.join(items) + '</channel></rss>').encode()


def item(name='Open AI Fellowship', link='https://www.ukri.org/opportunity/open-ai-fellowship/', description='AI research'):
    return f'<item><title>{name}</title><link>{link}</link><description>{description}</description><pubDate>Fri, 16 Oct 2026 13:00:00 +0000</pubDate></item>'


class UKRITests(unittest.TestCase):
    def test_parse_official_rss_leads_not_verified_calls(self):
        data = mod.parse_feed(feed([item()]), query='AI')
        self.assertEqual(data['meta']['count'], 1)
        self.assertEqual(data['results'][0]['round'], 'unverified')
        self.assertEqual(data['results'][0]['call_status'], 'unknown')
        self.assertIsNone(data['results'][0].get('verified_at'))

    def test_query_filters(self):
        data = mod.parse_feed(feed([item(description='network AI'), item('Biomed Grant', 'https://www.ukri.org/opportunity/biomed/', 'other research')]), query='network')
        self.assertEqual(len(data['results']), 1)

    def test_duplicate_slug_deduped(self):
        self.assertEqual(mod.parse_feed(feed([item(), item()]))['meta']['count'], 1)

    def test_reject_non_ukri_link(self):
        self.assertEqual(mod.parse_feed(feed([item(link='https://evil.example/attack/')]))['meta']['count'], 0)

    def test_malformed_xml_fails(self):
        with self.assertRaisesRegex(ValueError, 'XML'):
            mod.parse_feed(b'<rss><channel>')

    def test_empty_feed_not_interpreted_as_zero_calls(self):
        with self.assertRaisesRegex(ValueError, 'no RSS items'):
            mod.parse_feed(feed([]))

    def test_detail_does_not_assert_verified_rule(self):
        r = mod.detail(b'<html><head><style>bad</style></head><body><main>A substantial UKRI call page for review. Eligibility details require human evaluation.</main></body></html>', 'https://www.ukri.org/opportunity/foo/')
        self.assertIn('retrieved_unverified', r['detail_status'])
        self.assertNotIn('bad', r['text'])

    def test_reject_unsafe_detail_host(self):
        with self.assertRaisesRegex(ValueError, 'UKRI'):
            mod.detail(b'legitimate text', 'https://evil.example/opportunity/foo/')


if __name__ == '__main__':
    unittest.main()
