#!/usr/bin/env python3
"""Stage only approved public web assets. Never copy Git data or test evidence."""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
FILES = ('index.html', 'fintech.html', '404.html', 'styles.css', 'fintech.css', 'script.js', 'robots.txt', 'sitemap.xml')
DIRECTORIES = ('assets', 'projects')

def build(destination: Path) -> None:
    destination = Path(destination)
    if destination.exists() or destination.is_symlink():
        raise FileExistsError('Refusing to overwrite an existing deployment directory')
    for name in FILES:
        source = ROOT / name
        if not source.is_file() or source.is_symlink():
            raise ValueError('Missing or unsafe public file: ' + name)
    for name in DIRECTORIES:
        base = ROOT / name
        if not base.is_dir() or base.is_symlink():
            raise ValueError('Unsafe public directory: ' + name)
        if any(p.is_symlink() for p in base.rglob('*')):
            raise ValueError('Symlinks are not allowed in published assets')
    destination.mkdir(parents=True, exist_ok=False)
    for name in FILES:
        shutil.copyfile(ROOT / name, destination / name)
    for name in DIRECTORIES:
        shutil.copytree(ROOT / name, destination / name)
    (destination / '.nojekyll').write_text('')
    print('SITE_STAGED', len(list(destination.rglob('*'))), 'entries')

if __name__ == '__main__':
    build(ROOT / '_site')
