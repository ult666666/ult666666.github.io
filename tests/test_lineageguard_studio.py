"""The Studio showcase links actual implementation and preserves runtime boundaries."""
from pathlib import Path
import hashlib
import json
import struct
import unittest

ROOT = Path(__file__).resolve().parents[1]

class LineageGuardStudioTests(unittest.TestCase):
    def test_case_study_explains_executable_orchestration_and_runtime_limits(self):
        text = (ROOT / 'projects/lineageguard.html').read_text()
        for phrase in ('LineageGuard Studio', 'SQLite', 'browser-session', 'deterministic',
                       'bound to the source it was read from', 'docs/ARCHITECTURE.md', 'docs/VERIFICATION.md',
                       'test/studio/process-recovery.test.mjs', 'No SQL execution'):
            self.assertIn(phrase, text)

    def test_homepage_uses_the_verified_studio_capture(self):
        text = (ROOT / 'index.html').read_text()
        self.assertIn('LineageGuard Studio', text)
        self.assertIn('<img src="/assets/lineageguard-studio-review.png" width="1440" height="1404"', text)
        self.assertNotIn('lineageguard-studio-v2.png', text)
        self.assertIn('database schema changes', text)

    def test_new_screenshot_is_explicitly_in_the_public_inventory(self):
        inventory = json.loads((ROOT / 'public-files.json').read_text())['files']
        self.assertIn('assets/lineageguard-studio-review.png', inventory)
        self.assertNotIn('assets/lineageguard-studio-v2.png', inventory)
        raw = (ROOT / 'assets/lineageguard-studio-review.png').read_bytes()
        self.assertEqual(raw[:8], b'\x89PNG\r\n\x1a\n')
        self.assertEqual(struct.unpack('>II', raw[16:24]), (1440, 1404))
        # assets/studio-v2-desktop.png at LineageGuard commit ed48eea, copied unchanged (see docs/ASSETS.md).
        self.assertEqual(hashlib.sha256(raw).hexdigest(),
                         'e6165a633dfcc07468849da0f610e49b0bf0a31211133dcff576bba342795b45')

if __name__ == '__main__':
    unittest.main()
