"""The Studio showcase links actual implementation and preserves runtime boundaries."""
from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]

class LineageGuardStudioTests(unittest.TestCase):
    def test_case_study_explains_executable_orchestration_and_runtime_limits(self):
        text = (ROOT / 'projects/lineageguard.html').read_text()
        for phrase in ('LineageGuard Studio', 'SQLite', 'browser-session', 'deterministic',
                       'source-bound', 'docs/ARCHITECTURE.md', 'docs/VERIFICATION.md',
                       'test/studio/process-recovery.test.mjs', 'No SQL execution'):
            self.assertIn(phrase, text)

    def test_homepage_uses_the_verified_studio_capture(self):
        text = (ROOT / 'index.html').read_text()
        self.assertIn('LineageGuard Studio', text)
        self.assertIn('/assets/lineageguard-studio-v2.png', text)
        self.assertIn('Workflow orchestration', text)
        self.assertIn('browser-session preview', text)

    def test_new_screenshot_is_explicitly_in_the_public_inventory(self):
        inventory = json.loads((ROOT / 'public-files.json').read_text())['files']
        self.assertIn('assets/lineageguard-studio-v2.png', inventory)
        self.assertEqual((ROOT / 'assets/lineageguard-studio-v2.png').read_bytes()[:8], b'\x89PNG\r\n\x1a\n')

if __name__ == '__main__':
    unittest.main()
