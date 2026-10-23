#!/usr/bin/env python3
"""Offline verification of reviewed wheels; trusted code and local directories."""
import argparse
from email.parser import BytesParser
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / 'examples/operations_handoff'
MAX_WHEEL_BYTES = 8 * 1024 * 1024
MAX_REPORT_BYTES = 1024 * 1024
REPORT_FILES = ('handoff-receipt.json', 'fixture-hashes.json', 'outputs.jsonl',
                'synthetic-regression-outputs.jsonl', 'clean.json', 'clean.md', 'clean.html',
                'synthetic-regression.json', 'synthetic-regression.md', 'synthetic-regression.html')


class HandoffError(ValueError):
    """A bounded handoff could not be verified; no successful output is published."""


def load_lock():
    return json.loads((FIXTURES / 'release-lock.json').read_text(encoding='utf-8'))


def new_destination(output):
    selected = Path(os.path.abspath(output))
    if selected.exists() or selected.is_symlink():
        raise HandoffError('output must not exist, including aliases and symlinks')
    try:
        parent = selected.parent.resolve(strict=True)
    except OSError as exc:
        raise HandoffError('output parent must already exist') from exc
    if not parent.is_dir():
        raise HandoffError('output parent must be a directory')
    destination = parent / selected.name
    if destination.is_relative_to(ROOT):
        raise HandoffError('output must be outside the source checkout')
    return destination


def validate_inputs(wheel_dir, output, lock):
    destination = new_destination(output)
    selected = Path(wheel_dir)
    if selected.is_symlink() or not selected.is_dir():
        raise HandoffError('select a real flat wheel directory')
    directory = selected.resolve(strict=True)
    if destination.is_relative_to(directory):
        raise HandoffError('output must not alias or be inside wheel inputs')
    entries = lock.get('wheels', [])
    if lock.get('schema_version') != 1 or len(entries) != 3:
        raise HandoffError('lock must contain exactly three schema-1 wheels')
    names = [entry.get('filename', '') for entry in entries]
    if len(set(names)) != 3 or any(not re.fullmatch(r'[A-Za-z0-9_.-]+-py3-none-any\.whl', n) for n in names):
        raise HandoffError('invalid locked wheel filenames')
    if {p.name for p in directory.iterdir()} != set(names):
        raise HandoffError('wheel directory must contain precisely the three locked wheels')
    wheels = []
    for item in entries:
        wheel = directory / item['filename']
        details = wheel.lstat()
        if not stat.S_ISREG(details.st_mode) or not 0 < details.st_size <= MAX_WHEEL_BYTES:
            raise HandoffError('selected wheel must be a bounded regular file')
        content = wheel.read_bytes()
        if hashlib.sha256(content).hexdigest() != item.get('sha256'):
            raise HandoffError('wheel SHA-256 does not match the reviewed lock')
        try:
            with zipfile.ZipFile(wheel) as archive:
                prefix = item['distribution'].replace('-', '_') + '-' + item['version'] + '.dist-info/'
                metadata_names = [n for n in archive.namelist() if n.endswith('.dist-info/METADATA')]
                if metadata_names != [prefix + 'METADATA']:
                    raise HandoffError('wheel metadata identity does not match lock')
                for name in (prefix + 'METADATA', prefix + 'WHEEL'):
                    if archive.getinfo(name).file_size > 65536:
                        raise HandoffError('wheel metadata exceeds bound')
                metadata = BytesParser().parsebytes(archive.read(prefix + 'METADATA'))
                tags = BytesParser().parsebytes(archive.read(prefix + 'WHEEL'))
                if (metadata.get_all('Name') != [item['distribution']] or
                        metadata.get_all('Version') != [item['version']] or
                        metadata.get_all('Requires-Dist') or tags.get_all('Tag') != ['py3-none-any']):
                    raise HandoffError('wheel metadata/version/dependencies/tag do not match lock')
        except (zipfile.BadZipFile, KeyError, UnicodeError) as exc:
            raise HandoffError('invalid wheel metadata') from exc
        wheels.append(wheel)
    return wheels, destination


def isolated_environment():
    env = {key: value for key, value in os.environ.items()
           if key in {'PATH', 'SYSTEMROOT', 'SystemRoot', 'TMPDIR', 'TEMP', 'TMP'}}
    env.update({'PYTHONDONTWRITEBYTECODE': '1', 'PIP_CONFIG_FILE': os.devnull,
                'PIP_NO_INDEX': '1', 'PIP_DISABLE_PIP_VERSION_CHECK': '1'})
    return env


def run_checked(argv, *, cwd, label, timeout=120):
    try:
        result = subprocess.run(argv, cwd=cwd, env=isolated_environment(),
                                capture_output=True, timeout=timeout, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise HandoffError(label + ' failed or timed out') from exc
    if result.returncode:
        raise HandoffError(label + ' failed (exit ' + str(result.returncode) + ')')
    return result


def verify(wheel_dir, output):
    if sys.version_info < (3, 11):
        raise HandoffError('Python 3.11 or later is required')
    wheels, destination = validate_inputs(wheel_dir, output, load_lock())
    published = False
    with tempfile.TemporaryDirectory(prefix='.handoff 交接 ', dir=destination.parent) as temporary:
        work = Path(temporary)
        # Copy the already-validated bytes into private execution space, then
        # validate again before installation. No source checkout enters sys.path.
        private_wheels = work / 'wheels'
        private_wheels.mkdir()
        for wheel in wheels:
            shutil.copyfile(wheel, private_wheels / wheel.name)
        validate_inputs(private_wheels, work / 'unused', load_lock())
        environment = work / 'venv'
        run_checked([sys.executable, '-I', '-m', 'venv', str(environment)], cwd=work, label='fresh environment')
        python = environment / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
        run_checked([str(python), '-I', '-m', 'pip', '--isolated', 'install', '--no-index', '--no-deps',
                     *[str(private_wheels / p.name) for p in wheels]], cwd=work, label='offline wheel installation')
        fixtures = work / 'fixtures'
        shutil.copytree(FIXTURES, fixtures, ignore=shutil.ignore_patterns('evidence', '__pycache__'))
        child = fixtures / 'run_installed.py'
        reports = work / 'reports'
        reports.mkdir()
        run_checked([str(python), '-I', str(child), '--fixtures', str(fixtures), '--output', str(reports)],
                    cwd=work, label='installed handoff', timeout=120)
        if {p.name for p in reports.iterdir()} != set(REPORT_FILES):
            raise HandoffError('unexpected or missing report files')
        for name in REPORT_FILES:
            report = reports / name
            if report.is_symlink() or not report.is_file() or report.stat().st_size > MAX_REPORT_BYTES:
                raise HandoffError('report is not a bounded regular file')
            text = report.read_text(encoding='utf-8')
            if any(private in text for private in (str(work), str(ROOT), 'lease_token')):
                raise HandoffError('report contains private runtime fields or paths')
        try:
            destination.mkdir(mode=0o700)
            published = True
            for name in REPORT_FILES:
                with (destination / name).open('xb') as stream:
                    stream.write((reports / name).read_bytes())
        except BaseException:
            if published:
                shutil.rmtree(destination)
            raise


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--wheel-dir', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path, help='new directory outside source; existing trusted parent')
    args = parser.parse_args(argv)
    try:
        verify(args.wheel_dir, args.output)
    except (HandoffError, OSError, ValueError) as exc:
        print('handoff: ' + str(exc), file=sys.stderr)
        return 2
    print('Installed synthetic handoff verified; normalized reports published.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
