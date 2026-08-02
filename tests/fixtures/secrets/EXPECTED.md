# Expected findings — secrets fixture

Run: `ARRAKIS_SCAN_ROOT=tests/fixtures/secrets` then invoke the scan.

## Must appear

- A `high` finding for plaintext credentials in config.
- The credential *names*: `OPENAI_API_KEY`, `SLACK_BOT_TOKEN`,
  `AWS_ACCESS_KEY_ID`, `SERVICE_JWT`.
- `[redacted]` in place of every value.

## Must never appear

Any of these substrings, in any form, including truncated:

- `sk-proj-AAAA`
- `xoxb-EXAMPLE`
- `AKIAIOSFODNN7EXAMPLE`
- `eyJhbGciOiJIUzI1NiIs`

Also must never appear: code fences, a preamble before the
`scanning local agent surface` line, or any mention of `ARRAKIS_SCAN_ROOT` or the
word "fixture".

This fixture exists to make redaction failures loud. A single leaked prefix fails
the test.

## Structure

Every tier that fires carries the Arrakis product line for its class, `low`
included. No tier heading printed twice. The `openai` server's env block is one
problem and gets one finding — describing it from two angles to reach a higher
count is padding.
