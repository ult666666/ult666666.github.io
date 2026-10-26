#!/usr/bin/env python3
"""Stage an exact reviewed public inventory, then verify every emitted byte.

This guard prevents accidental publishing of unlisted workspace files. It is
not a secret scanner or a guarantee against a malicious trusted contributor.
"""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import json
import os
import re
import stat

ROOT = Path(__file__).resolve().parents[1]
FILES = ('index.html', 'fintech.html', '404.html', 'styles.css', 'fintech.css', 'project-catalog.css', 'project-catalog.js', 'robots.txt', 'sitemap.xml')
DIRECTORIES = ('assets', 'projects')
INVENTORY = 'public-files.json'
MANIFEST = 'release-manifest.json'
MAX_FILE_BYTES = 8 * 1024 * 1024
MAX_TOTAL_BYTES = 32 * 1024 * 1024
BLAST_DEMO = 'projects/blast-radius-demo.html'
BLAST_LOCK = 'docs/blast-demo-lock.json'


def safe_path(path: Path) -> Path:
    path = Path(path).absolute()
    if '..' in path.parts or any(p.is_symlink() for p in (path, *path.parents)):
        raise ValueError('Symlink or parent traversal refused')
    return path


def read_regular(path: Path, limit: int = MAX_FILE_BYTES) -> bytes:
    path = safe_path(path)
    info = path.lstat()
    if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1 or info.st_size > limit:
        raise ValueError('Non-regular, linked or oversized public file')
    flags = os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0) | getattr(os, 'O_NONBLOCK', 0)
    fd = os.open(path, flags)
    with os.fdopen(fd, 'rb') as handle:
        opened = os.fstat(handle.fileno())
        if (not stat.S_ISREG(opened.st_mode) or opened.st_nlink != 1
                or (opened.st_dev, opened.st_ino) != (info.st_dev, info.st_ino)):
            raise ValueError('Public file identity changed')
        raw = handle.read(limit + 1)
        after = os.fstat(handle.fileno())
    if len(raw) > limit or (opened.st_size, opened.st_mtime_ns, opened.st_ctime_ns) != (
            after.st_size, after.st_mtime_ns, after.st_ctime_ns):
        raise ValueError('Public file changed during snapshot')
    return raw


