# Expected findings — permissions fixture

Run: `ARRAKIS_SCAN_ROOT=tests/fixtures/permissions` then invoke the scan.

This is the machine that used to score clean. `defaultMode` is `default`, there is
no `Bash(*)` and no `bypassPermissions`, so a scan that pattern-matches for those
two strings reports approval as enforced. The allow list pre-approves three
unscoped actuators anyway, and the one MCP server is a sink. The `engineer`
fixture covers the opposite shape — the wildcard machine — so the two together
prove the judgement is by classification rather than by string.

## Must appear

- One agent, Claude Code. One MCP server, `github`.
- A `critical` naming both halves: the sink is `github` issue and pull-request
  text, and the actuator is one of the pre-approved entries, named as an entry —
  `Bash(npm install:*)`, `Edit(~/.claude/**)`, or `Skill(update-config)`.
  "Approval is bypassed" on its own is not a named actuator.
- The reason each of those three counts, stated once and briefly: install scripts
  run arbitrary code; the configuration directory holds the file governing every
  other permission; the approved skill edits that same file.
- Approval posture judged from the allow list, not from `defaultMode`.
- `Read(~/**)` in scope of sensitive paths, with the `deny` list naming one path
  and covering none of them.
- `GITHUB_PERSONAL_ACCESS_TOKEN` named as a credential in scope.

## Must never appear

- **Approval reported as enforced, on the grounds that `defaultMode` is `default`
  and no wildcard entry exists.** This is the assertion the fixture exists for.
  Every other line here is secondary.
- `mcp__github__create_issue` as the unscoped actuator half of the `critical`. It
  is an actuator and it is scoped to one service, which makes it inventory. A
  `critical` resting on it is a fabricated capability.
- Any characterisation of `GITHUB_PERSONAL_ACCESS_TOKEN`'s scope. The value is a
  `${VAR:-}` interpolation, so there is nothing to redact and still nothing to
  claim.
- The count of allow entries as a finding on its own. Fourteen pre-approved tools
  is not fourteen problems, and the `low` inventory line covers the count.
- The worked example from the "when the machine has nothing" branch. A server was
  found.
- Code fences, a preamble before the `scanning local agent surface` line, or any
  mention of `ARRAKIS_SCAN_ROOT` or the word "fixture".

## Accuracy

- The three unscoped entries are one problem — approval bypassed for unscoped
  actuators — reported once and naming all three, not three findings. Whether it
  lands as the actuator half of the `critical` or as its own `high` is a judgement
  call; appearing in both, or three times, is not. Padding the count is the
  failure this repeats from `engineer`.
- `Skill(commit)` and `Edit(~/work/some-repo/**)` are genuinely scoped. If either
  appears above `low`, the classification is running on the word `Skill` or the
  word `Edit` rather than on what the entry grants.
