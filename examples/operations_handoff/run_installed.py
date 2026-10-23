"""Trusted synthetic drill. Run only through the fresh installed-wheel launcher."""
import argparse
from contextlib import contextmanager
from decimal import Decimal
import hashlib
import http.client
from importlib import import_module, metadata
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
import threading
from urllib.parse import urlencode

CLOCK = 1790812800
DEMO_KEY = b'public-synthetic-handoff-key-only'
COUNTS = {'queued': 0, 'leased': 0, 'succeeded': 2, 'dead_letter': 0}


def require(condition, contract):
    if not condition:
        raise RuntimeError('contract failed: ' + contract)


def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + '\n', encoding='utf-8')


def digest(content):
    return hashlib.sha256(content).hexdigest()


@contextmanager
def running(server):
    thread = threading.Thread(target=server.serve_forever, kwargs={'poll_interval': 0.02}, daemon=True)
    started = False
    try:
        thread.start()
        started = True
        yield server
    finally:
        try:
            if started:
                server.shutdown()
        finally:
            server.server_close()
            if started:
                thread.join(timeout=6)
                require(not thread.is_alive(), 'server thread stopped')


def request(server, method, path, body=None, headers=None):
    connection = http.client.HTTPConnection('127.0.0.1', server.server_port, timeout=6)
    try:
        connection.request(method, path, body=body, headers=headers or {})
        response = connection.getresponse()
        raw = response.read(1024 * 1024 + 1)
        require(len(raw) <= 1024 * 1024, 'bounded HTTP response')
        return response.status, json.loads(raw)
    finally:
        connection.close()


def get(server, path):
    status, result = request(server, 'GET', path)
    require(status == 200, 'GET ' + path.split('?')[0])
    return result


def rows(server):
    meta = get(server, '/api/meta')
    return {key: meta[key] for key in ('sessions', 'attendance')}


def db_rows(path):
    with sqlite3.connect(path) as connection:
        return connection.execute('SELECT * FROM jobs ORDER BY id').fetchall()


def exact(totals):
    result = {key: totals[key] for key in ('sessions', 'unique_participants', 'attendance')}
    for key, suffix in [('participant_hours', 'hundredths'), ('session_hours', 'hundredths'),
                        ('budget', 'cents'), ('actual', 'cents'), ('variance', 'cents')]:
        number = Decimal(str(totals[key])) * 100
        require(number == number.to_integral_value(), 'exact hundredths ' + key)
        result[key + '_' + suffix] = int(number)
    return result


def cli(argv, expected):
    # No shell, no provider, no source tree. Captured diagnostics stay private.
    result = subprocess.run([sys.executable, '-I', '-m', *argv], capture_output=True, timeout=25)
    require(result.returncode == expected, 'installed CLI exit ' + str(expected))
    return result


def installed(lock):
    require(sys.flags.isolated == 1 and sys.prefix != sys.base_prefix, 'isolated fresh venv')
    modules = {'relaybox': 'relaybox', 'tracebench': 'tracebench', 'impact-ledger': 'impact_ledger'}
    versions = {}
    for item in lock['wheels']:
        distribution = metadata.distribution(item['distribution'])
        module = import_module(modules[item['project']])
        require(distribution.version == item['version'], 'installed distribution version')
        require(Path(module.__file__).resolve().is_relative_to(Path(sys.prefix).resolve()), 'module inside fresh venv')
        require(Path(distribution.locate_file('')).resolve().is_relative_to(Path(sys.prefix).resolve()), 'distribution inside fresh venv')
        versions[item['project']] = item['version']
    return versions


