#!/usr/bin/env python3
"""Lightweight funding PDF mechanical checks; cannot replace rendered visual review."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

PLACEHOLDER = re.compile(r'\[(?:TO CONFIRM|EVIDENCE NEEDED|HOST APPROVAL REQUIRED)[^\]]*\]', re.I)


def verify_pdf(path: Path, max_pages: int | None, required_text: list[str], min_chars: int = 40):
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise RuntimeError('pypdf missing: install funding-autopilot-skill[documents]') from exc
    if not path.is_file():
        raise ValueError(f'PDF does not exist: {path}')
    reader = PdfReader(str(path))
    pages = len(reader.pages)
    text_pages = [(page.extract_text() or '') for page in reader.pages]
    text = '\n'.join(text_pages)
    issues = []
    if max_pages is not None and pages > max_pages:
        issues.append(f'pages {pages} > scheme maximum {max_pages}')
    if len(text.strip()) < min_chars:
        issues.append(f'only {len(text.strip())} extractable characters, expected >= {min_chars}')
    for n, body in enumerate(text_pages, start=1):
        if not body.strip():
            issues.append(f'page {n} has no extractable text (could be image/scanned)')
    for phrase in required_text:
        if phrase.casefold() not in text.casefold():
            issues.append(f'required visible text absent from PDF layer: {phrase}')
    for match in PLACEHOLDER.finditer(text):
        issues.append(f'unresolved placeholder: {match.group()[:120]}')
    if '\ufffd' in text:
        issues.append('replacement characters found in extractable PDF text')
    return {'file': path.name, 'pages': pages, 'extractable_chars': len(text.strip()),
            'status': 'failed' if issues else 'mechanical_checks_passed_visual_review_required',
            'issues': issues, 'visual_review_required': True,
            'disclaimer': 'No clipping, overlap, font or page-break geometry is certified by text checks.'}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pdf', type=Path, required=True)
    parser.add_argument('--max-pages', type=int)
    parser.add_argument('--must-contain', action='append', default=[])
    parser.add_argument('--min-chars', type=int, default=40)
    args = parser.parse_args(argv)
    try:
        if args.max_pages is not None and args.max_pages <= 0:
            raise ValueError('--max-pages must be a positive integer')
        result = verify_pdf(args.pdf, args.max_pages, args.must_contain, args.min_chars)
        print(json.dumps(result, indent=2))
        return 0 if not result['issues'] else 1
    except (RuntimeError, ValueError, OSError) as exc:
        print(json.dumps({'error': str(exc), 'code': 'PDF_CHECK_UNAVAILABLE_OR_INVALID'}), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
