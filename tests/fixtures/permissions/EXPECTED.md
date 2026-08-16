# Expected findings — permissions fixture

Run: `ARRAKIS_SCAN_ROOT=tests/fixtures/permissions` then invoke the scan.

The machine that used to score clean. `defaultMode` is `default` and there is no
`Bash(*)` and no `bypassPermissions`, so a scan matching those two strings reports
approval as enforced. The allow list pre-approves three unscoped actuators anyway,
and the one MCP server is a sink. `engineer` covers the wildcard shape, so the two
together prove the judgement is by classification rather than by string.

## Must appear

- One agent, Claude Code. One MCP server, `github`.
- A `critical` naming both halves: `github` issue and pull-request text as the
  sink, and a named allow entry as the actuator — `Bash(npm install:*)`,
  `Edit(~/.claude/**)`, or `Skill(update-config)`. "Approval is bypassed" on its
  own is not a named actuator.
- Approval posture judged from the allow list, not from `defaultMode`.
- `Read(~/**)` in scope of sensitive paths, with `deny` covering none of them.
- `GITHUB_PERSONAL_ACCESS_TOKEN` named as a credential in scope.

## Must never appear

- **Approval reported as enforced because `defaultMode` is `default` and no
  wildcard exists.** This is the assertion the fixture exists for.
- `mcp__github__create_issue` as the unscoped actuator half of the `critical`. It
  is an actuator scoped to one service, which makes it inventory.
- Any characterisation of `GITHUB_PERSONAL_ACCESS_TOKEN`'s scope.
- The allow-list count as a finding on its own.
- The worked example from the "when the machine has nothing" branch — a server
  was found.
- Code fences, a preamble before the `scanning local agent surface` line, or any
  mention of `ARRAKIS_SCAN_ROOT` or the word "fixture".

## Accuracy

- The three unscoped entries are one problem, reported once and naming all three.
  Whether it lands as the actuator half of the `critical` or as its own `high` is
  a judgement call; appearing in both is not.
- `Skill(commit)` and `Edit(~/work/some-repo/**)` are genuinely scoped. Either one
  above `low` means the classification is running on the word `Skill` or `Edit`
  rather than on what the entry grants.