def drill(fixtures, output):
    lock = json.loads((fixtures / 'release-lock.json').read_text(encoding='utf-8'))
    versions = installed(lock)
    from relaybox.auth import sign
    from relaybox.backup import backup_database, verify_backup
    from relaybox.server import make_server
    from relaybox.store import Inbox
    from relaybox.worker import ReceiptHandler, run_worker
    from impact_ledger.server import create_server
    from impact_ledger.store import Store

    oracle = json.loads((fixtures / 'oracle.json').read_text(encoding='utf-8'))
    records = {}
    bodies = {}
    csvs = {}
    for kind in ('sessions', 'attendance'):
        csvs[kind] = (fixtures / (kind + '.csv')).read_bytes()
        bodies[kind] = json.dumps({'kind': kind, 'csv': csvs[kind].decode('utf-8')},
                                  ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    inbox_path = Path('inbox.sqlite3')
    inbox = Inbox(inbox_path, clock=lambda: CLOCK)
    receipt_dir = Path('canonical receipts 收据')
    with running(make_server(inbox, DEMO_KEY, port=0)) as relay:
        require(get(relay, '/healthz')['status'] == 'ok', 'relay ready')
        def send(kind, changed=False):
            body = bodies[kind] if not changed else b'{"kind":"sessions","csv":"changed synthetic body"}'
            delivery = 'synthetic-' + kind
            return request(relay, 'POST', '/webhooks', body, {
                'Content-Type': 'application/json', 'X-RelayBox-ID': delivery,
                'X-RelayBox-Timestamp': str(CLOCK), 'X-RelayBox-Signature': sign(DEMO_KEY, CLOCK, delivery, body)})
        first_status, first = send('sessions')
        duplicate_status, duplicate = send('sessions')
        records['dedupe'] = {'statuses': [first_status, duplicate_status],
                             'same_job': first['job']['id'] == duplicate['job']['id'],
                             'created': [first['created'], duplicate['created']]}
        conflict_status, _ = send('sessions', changed=True)
        original = get(relay, '/api/jobs/' + str(first['job']['id']))['job']
        records['changed-replay'] = {'status': conflict_status, 'original_payload_unchanged':
                                     original['payload'] == json.loads(bodies['sessions']) and
                                     original['digest'] == digest(bodies['sessions'])}
        status, _ = send('attendance')
        require(status == 202, 'second distinct delivery')
        worker = run_worker(inbox, ReceiptHandler(receipt_dir), max_jobs=3, worker='synthetic-handoff')
        receipts = [json.loads(p.read_text(encoding='utf-8')) for p in sorted(receipt_dir.glob('*.json'))]
        payloads = {r['payload']['kind']: r for r in receipts}
        records['worker-receipts'] = {'worker': worker, 'receipts': len(receipts),
            'raw_body_hashes_match': all(payloads[k]['digest'] == digest(bodies[k]) for k in bodies),
            'payloads_match': all(payloads[k]['payload'] == json.loads(bodies[k]) for k in bodies)}
        before_metrics = db_rows(inbox_path)
        metrics = get(relay, '/api/metrics')
        metrics.pop('snapshot_at')
        metrics['read_nonmutation'] = db_rows(inbox_path) == before_metrics
        records['queue-metrics'] = metrics
    # Worker is synchronous and original HTTP service is stopped before snapshot/restore.
    snapshot = Path('acknowledged-backup.sqlite3')
    backup = backup_database(inbox_path, snapshot, timeout=5)
    verified = verify_backup(snapshot, timeout=5)
    restored_path = Path('restored inbox 新.sqlite3')
    restored_cli = cli(['relaybox', '--db', str(restored_path), 'restore', str(snapshot), '--timeout', '5'], 0)
    restored = json.loads(restored_cli.stdout)
    require(backup['sha256'] == verified['sha256'], 'snapshot verification physical hash')
    restored_verified = verify_backup(restored_path, timeout=5)
    require(restored['sha256'] == restored_verified['sha256'], 'restored file verification physical hash')
    require(all(restored[key] == verified[key] for key in ('schema_version', 'integrity', 'jobs', 'counts')),
            'restored logical metadata')
    require(inbox.stats() == COUNTS, 'acknowledged original state')
    records['restored-states'] = {key: verified[key] for key in ('schema_version', 'integrity', 'jobs', 'counts')}
    records['restored-states'].update({'all_columns_equal': db_rows(inbox_path) == db_rows(restored_path),
                                      'receipt_files_separate': len(list(receipt_dir.glob('*.json'))) == 2,
                                      'original_service_stopped': True})
    store = Store('impact.sqlite3')
    query = '?' + urlencode(oracle['filters'])
    with running(create_server(store, port=0)) as impact:
        require(get(impact, '/api/health')['status'] == 'ok', 'impact ready')
        previews = {}
        def csv_request(route, kind, content):
            return request(impact, 'POST', route + '?kind=' + kind, content, {'Content-Type': 'text/csv; charset=utf-8'})
        for kind in ('sessions', 'attendance'):
            # Explicit bounded adapter: only these two canonical receipt payloads.
            receipt = payloads[kind]
            require(set(receipt['payload']) == {'kind', 'csv'}, 'bounded receipt adapter keys')
            content = receipt['payload']['csv'].encode('utf-8')
            require(content == csvs[kind], 'receipt CSV bytes equal fixture')
            before_summary = get(impact, '/api/summary')
            before_rows = rows(impact)
            status, preview = csv_request('/api/import/preview', kind, content)
            require(status == 200, 'HTTP preview accepted')
            previews[kind] = {'valid': preview['valid'], 'rows': preview['rows'],
                              'summary_unchanged': get(impact, '/api/summary') == before_summary,
                              'rows_unchanged': rows(impact) == before_rows}
            status, imported = csv_request('/api/import', kind, content)
            require(status == 201 and imported == {'kind': kind, 'imported': preview['rows']}, 'explicit HTTP import')
        records['preview-nonmutation'] = previews
        base_rows = rows(impact)
        current = get(impact, '/api/summary' + query)
        require(current['filters'] == oracle['filters'], 'selected summary filters')
        current_exact = exact(current['totals'])
        require(base_rows == oracle['base_rows'], 'independent fixture row counts')
        require(current_exact == oracle['current_exact'], 'independent current accounting oracle')
        comparison = get(impact, '/api/comparison' + query)
        comparison_record = {'days': comparison['days'], 'previous_start': comparison['previous']['start'],
                             'previous_end': comparison['previous']['end'], 'current_exact': exact(comparison['current']['totals']),
                             'prior_exact': exact(comparison['previous']['totals']), 'deltas_exact': exact(comparison['deltas'])}
        for key in ('current_exact', 'prior_exact', 'deltas_exact'):
            require(comparison_record[key] == oracle[key], 'independent comparison oracle ' + key)
        require(comparison_record['days'] == oracle['prior_window']['days'] and
                comparison_record['previous_start'] == oracle['prior_window']['start'] and
                comparison_record['previous_end'] == oracle['prior_window']['end'], 'equal inclusive previous window')
        records['comparison'] = comparison_record
        before_duplicate = get(impact, '/api/summary')
        duplicate_statuses = [csv_request('/api/import', k, csvs[k])[0] for k in ('sessions', 'attendance')]
        inclusive = {}
        for day in oracle['inclusive_days']:
            selected = get(impact, '/api/summary?' + urlencode({'start': day, 'end': day, 'program': oracle['program']}))
            inclusive[day] = [row['session_id'] for row in selected['sessions']]
        other = get(impact, '/api/summary?' + urlencode({'program': 'Different program / 其他项目'}))
        records['import-totals'] = {'base_rows': base_rows, 'current_exact': current_exact,
                                    'duplicate_statuses': duplicate_statuses,
                                    'duplicate_totals_unchanged': get(impact, '/api/summary') == before_duplicate,
                                    'inclusive_dates': inclusive, 'other_program_sessions': other['totals']['sessions']}
        header = csvs['sessions'].split(b'\n', 1)[0] + b'\n'
        taken = 'race-taken,Advisory Drill / 预览演练,2026-10-20,1.00,1.00,1.00\n'.encode('utf-8')
        fresh = 'race-fresh,Advisory Drill / 预览演练,2026-10-21,1.00,1.00,1.00\n'.encode('utf-8')
        candidate = header + taken + fresh
        before_race = rows(impact)
        status, preview = csv_request('/api/import/preview', 'sessions', candidate)
        require(status == 200, 'advisory candidate preview')
        competing_status, competing = csv_request('/api/import', 'sessions', header + taken)
        require(competing_status == 201, 'competing HTTP import')
        after_competing = get(impact, '/api/summary')
        original_status, _ = csv_request('/api/import', 'sessions', candidate)
        after_race = rows(impact)
        records['advisory-race'] = {'preview_valid': preview['valid'], 'candidate_rows': preview['rows'],
            'competing_imported': competing['imported'], 'original_status': original_status,
            'global_rows_before': before_race, 'global_rows_after': after_race,
            'atomic_rejection': get(impact, '/api/summary') == after_competing and
                                'race-fresh' not in [s['session_id'] for s in after_competing['sessions']],
            'selected_program_comparison_unchanged': get(impact, '/api/comparison' + query) == comparison}
        require(after_race == oracle['post_race_rows'], 'race row oracle')
    # TraceBench evaluates these recorded product outputs against source-reviewed
    # literals, never a model or a production-generated expected answer.
    cases = fixtures / 'cases.jsonl'
    order = [json.loads(line)['id'] for line in cases.read_text(encoding='utf-8').splitlines()]
    require(set(order) == set(records), 'contract coverage')
    def write_outputs(path, source):
        path.write_text(''.join(json.dumps({'id': key, 'output': source[key]}, ensure_ascii=False,
                                          sort_keys=True, separators=(',', ':')) + '\n' for key in order), encoding='utf-8')
    actual = output / 'outputs.jsonl'
    write_outputs(actual, records)
    for fmt, extension in [('json', 'json'), ('markdown', 'md'), ('html', 'html')]:
        cli(['tracebench', 'evaluate', '--cases', str(cases), '--outputs', str(actual), '--format', fmt,
             '--report', str(output / ('clean.' + extension))], 0)
    mutation = json.loads(json.dumps(records))
    mutation['import-totals']['current_exact']['actual_cents'] = 13024
    mutated = output / 'synthetic-regression-outputs.jsonl'
    write_outputs(mutated, mutation)
    for fmt, extension in [('json', 'json'), ('markdown', 'md'), ('html', 'html')]:
        cli(['tracebench', 'evaluate', '--cases', str(cases), '--outputs', str(mutated),
             '--baseline', str(output / 'clean.json'), '--format', fmt,
             '--report', str(output / ('synthetic-regression.' + extension))], 3)
    invalid = Path('invalid synthetic outputs.jsonl')
    invalid.write_text('{"id":"invalid","output":', encoding='utf-8')
    invalid_report = Path('must-not-publish-invalid.json')
    cli(['tracebench', 'evaluate', '--cases', str(cases), '--outputs', str(invalid), '--report', str(invalid_report)], 2)
    require(not invalid_report.exists(), 'invalid input publishes no report')
    dump(output / 'handoff-receipt.json', {
        'schema_version': 1, 'synthetic': True, 'installed_versions': versions,
        'installed_modules_verified_inside_fresh_venv': True,
        'tracebench_exit_codes': {'clean': 0, 'synthetic_regression': 3, 'invalid_input': 2},
        'synthetic_mutation': {'case': 'import-totals', 'field': 'current_exact.actual_cents', 'from': 13025, 'to': 13024,
                               'notice': 'Deliberate recorded-output mutation, not an observed provider regression.'},
        'canonical_receipts': sorted(receipts, key=lambda receipt: receipt['delivery_id']),
        'transaction_boundaries': ['receipt effect', 'CSV import', 'inbox acknowledgment'],
        'limitations': ['Bounded synthetic adapter with explicit duplicate rejection; no exactly-once distributed pipeline.',
                        'Queue snapshot time is supplied logical time, not measured latency.',
                        'Acknowledged inbox snapshot excludes receipt files and does not fence the old database.',
                        'TraceBench checks recorded JSON contracts; no model calls or semantic quality claim.']})
    names = ('sessions.csv', 'attendance.csv', 'participants.json', 'oracle.json', 'cases.jsonl', 'release-lock.json')
    dump(output / 'fixture-hashes.json', {
        'algorithm': 'sha256', 'inputs': {name: digest((fixtures / name).read_bytes()) for name in names},
        'wheels': {item['filename']: item['sha256'] for item in lock['wheels']},
        'outputs': {p.name: digest(p.read_bytes()) for p in sorted(output.iterdir())}})


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fixtures', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    drill(args.fixtures, args.output)
