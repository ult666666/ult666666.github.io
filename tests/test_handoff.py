"""Boundary tests: removing validation must permit unsafe input and fail these."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts/verify_handoff.py'
LOCK = json.loads((ROOT / 'examples/operations_handoff/release-lock.json').read_text())


def launcher():
    assert SCRIPT.is_file(), 'offline handoff launcher is not implemented'
    spec = importlib.util.spec_from_file_location('verify_handoff', SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class HandoffBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='handoff 测试 ')
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.wheels = self.base / '-wheels 空间'
        self.wheels.mkdir()
        self.lock = json.loads(json.dumps(LOCK))
        for item in self.lock['wheels']:
            wheel = self.wheels / item['filename']
            name = item['distribution'].replace('-', '_')
            with zipfile.ZipFile(wheel, 'w') as archive:
                archive.writestr(f'{name}-{item["version"]}.dist-info/METADATA',
                                 f'Metadata-Version: 2.1\nName: {item["distribution"]}\nVersion: {item["version"]}\n')
                archive.writestr(f'{name}-{item["version"]}.dist-info/WHEEL',
                                 'Wheel-Version: 1.0\nRoot-Is-Purelib: true\nTag: py3-none-any\n')
            item['sha256'] = hashlib.sha256(wheel.read_bytes()).hexdigest()
        self.output = self.base / '-result 结果'

    def test_valid_unicode_space_and_leading_hyphen_paths(self):
        wheels, output = launcher().validate_inputs(self.wheels, self.output, self.lock)
        self.assertEqual(len(wheels), 3)
        self.assertEqual(output, self.output.parent.resolve() / self.output.name)
        self.assertFalse(output.exists())

    def test_missing_foreign_or_changed_wheel_rejected(self):
        module = launcher()
        wheel = self.wheels / self.lock['wheels'][0]['filename']
        good = wheel.read_bytes()
        for mode in ('missing', 'foreign', 'changed'):
            with self.subTest(mode=mode):
                wheel.write_bytes(good)
                foreign = self.wheels / 'foreign.whl'
                if mode == 'missing': wheel.unlink()
                if mode == 'foreign': foreign.write_bytes(b'foreign')
                if mode == 'changed': wheel.write_bytes(good + b'changed')
                with self.assertRaises(module.HandoffError):
                    module.validate_inputs(self.wheels, self.output, self.lock)
                self.assertFalse(self.output.exists())
                foreign.unlink(missing_ok=True)

    def test_metadata_mismatch_rejected_even_with_matching_hash(self):
        module = launcher()
        self.lock['wheels'][0]['version'] = '999.0.0'
        with self.assertRaises(module.HandoffError):
            module.validate_inputs(self.wheels, self.output, self.lock)

    def test_selected_wheel_directory_or_wheel_symlink_rejected(self):
        module = launcher()
        alias = self.base / 'wheel-link'
        alias.symlink_to(self.wheels, target_is_directory=True)
        with self.assertRaises(module.HandoffError):
            module.validate_inputs(alias, self.output, self.lock)
        wheel = self.wheels / self.lock['wheels'][0]['filename']
        moved = self.base / 'moved.whl'
        wheel.rename(moved)
        wheel.symlink_to(moved)
        with self.assertRaises(module.HandoffError):
            module.validate_inputs(self.wheels, self.output, self.lock)

    def test_existing_outputs_and_source_aliases_remain_untouched(self):
        module = launcher()
        sentinel = self.base / 'sentinel'
        sentinel.write_text('keep')
        existing_dir = self.base / 'existing'
        existing_dir.mkdir()
        link = self.base / 'output-link'
        link.symlink_to(sentinel)
        hard = self.base / 'output-hard'
        os.link(sentinel, hard)
        missing_parent = self.base / 'missing' / 'result'
        for output in (sentinel, existing_dir, link, hard, self.wheels / 'result',
                       ROOT / 'scripts' / 'new-result', missing_parent):
            with self.subTest(output=output):
                with self.assertRaises(module.HandoffError):
                    module.validate_inputs(self.wheels, output, self.lock)
        self.assertEqual(sentinel.read_text(), 'keep')
        self.assertEqual(list(existing_dir.iterdir()), [])

    def test_install_failure_cleans_execution_and_leaves_no_output(self):
        module = launcher()
        before = set(self.base.iterdir())
        with patch.object(module, 'load_lock', return_value=self.lock), \
             patch.object(module, 'run_checked', side_effect=module.HandoffError('bounded child failed')):
            with self.assertRaises(module.HandoffError):
                module.verify(self.wheels, self.output)
        self.assertEqual(set(self.base.iterdir()), before)

    def test_bad_arguments_exit_two_without_output(self):
        result = subprocess.run([os.sys.executable, '-B', str(SCRIPT), '--wheel-dir', str(self.wheels)],
                                capture_output=True, timeout=10)
        self.assertEqual(result.returncode, 2)
        self.assertIn(b'usage:', result.stderr)
        self.assertFalse(self.output.exists())


@unittest.skipUnless(os.environ.get('HANDOFF_WHEEL_DIR'), 'set HANDOFF_WHEEL_DIR for fresh installed integration')
class InstalledHandoffTests(unittest.TestCase):
    def test_real_installed_contract_and_retained_reports(self):
        with tempfile.TemporaryDirectory(prefix='installed integration 交接 ') as directory:
            output = Path(directory) / '-result 结果'
            result = subprocess.run([os.sys.executable, '-B', str(SCRIPT), '--wheel-dir',
                                     os.environ['HANDOFF_WHEEL_DIR'], '--output', str(output)],
                                    capture_output=True, timeout=240)
            self.assertEqual(result.returncode, 0, result.stderr.decode())
            receipt = json.loads((output / 'handoff-receipt.json').read_text())
            self.assertEqual(receipt['tracebench_exit_codes'], {'clean': 0, 'synthetic_regression': 3, 'invalid_input': 2})
            records = {r['id']: r['output'] for r in map(json.loads, (output / 'outputs.jsonl').read_text().splitlines())}
            self.assertEqual(records['import-totals']['current_exact'], {
                'sessions': 2, 'unique_participants': 3, 'attendance': 4, 'participant_hours_hundredths': 700,
                'session_hours_hundredths': 350, 'budget_cents': 13025, 'actual_cents': 13025, 'variance_cents': 0})
            self.assertEqual(records['comparison']['deltas_exact'], {
                'sessions': 0, 'unique_participants': 1, 'attendance': 1, 'participant_hours_hundredths': 375,
                'session_hours_hundredths': 150, 'budget_cents': 15, 'actual_cents': -75, 'variance_cents': -90})
            self.assertEqual(records['advisory-race']['global_rows_after'], {'sessions': 5, 'attendance': 7})
            self.assertEqual(records['restored-states']['all_columns_equal'], True)
            self.assertEqual(set(p.name for p in output.iterdir()), set(launcher().REPORT_FILES))
            clean = json.loads((output / 'clean.json').read_text())
            regression = json.loads((output / 'synthetic-regression.json').read_text())
            self.assertEqual(clean['summary']['failed'], 0)
            self.assertGreater(regression['summary']['failed'], 0)
            for p in output.iterdir():
                text = p.read_text()
                self.assertNotIn(directory, text)
                self.assertNotIn(str(ROOT), text)
                self.assertNotIn('lease_token', text)
                self.assertLess(p.stat().st_size, 1_048_576)
