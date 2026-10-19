"""Regression tests for accidental disclosure through static site staging.

Only synthetic marker content is created. No real private file is read.
"""
from pathlib import Path
import hashlib
import importlib.util
import json
import os
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class PublicationGuardTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='portfolio-publication-test-')
        self.addCleanup(self.temp.cleanup)
        self.parent = Path(self.temp.name).resolve()
        self.root = self.parent / 'source'
        self.root.mkdir()
        spec = importlib.util.spec_from_file_location('publication_under_test', ROOT / 'scripts/build_site.py')
        self.build = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.build)
        for name in self.build.FILES:
            shutil.copyfile(ROOT / name, self.root / name)
        for name in self.build.DIRECTORIES:
            shutil.copytree(ROOT / name, self.root / name)
        for name in ('public-files.json',):
            if (ROOT / name).is_file(): shutil.copyfile(ROOT / name, self.root / name)
        self.build.ROOT = self.root
        self.output = self.parent / 'published'

    def assert_refused_before_output(self):
        with self.assertRaises((ValueError, OSError)):
            self.build.build(self.output)
        self.assertFalse(self.output.exists(), 'Invalid input produced a publishable-looking directory')

    def test_hidden_file_in_assets_is_not_published(self):
        (self.root / 'assets/.env').write_text('SYNTHETIC_PRIVATE_MARKER=not-a-credential\n')
        self.assert_refused_before_output()

    def test_private_note_in_projects_is_not_published(self):
        (self.root / 'projects/local-notes.txt').write_text('synthetic local-only note\n')
        self.assert_refused_before_output()

    def test_unlisted_image_is_not_implicitly_approved(self):
        shutil.copyfile(self.root / 'assets/portfolio-og.png', self.root / 'assets/unreviewed.png')
        self.assert_refused_before_output()

    def test_unlisted_subdirectory_is_refused_even_when_empty(self):
        (self.root / 'assets/private-backup').mkdir()
        self.assert_refused_before_output()

    def test_hardlinked_known_asset_is_refused(self):
        p = self.root / 'assets/portfolio-og.svg'
        original = self.parent / 'other-file.svg'
        p.rename(original)
        os.link(original, p)
        self.assert_refused_before_output()
        self.assertTrue(original.is_file())

    def test_symlinked_source_ancestor_is_refused(self):
        alias = self.parent / 'source-alias'
        alias.symlink_to(self.root, target_is_directory=True)
        self.build.ROOT = alias
        self.assert_refused_before_output()

    def test_symlinked_destination_ancestor_is_refused(self):
        external = self.parent / 'elsewhere'; external.mkdir()
        alias = self.parent / 'output-alias'; alias.symlink_to(external, target_is_directory=True)
        self.output = alias / 'published'
        self.assert_refused_before_output()
        self.assertEqual(list(external.iterdir()), [])

    def test_missing_approved_asset_is_refused(self):
        (self.root / 'assets/portfolio-og.png').unlink()
        self.assert_refused_before_output()

    def test_checked_in_inventory_rejects_duplicate_paths(self):
        path = self.root / 'public-files.json'
        self.assertTrue(path.exists(), 'There is no exact reviewed publication inventory')
        doc = json.loads(path.read_text()); doc['files'].append(doc['files'][0])
        path.write_text(json.dumps(doc))
        self.assert_refused_before_output()

    def test_release_inventory_matches_every_published_byte(self):
        self.build.build(self.output)
        manifest = self.output / 'release-manifest.json'
        self.assertTrue(manifest.is_file(), 'No independently checkable release inventory')
        doc = json.loads(manifest.read_text())
        actual = {p.relative_to(self.output).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in self.output.rglob('*') if p.is_file() and p != manifest}
        self.assertEqual(doc['files'], actual)
        self.assertEqual(doc['scope'], 'static_public_assets_only')
        self.assertFalse((self.output / 'public-files.json').exists())

    def test_identical_inputs_produce_identical_release_bytes(self):
        self.build.build(self.output)
        other = self.parent / 'second'; self.build.build(other)
        def inventory(root):
            return {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob('*') if p.is_file()}
        self.assertEqual(inventory(self.output), inventory(other))

    def test_modified_output_is_detected(self):
        self.build.build(self.output)
        (self.output / 'index.html').write_text('changed after staging')
        with self.assertRaisesRegex(ValueError, 'hash or size'): self.build.verify(self.output)

    def test_added_output_is_detected(self):
        self.build.build(self.output)
        (self.output / 'assets/unexpected.txt').write_text('synthetic unlisted output')
        with self.assertRaisesRegex(ValueError, 'inventory mismatch'): self.build.verify(self.output)

    def test_release_manifest_duplicate_key_is_refused(self):
        self.build.build(self.output)
        path = self.output / 'release-manifest.json'
        path.write_text(path.read_text().rstrip()[:-1] + ', "scope": "static_public_assets_only"}')
        with self.assertRaisesRegex(ValueError, 'Duplicate JSON key'): self.build.verify(self.output)

    def test_root_development_files_are_not_in_the_public_payload(self):
        (self.root / '.env').write_text('synthetic local configuration')
        (self.root / 'local-notes.md').write_text('synthetic local notes')
        self.build.build(self.output)
        self.assertFalse((self.output / '.env').exists())
        self.assertFalse((self.output / 'local-notes.md').exists())

    def test_unlisted_fifo_is_refused_without_opening_it(self):
        if not hasattr(os, 'mkfifo'): self.skipTest('FIFO not supported')
        os.mkfifo(self.root / 'assets/synthetic-pipe')
        self.assert_refused_before_output()

    def test_oversized_approved_asset_is_refused_before_output(self):
        with (self.root / 'assets/portfolio-og.png').open('wb') as handle:
            handle.truncate(self.build.MAX_FILE_BYTES + 1)
        self.assert_refused_before_output()

    def test_existing_output_is_preserved(self):
        self.output.mkdir(); marker = self.output / 'do-not-overwrite.txt'; marker.write_text('preserve\n')
        with self.assertRaises(FileExistsError): self.build.build(self.output)
        self.assertEqual(marker.read_text(), 'preserve\n')

if __name__ == '__main__': unittest.main(verbosity=2)
