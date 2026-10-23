#!/usr/bin/env python3
"""Explicit optional network step: fetch only the three source-reviewed releases."""
import argparse
from pathlib import Path
import shutil
import sys
import tempfile
import time
from urllib.error import URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

from verify_handoff import HandoffError, MAX_WHEEL_BYTES, load_lock, new_destination, validate_inputs


def check_https(url):
    parsed = urlsplit(url)
    if (parsed.scheme != 'https' or parsed.hostname not in
            {'github.com', 'release-assets.githubusercontent.com', 'objects.githubusercontent.com'}
            or parsed.username or parsed.password or parsed.port not in (None, 443)):
        raise HandoffError('release URL and redirects must use approved GitHub HTTPS hosts')


class ReleaseRedirect(HTTPRedirectHandler):
    def __init__(self, deadline=None):
        self.deadline = time.monotonic() + 60 if deadline is None else deadline
        super().__init__()

    def redirect_request(self, request, response, code, message, headers, newurl):
        check_https(newurl)
        # urllib follows redirects using the original request's timeout.
        request.timeout = remaining(self.deadline)
        return super().redirect_request(request, response, code, message, headers, newurl)


def remaining(deadline):
    value = deadline - time.monotonic()
    if value <= 0:
        raise HandoffError('release download deadline expired')
    return min(value, 8)


def download_one(item, destination, deadline):
    expected = ('https://github.com/' + item['repository'] + '/releases/download/' + item['tag'] + '/' + item['filename'])
    if item['url'] != expected:
        raise HandoffError('release URL must match the reviewed repository/tag/filename')
    check_https(expected)
    timeout = remaining(deadline)
    created = False
    try:
        opener = build_opener(ReleaseRedirect(deadline))
        with opener.open(Request(expected, headers={'User-Agent': 'synthetic-handoff-verifier/1'}), timeout=timeout) as response:
            check_https(response.geturl())
            content = bytearray()
            while True:
                remaining(deadline)
                block = response.read(min(65536, MAX_WHEEL_BYTES + 1 - len(content)))
                if not block:
                    break
                content.extend(block)
                if len(content) > MAX_WHEEL_BYTES:
                    raise HandoffError('release wheel exceeds the 8 MiB limit')
            remaining(deadline)
            with destination.open('xb') as stream:
                created = True
                stream.write(content)
    except BaseException:
        if created:
            destination.unlink(missing_ok=True)
        raise


def fetch(output):
    destination = new_destination(output)
    lock = load_lock()
    published = False
    with tempfile.TemporaryDirectory(prefix='.handoff-download ', dir=destination.parent) as directory:
        wheels = Path(directory) / 'wheels'
        wheels.mkdir()
        deadline = time.monotonic() + 60
        for item in lock['wheels']:
            download_one(item, wheels / item['filename'], deadline)
        # Hash, metadata, filename and complete-set verification before publication.
        paths, _ = validate_inputs(wheels, Path(directory) / 'unused', lock)
        try:
            destination.mkdir(mode=0o700)
            published = True
            for path in paths:
                with (destination / path.name).open('xb') as stream:
                    stream.write(path.read_bytes())
        except BaseException:
            if published:
                shutil.rmtree(destination)
            raise


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--download', action='store_true', required=True, help='explicitly enable fixed-release network downloads')
    parser.add_argument('--output', type=Path, required=True, help='new directory outside source; trusted existing parent')
    args = parser.parse_args(argv)
    try:
        fetch(args.output)
    except (HandoffError, OSError, URLError, ValueError):
        print('handoff download failed; no verified wheel directory published', file=sys.stderr)
        return 2
    print('Three reviewed release wheels downloaded and byte-verified.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
