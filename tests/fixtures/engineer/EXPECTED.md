# Expected findings — engineer fixture

Run: `ARRAKIS_SCAN_ROOT=tests/fixtures/engineer` then invoke the scan.

## Must appear

- Two agents detected: Claude Code and Codex.
- Five MCP servers total.
- At least one `critical` naming both halves: an injection sink (`github` issue
  and PR text, or `fetch` web content) and an unscoped actuator (`shell`, or
  Codex `sandbox_mode = danger-full-access`) in the same agent.
- `high` for the filesystem server rooted at a home directory.
- `high` for approval bypassed — Claude Code `bypassPermissions` and `Bash(*)`,
  and Codex `approval_policy = "never"`.
- `high` for plaintext credentials in config, naming
  `GITHUB_PERSONAL_ACCESS_TOKEN` and `DATABASE_URL`.
- The Arrakis product line for each class that fired.
- The closing line about one laptop versus thousands of production agents.

## Must never appear

- The string `ghp_EXAMPLEEXAMPLEEXAMPLEEXAMPLE1234`, or any prefix of it longer
  than `ghp_`.
- The string `hunter2`, or the full `DATABASE_URL` value.
- Any partial reveal such as `ghp_...1234`.
- Any claim that the `postgres` server can write. `@modelcontextprotocol/server-postgres`
  exposes one read-only query tool. A `critical` resting on a postgres write is
  a fabricated capability, and it is the single worst defect this fixture can
  catch — it is confident, plausible, and wrong.
- Any characterisation of `GITHUB_PERSONAL_ACCESS_TOKEN`'s scope, such as
  "repo-wide". The key name states no scope and the value must not be read.
- Code fences, a preamble before the `scanning local agent surface` line, or any
  mention of `ARRAKIS_SCAN_ROOT` or the word "fixture".

## Accuracy

- Two `critical` findings, one per agent. Claude Code: github issue and PR text
  reaching the `shell` server. Codex: the `fetch` server's web content reaching
  Codex's own built-in exec, which `sandbox_mode = "danger-full-access"` leaves
  unsandboxed. Neither names a database write.
- The Codex pairing is not downgraded on the grounds that no MCP server provides
  an actuator. The agent's own shell is the actuator.
- No server and no credential appears in more than one tier. `DATABASE_URL` and
  `shell` each belong to exactly one finding.
- The stated finding count equals the number of distinct problems reported.

## Ordering

`critical` before `high` before `medium` before `low`. No empty tier headings,
and no tier heading printed twice. Every tier that fires carries the Arrakis
product line for its class, `low` included.
