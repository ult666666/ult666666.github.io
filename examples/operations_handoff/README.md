# Installed synthetic operations handoff

This source-only drill connects three released Python tools using invented bilingual community-program records. It demonstrates signed ingestion, durable duplicate detection, canonical receipts, advisory CSV preview, explicit atomic import, exact accounting, recovery and an offline recorded-output contract gate. It runs real loopback HTTP servers on port 0; it calls no model or external provider.

Python 3.11+ with venv/pip is required. The selected wheel directory must contain precisely the three regular wheels named in [release-lock.json](release-lock.json), byte-for-byte. The lock records reviewed repository/tag commits, versions, public filenames, URLs and SHA-256 values; it is configuration, not authorship proof. The verifier has no network step or source-checkout fallback.

From the repository root, with an existing trusted parent directory outside the source checkout:

```sh
python3 -B scripts/verify_handoff.py --wheel-dir /trusted/wheels --output /trusted/new-handoff-result
```

An optional separate command explicitly downloads only the fixed reviewed GitHub release URLs. It uses HTTPS, approved GitHub redirect hosts, an 8 MiB limit per wheel, a shared 60-second cooperative deadline across redirects/reads and socket waits of at most eight seconds (an in-progress OS read can finish after the deadline), then validates hashes and wheel metadata before publishing a new directory:

```sh
python3 -B scripts/fetch_handoff_wheels.py --download --output /trusted/new-wheels
```

Paths containing spaces, Unicode or leading hyphens are supported as argument values. Existing outputs, selected symlinks, foreign/missing wheels, incorrect metadata/hashes and outputs inside source or wheel inputs are refused before installation. Output parents must exist and be trusted. The launcher uses an exclusive temporary directory, installs only these three wheels with `pip --no-index --no-deps`, clears Python path overrides and runs with `-I` outside checkouts. It verifies imported distributions/modules are inside the fresh venv. Released code is trusted: this is not arbitrary-wheel isolation or a sandbox against hostile concurrent filesystem replacement.

## What the drill records

1. Two signed `{kind,csv}` deliveries carry the exact session/attendance UTF-8 bytes. The first receives 202 then 200 with stable job identity; a changed signed replay receives 409 and leaves the original intact.
2. The bounded real worker writes two canonical receipts and acknowledges two jobs. Receipt payloads and raw-body SHA-256 values match the input bytes. The actual metrics endpoint shows two persisted successes and no ready/delayed/leased/expired/dead-letter work; the read does not mutate any inbox columns. The supplied logical snapshot time is removed, and no latency is inferred.
3. A small explicit adapter extracts only `sessions` and `attendance` CSV payloads from those receipts. Each HTTP preview leaves summary and row counts unchanged; explicit HTTP imports add exactly four sessions and seven attendance rows. Repeating either import receives 400 and preserves totals.
4. Inclusive date/program filters produce October totals of 2 sessions, 3 people, 4 attendance, 7 participant-hours, 3.5 session-hours, $130.25 budget and actual, and zero variance. The equal 31-day prior window is August 31–September 30; its 2 sessions, 2 people, 3 attendance, 3.25 participant-hours, 2 session-hours, $130.10 budget and $131.00 actual yield $0.90 variance. Exact integer cents/hundredths and deltas are independently fixed in [oracle.json](oracle.json), not obtained from the production summarizer.
5. A separate-program candidate previews as valid with two new rows. A competing request imports one candidate ID, then the original two-row import is rejected atomically. Global sessions become five, attendance remains seven, and the selected-program comparison stays unchanged. Preview never reserved the IDs.
6. After the original HTTP service and synchronous worker stop, the acknowledged inbox is backed up, verified and restored through the installed RelayBox CLI to a new path. All persisted columns and state counts are compared. Physical hashes verify each respective snapshot; SQLite may alter physical bytes during a new backup. Receipt files remain separate and are not backed up by the inbox snapshot. A snapshot does not fence the old database.
7. Installed TraceBench evaluates nine `json_subset` cases against actual recorded outputs and renders JSON, Markdown and inspectable HTML. Clean reports exit 0. A deliberate one-cent mutation of recorded actual spend, compared with the clean generated baseline, exits 3 and retains failure reports. Invalid input exits 2 without publishing a report. The mutation is synthetic; this establishes an operational contract gate, not semantic model quality or an observed provider regression.

Receipt effect, CSV import and inbox acknowledgment are separate transactions. The example deliberately rejects repeated imports; it does not establish exactly-once delivery across the systems. A receipt-before-ack crash drill is outside this bounded example; RelayBox's released recovery drill covers lease recovery separately.

`participants.json` supplies fictional English/Mandarin display labels; only IDs enter the ledger, and program labels preserve Mandarin in actual imports. No contact details or production/customer data are used. The only published files are a normalized receipt, exact input/output hash manifest, recorded outputs and clean/synthetic-regression reports in [evidence/](evidence/). Databases, venv, lease capabilities, raw logs and absolute runtime paths are removed with the private execution directory. The explicit `REPORT_FILES` allowlist is also the CI artifact boundary.

Run focused tests and a fresh installed integration:

```sh
python3 -B -m unittest discover -s tests -p 'test_handoff*.py' -v
HANDOFF_WHEEL_DIR=/trusted/wheels python3 -B -m unittest discover -s tests -p test_handoff.py -v
```

The separate read-only `handoff.yml` job fetches the pinned wheels and runs the real offline drill. It has no write tokens or secrets, uses pinned Actions, and uploads only the ten explicit normalized files. The existing portfolio Pages job and exact visitor inventory are unchanged. Hosted CI evidence and publication remain separate parent review steps.

## 中文交接说明

本示例只使用虚构的中英双语社区活动数据：签名事件进入 RelayBox，重复投递返回同一任务，内容冲突返回 409；真实工作器生成标准收据后，适配器通过 Impact Ledger 的本机 HTTP 接口先预览、再明确导入。预览不锁定或保留 ID；另一请求先导入相同 ID 后，原候选文件整批拒绝，不增加部分数据。

十月数据为 2 场、3 位参与者、4 条出席记录、7 参与者小时、3.5 活动小时，预算与实际均为 130.25 美元。上期与差额在独立人工核算的 `oracle.json` 中固定，以整数分和百分之一小时核对。活动收据、CSV 导入、收件箱确认是三个事务，不保证跨系统“恰好一次”。

执行命令见上文。必须提供锁定版本的三个 wheel，输出目录必须尚不存在，父目录须可信。程序在全新临时环境离线安装，不使用源码回退。恢复前已停止原服务和工作器；数据库快照不包含单独的收据，也不会阻止旧数据库继续运行。TraceBench 对真实记录的 JSON 合约执行检查：正常为 0，故意改动一分钱后的合成回归为 3，输入错误为 2；没有模型调用或语义质量结论。仅保留规范化收据、哈希和报告，不保留数据库、密钥、租约令牌或本机绝对路径。
