#!/usr/bin/env python3
"""UKRI official RSS discovery adapter; results are unverified leads, not eligibility."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

FEED = 'https://www.ukri.org/opportunity/feed/'
ALLOWED_HOSTS = {'www.ukri.org', 'ukri.org'}
MAX_BYTES = 2_000_000


class PlainText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.text = []
        self.hidden = 0

    def handle_starttag(self, tag, attrs):
        if tag.lower() in {'script', 'style', 'svg'}:
            self.hidden += 1

    def handle_endtag(self, tag):
        if tag.lower() in {'script', 'style', 'svg'}:
            self.hidden = max(0, self.hidden - 1)

    def handle_data(self, data):
        if not self.hidden and data.strip():
            self.text.append(data.strip())


def strip_html(value: str) -> str:
    parser = PlainText()
    parser.feed(value or '')
    return re.sub(r'\s+', ' ', ' '.join(parser.text)).strip()


def valid_ukri_url(value: str) -> str:
    parsed = urlparse(value)
    if (parsed.scheme != 'https' or parsed.hostname not in ALLOWED_HOSTS
            or parsed.username or parsed.password or not parsed.path.startswith('/opportunity/')):
        raise ValueError('only public official UKRI opportunity HTTPS URLs are allowed')
    return parsed.geturl()


def get_bytes(url: str, timeout: int = 10):
    valid_ukri_url(url)
    req = Request(url, headers={'User-Agent': 'FundingAutopilot/0.2 (research funding discovery; no bulk scraping)',
                                'Accept': 'application/rss+xml,application/xml,text/html;q=0.8'})
    with urlopen(req, timeout=timeout) as response:
        valid_ukri_url(response.geturl())  # do not follow a redirect into an outside domain
        body = response.read(MAX_BYTES + 1)
        if len(body) > MAX_BYTES:
            raise ValueError('official response exceeded conservative size limit')
        return body


def parse_feed(data: bytes, query: str = '', limit: int = 30, checked_at: str | None = None):
    if limit < 1 or limit > 100:
        raise ValueError('limit must be from 1 to 100')
    try:
        root = ET.fromstring(data)
    except ET.ParseError as exc:
        raise ValueError(f'invalid RSS XML: {exc}') from exc
    if root.tag.lower() != 'rss':
        raise ValueError('expected UKRI RSS feed root')
    items = root.findall('./channel/item')
    if not items:
        raise ValueError('feed contains no RSS items: source may have changed')
    seen, leads = set(), []
    for item in items:
        title = strip_html(item.findtext('title', default=''))
        url = (item.findtext('link', default='') or '').strip()
        try:
            url = valid_ukri_url(url)
        except ValueError:
            continue
        description = strip_html(item.findtext('description', default=''))
        if query and query.casefold() not in (title + ' ' + description).casefold():
            continue
        path = urlparse(url).path.rstrip('/')
        slug = path.split('/')[-1] or hashlib.sha256(url.encode()).hexdigest()[:12]
        if slug in seen:
            continue
        seen.add(slug)
        posted = item.findtext('pubDate')
        try:
            dt = parsedate_to_datetime(posted)
            pub_iso = dt.astimezone(timezone.utc).isoformat() if dt.tzinfo else None
        except (TypeError, ValueError):
            pub_iso = None
        leads.append({'id': slug, 'funder': 'UKRI', 'round': 'unverified',
                      'title': title, 'official_url': url, 'discovered_via': 'ukri-official-rss',
                      'call_status': 'unknown', 'description': description,
                      'published_at': pub_iso})
        if len(leads) >= limit:
            break
    return {'meta': {'source': FEED, 'checked_at': checked_at or datetime.now(timezone.utc).isoformat(),
                     'count': len(leads), 'query': query, 'status': 'discovery_only_not_eligibility'},
            'results': leads}


def detail(data: bytes, url: str, max_chars: int = 50000):
    valid_ukri_url(url)
    parser = PlainText()
    parser.feed(data.decode('utf-8', errors='replace'))
    body = re.sub(r'\s+', ' ', ' '.join(parser.text)).strip()
    if len(body) < 50:
        raise ValueError('insufficient HTML extractable text; review official URL with host browser')
    return {'url': url, 'source_sha256': hashlib.sha256(data).hexdigest(),
            'retrieved_at': datetime.now(timezone.utc).isoformat(),
            'detail_status': 'retrieved_unverified_check_actual_guidance',
            'text': body[:max_chars], 'truncated': len(body) > max_chars}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='cmd', required=True)
    search = sub.add_parser('search')
    search.add_argument('--query', default='')
    search.add_argument('--limit', type=int, default=30)
    search.add_argument('--xml-file', type=Path, help='local fixture/offline XML; otherwise fetch official UKRI RSS')
    view = sub.add_parser('detail')
    view.add_argument('url')
    view.add_argument('--html-file', type=Path, help='offline/fixture source, otherwise fetch public UKRI page')
    args = p.parse_args(argv)
    try:
        if args.cmd == 'search':
            contents = args.xml_file.read_bytes() if args.xml_file else get_bytes(FEED)
            result = parse_feed(contents, args.query, args.limit)
        else:
            contents = args.html_file.read_bytes() if args.html_file else get_bytes(args.url)
            result = detail(contents, args.url)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    except (OSError, ValueError, TimeoutError) as exc:
        print(json.dumps({'error': str(exc), 'code': 'UKRI_SOURCE_ERROR'}), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
