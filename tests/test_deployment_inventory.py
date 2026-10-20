"""Deployment checks follow the reviewed allowlist without widening publication.

Each case uses a real temporary Git repository and the actual staging and
capture functions. No network or real private files are involved.
"""
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


class DeploymentInventoryTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='portfolio-deployment-inventory-')
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve() / 'source'
        self.root.mkdir()
        inventory = json.loads((ROOT / 'public-files.json').read_text())
        for name in inventory['files'] + [
                'public-files.json', 'scripts/build_site.py', 'scripts/verify_deployment.py']:
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, target)
        self.staged = self.root / '_site'

        spec = importlib.util.spec_from_file_location('build_site', self.root / 'scripts/build_site.py')
        self.build = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.build)
        with patch.dict(sys.modules, {'build_site': self.build}):
            spec = importlib.util.spec_from_file_location(
                'deployment_inventory_under_test', self.root / 'scripts/verify_deployment.py')
            self.verifier = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(self.verifier)
        self.git('init', '-q')

    def git(self, *arguments):
        return subprocess.check_output(
            ['git', '-c', 'user.name=Deployment Test', '-c', 'user.email=deployment@example.invalid',
             *arguments], cwd=self.root, text=True, timeout=10).strip()

    def commit_and_stage(self):
        self.git('add', '.')
        self.git('commit', '-qm', 'Reviewed synthetic deployment fixture')
        head = self.git('rev-parse', 'HEAD')
        with redirect_stdout(StringIO()):
            self.build.build(self.staged)
        return head

    def add_reviewed_asset(self, name='assets/reviewed-extension.svg'):
        (self.root / name).write_text('<svg xmlns="http://www.w3.org/2000/svg"/>\n')
        path = self.root / 'public-files.json'
        inventory = json.loads(path.read_text())
        inventory['files'].append(name)
        inventory['files'].sort()
        path.write_text(json.dumps(inventory, indent=2) + '\n')
        return len(inventory['files'])

    def test_additional_committed_allowlisted_asset_is_verified(self):
        expected_count = self.add_reviewed_asset()
        head = self.commit_and_stage()
        try:
            snapshot, bodies = self.verifier.capture(head)
        except ValueError as error:
            self.fail('A valid reviewed inventory was rejected: ' + str(error))
        self.assertEqual(snapshot['visitorSourceCount'], expected_count)
        self.assertIn('assets/reviewed-extension.svg', bodies)
        self.assertEqual(len(snapshot['deploymentFiles']), expected_count + 2)
        self.assertTrue(snapshot['reviewedCommitVerified'])
        self.assertEqual(snapshot['head'], head)

    def test_prepared_receipt_records_actual_reviewed_inventory_count(self):
        expected_count = self.add_reviewed_asset()
        head = self.commit_and_stage()
        output = self.root.parent / 'prepared.json'
        result = subprocess.run(
            [sys.executable, '-B', str(self.root / 'scripts/verify_deployment.py'),
             '--base-url', 'https://example.invalid', '--commit', head, '--output', str(output)],
            capture_output=True, text=True, timeout=20)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        receipt = json.loads(output.read_text())
        self.assertEqual(receipt['status'], 'prepared')
        self.assertEqual(receipt['counts']['visitorSources'], expected_count)
        self.assertEqual(receipt['bounds']['visitorSources'], expected_count)
        self.assertEqual(receipt['networkRequests'], 0)

    def test_unlisted_source_asset_is_still_rejected(self):
        head = self.commit_and_stage()
        (self.root / 'assets/unreviewed.svg').write_text('<svg/>\n')
        with self.assertRaisesRegex(ValueError, 'unlisted or missing file'):
            self.verifier.capture(head)

    def test_unlisted_staged_asset_is_rejected_even_with_forged_manifest(self):
        head = self.commit_and_stage()
        payload = self.build.source_snapshot()
        payload['assets/unreviewed.svg'] = b'<svg/>\n'
        (self.staged / 'assets/unreviewed.svg').write_bytes(payload['assets/unreviewed.svg'])
        (self.staged / self.build.MANIFEST).write_text(
            json.dumps(self.build.release_document(payload), sort_keys=True, indent=2) + '\n')
        with self.assertRaisesRegex(ValueError, 'Staged release inventory differs'):
            self.verifier.capture(head)

    def test_allowlist_change_after_review_is_rejected(self):
        head = self.commit_and_stage()
        self.add_reviewed_asset()
        shutil.rmtree(self.staged)
        with redirect_stdout(StringIO()):
            self.build.build(self.staged)
        with self.assertRaisesRegex(ValueError, 'reviewed commit does not contain every release'):
            self.verifier.capture(head)

    def test_inventory_above_existing_publication_bound_is_rejected(self):
        inventory_path = self.root / 'public-files.json'
        inventory = json.loads(inventory_path.read_text())
        while len(inventory['files']) <= 100:
            name = 'assets/bounded-' + str(len(inventory['files'])) + '.svg'
            inventory['files'].append(name)
            (self.root / name).write_text('<svg/>\n')
        inventory_path.write_text(json.dumps(inventory) + '\n')
        self.git('add', '.')
        self.git('commit', '-qm', 'Oversized synthetic inventory')
        with self.assertRaisesRegex(ValueError, 'Invalid reviewed public inventory'):
            self.verifier.capture(self.git('rev-parse', 'HEAD'))


if __name__ == '__main__':
    unittest.main()
