"""Downloader safety: fixed reviewed URLs, explicit mode and bounded bytes."""
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts/fetch_handoff_wheels.py'


def downloader():
    assert SCRIPT.is_file(), 'explicit fixed-release downloader is not implemented'
    spec = importlib.util.spec_from_file_location('fetch_handoff_wheels', SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(ROOT / 'scripts'))
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path.pop(0)
    return module


class DownloadTests(unittest.TestCase):
    def test_network_requires_explicit_download_mode(self):
        result = subprocess.run([sys.executable, '-B', str(SCRIPT), '--output', 'unused'], capture_output=True, timeout=10)
        self.assertEqual(result.returncode, 2)
        self.assertIn(b'--download', result.stderr)

    def test_existing_destination_is_preserved_before_network(self):
        module = downloader()
        with tempfile.TemporaryDirectory(prefix='download 测试 ') as directory:
            target = Path(directory) / '-wheels'
            target.mkdir()
            (target / 'keep').write_text('keep')
            with patch.object(module, 'download_one', side_effect=AssertionError('network must not start')):
                with self.assertRaises(module.HandoffError):
                    module.fetch(target)
            self.assertEqual((target / 'keep').read_text(), 'keep')

    def test_bad_hash_and_network_failure_leave_no_directory(self):
        module = downloader()
        with tempfile.TemporaryDirectory(prefix='download 测试 ') as directory:
            for mode in ('hash', 'network'):
                with self.subTest(mode=mode):
                    target = Path(directory) / '-wheels'
                    def fake(item, destination, deadline):
                        if mode == 'network': raise module.HandoffError('network failed')
                        destination.write_bytes(b'incorrect released wheel bytes')
                    with patch.object(module, 'download_one', side_effect=fake):
                        with self.assertRaises(module.HandoffError):
                            module.fetch(target)
                    self.assertEqual(list(Path(directory).iterdir()), [])

    def test_redirects_refuse_non_https_and_foreign_hosts(self):
        module = downloader()
        for url in ('http://github.com/file', 'https://attacker.invalid/code.whl', 'file:///tmp/code.whl'):
            with self.subTest(url=url):
                with self.assertRaises(module.HandoffError):
                    module.check_https(url)
        module.check_https('https://release-assets.githubusercontent.com/fixed-release')

    def test_redirect_chain_shares_download_deadline(self):
        module = downloader()
        handler = module.ReleaseRedirect()
        handler.deadline = module.time.monotonic() - 1
        request = module.Request('https://github.com/reviewed')
        request.timeout = 8
        with self.assertRaises(module.HandoffError):
            handler.redirect_request(request, None, 302, 'redirect', {},
                                     'https://release-assets.githubusercontent.com/fixed-release')

    def test_stream_has_size_and_deadline_bounds(self):
        module = downloader()
        class Response:
            def __init__(self): self.blocks = 0
            def read(self, size):
                self.blocks += 1
                return b'x' * min(size, 65536)
            def __enter__(self): return self
            def __exit__(self, *args): return False
            def geturl(self): return 'https://github.com/reviewed'
        class Opener:
            def open(self, request, timeout): return Response()
        item = module.load_lock()['wheels'][0]
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'wheel.whl'
            with patch.object(module, 'build_opener', return_value=Opener()), patch.object(module, 'MAX_WHEEL_BYTES', 100):
                with self.assertRaises(module.HandoffError):
                    module.download_one(item, target, module.time.monotonic() + 10)
                self.assertFalse(target.exists())
            with self.assertRaises(module.HandoffError):
                module.download_one(item, target, module.time.monotonic() - 1)
            self.assertFalse(target.exists())