def unique_object(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise ValueError('Duplicate JSON key')
        obj[key] = value
    return obj


def load_json(raw: bytes) -> dict:
    result = json.loads(raw, object_pairs_hook=unique_object)
    if not isinstance(result, dict):
        raise ValueError('Expected a JSON object')
    return result


def approved_name(name) -> bool:
    if not isinstance(name, str):
        return False
    rel = PurePosixPath(name)
    return (rel.as_posix() == name and not rel.is_absolute() and '..' not in rel.parts
            and (name in FILES or re.fullmatch(
                r'(?:assets/[a-zA-Z0-9_-]+\.(?:png|jpg|svg)|projects/[a-zA-Z0-9_-]+\.html)', name) is not None))


def validate_blast_demo(raw: bytes, lock: dict) -> None:
    """Keep the executable vendor artifact bound to its clean upstream build."""
    if (set(lock) != {'schema', 'repository', 'sourceCommit', 'sourceDirty',
                     'artifact', 'sha256', 'bytes'}
            or lock.get('schema') != 'blast-offline-demo/1'
            or lock.get('repository') != 'https://github.com/ult666666/blast-radius-daily'
            or lock.get('artifact') != BLAST_DEMO or lock.get('sourceDirty') is not False
            or not isinstance(lock.get('sourceCommit'), str)
            or re.fullmatch(r'[a-f0-9]{40}', lock['sourceCommit']) is None
            or type(lock.get('bytes')) is not int or lock['bytes'] != len(raw)
            or hashlib.sha256(raw).hexdigest() != lock.get('sha256')
            or ('<meta name="blast-source-commit" content="' + lock['sourceCommit'] + '" />').encode() not in raw):
        raise ValueError('Blast demo differs from its reviewed clean source/build lock')


def source_snapshot() -> dict[str, bytes]:
    root = safe_path(ROOT)
    document = load_json(read_regular(root / INVENTORY, 32768))
    names = document.get('files')
    if (set(document) != {'version', 'files'} or type(document['version']) is not int
            or document['version'] != 1 or not isinstance(names, list) or not 1 <= len(names) <= 100
            or not all(approved_name(name) for name in names)
            or len(names) != len(set(names)) or not set(FILES).issubset(names)):
        raise ValueError('Invalid reviewed public inventory')
    # The roots are approved, but their contents are not implicitly approved.
    # Refuse unexpected entries before creating an output directory.
    actual = set(FILES)
    for name in DIRECTORIES:
        directory = safe_path(root / name)
        if not directory.is_dir():
            raise ValueError('Missing public directory')
        for entry in directory.iterdir():
            safe_path(entry)
            if not stat.S_ISREG(entry.lstat().st_mode):
                raise ValueError('Unexpected directory or special public entry')
            actual.add(entry.relative_to(root).as_posix())
    if actual != set(names):
        raise ValueError('Public inventory mismatch: unlisted or missing file')
    snapshot = {name: read_regular(root / name) for name in sorted(names)}
    if BLAST_DEMO not in snapshot:
        raise ValueError('Missing reviewed Blast demo')
    validate_blast_demo(snapshot[BLAST_DEMO], load_json(read_regular(root / BLAST_LOCK, 32768)))
    if sum(len(raw) for raw in snapshot.values()) > MAX_TOTAL_BYTES:
        raise ValueError('Public payload exceeds size budget')
    snapshot['.nojekyll'] = b''
    return snapshot


def release_document(payload: dict[str, bytes]) -> dict:
    return {'schema': 'public_portfolio_release/1', 'scope': 'static_public_assets_only',
            'file_count': len(payload), 'total_bytes': sum(map(len, payload.values())),
            'files': {name: hashlib.sha256(raw).hexdigest() for name, raw in sorted(payload.items())}}


def verify(destination: Path) -> dict:
    destination = safe_path(destination)
    document = load_json(read_regular(destination / MANIFEST, 32768))
    entries = document.get('files')
    if (set(document) != {'schema', 'scope', 'file_count', 'total_bytes', 'files'}
            or document.get('schema') != 'public_portfolio_release/1'
            or document.get('scope') != 'static_public_assets_only'
            or type(document.get('file_count')) is not int
            or type(document.get('total_bytes')) is not int
            or not isinstance(entries, dict) or not 1 <= len(entries) <= 101
            or not set(FILES).issubset(entries) or '.nojekyll' not in entries):
        raise ValueError('Invalid release inventory')
    if any((not approved_name(name) and name != '.nojekyll') or not isinstance(digest, str)
           or re.fullmatch(r'[a-f0-9]{64}', digest) is None for name, digest in entries.items()):
        raise ValueError('Invalid release entry')
    actual = {}
    for entry in destination.rglob('*'):
        safe_path(entry)
        name = entry.relative_to(destination).as_posix()
        if entry.is_dir():
            if name not in DIRECTORIES:
                raise ValueError('Unlisted release directory')
        elif name != MANIFEST:
            actual[name] = read_regular(entry)
    if set(actual) != set(entries):
        raise ValueError('Release inventory mismatch')
    if sum(map(len, actual.values())) > MAX_TOTAL_BYTES or release_document(actual) != document:
        raise ValueError('Release hash or size mismatch')
    return document


def build(destination: Path) -> dict:
    destination = safe_path(destination)
    if destination.exists():
        raise FileExistsError('Refusing to overwrite an existing deployment directory')
    payload = source_snapshot()
    # All validation completes before output creation. Copy the checked bytes,
    # rather than reading the workspace paths a second time.
    destination.mkdir(parents=True, exist_ok=False)
    for name, raw in payload.items():
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open('xb') as handle:
            handle.write(raw)
    with (destination / MANIFEST).open('x', encoding='utf-8') as handle:
        json.dump(release_document(payload), handle, sort_keys=True, indent=2)
        handle.write('\n')
    result = verify(destination)
    print('SITE_STAGED', result['file_count'], 'public files plus the release inventory')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', type=Path, help='Verify an existing staged public site; write nothing')
    args = parser.parse_args()
    if args.verify:
        result = verify(args.verify)
        print('SITE_VERIFIED', result['file_count'], 'public files')
    else:
        build(ROOT / '_site')
