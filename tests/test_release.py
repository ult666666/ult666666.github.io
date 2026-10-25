"""Release checks: application-ready metadata and a public-only deploy payload."""
from pathlib import Path
import importlib.util
import json
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]

class ReleaseTests(unittest.TestCase):
    def test_social_image_is_raster_and_exists(self):
        page = (ROOT / 'index.html').read_text()
        self.assertIn('https://ult666666.github.io/assets/portfolio-og.png', page)
        image = ROOT / 'assets/portfolio-og.png'
        self.assertTrue(image.is_file())
        self.assertEqual(image.read_bytes()[:8], b'\x89PNG\r\n\x1a\n')

    def test_copy_and_student_metadata(self):
        text = (ROOT / 'index.html').read_text()
        self.assertNotIn('TYPECRIPT', text)
        self.assertNotIn('"alumniOf":null', text)
        self.assertIn('Carnegie Mellon University student', text)
        self.assertIn('No automated order execution', text)

    def test_crawler_and_not_found_pages(self):
        for name in ('robots.txt', 'sitemap.xml', '404.html'):
            self.assertTrue((ROOT / name).is_file(), name)
        self.assertIn('https://ult666666.github.io/sitemap.xml', (ROOT/'robots.txt').read_text())

    def test_deploy_stages_only_public_files(self):
        path = ROOT / 'scripts/build_site.py'
        self.assertTrue(path.is_file(), 'Missing public-only site staging build')
        spec = importlib.util.spec_from_file_location('site_build', path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as t:
            destination = Path(t).resolve() / 'site'  # resolve our own newly-created macOS temp directory
            module.build(destination)
            names = {x.name for x in destination.iterdir()}
            self.assertEqual(names, {'index.html', 'fintech.html', '404.html', 'styles.css', 'fintech.css', 'robots.txt', 'sitemap.xml', 'assets', 'projects', '.nojekyll', 'release-manifest.json'})
            self.assertFalse((destination / '.git').exists())
            self.assertFalse((destination / 'tests').exists())
            self.assertEqual(len(list((destination / 'projects').glob('*.html'))), 6)
            with self.assertRaises(FileExistsError):
                module.build(destination)

if __name__ == '__main__':
    unittest.main(verbosity=2)
