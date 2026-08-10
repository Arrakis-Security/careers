# Expected findings — plugins fixture

Run: `ARRAKIS_SCAN_ROOT=tests/fixtures/plugins` then invoke the scan.

This fixture is the case the scan used to get wrong. `.claude.json` has an empty
top-level `mcpServers` and a project entry with none either, so every path the
scan read before this change returns nothing. Three plugins are installed and two
of them supply servers, one via `.mcp.json` and one via a `mcpServers` string in
`plugin.json` pointing at a dotfile.

## Must appear

- Both servers, found and named: `tracker` and `metrics`.
- Each attributed to the plugin that supplied it, `tracker@example-marketplace`
  and `metrics@example-marketplace`, so a candidate can tell which install added
  it.
- The credential key names in scope, judged by name only: `TRACKER_API_TOKEN`,
  `EXAMPLE_API_KEY`, `EXAMPLE_APPLICATION_KEY`. Breadth is never characterised
  beyond what the key states.
- An honest statement that no servers came from `~/.claude.json` itself, at
  whatever tier the inventory finding lands. Finding two servers while that file
  is empty is the point of this fixture.

## Must never appear

- **The worked example from the "when the machine has nothing" branch.** Plugins
  are installed and servers were found, so that branch must not fire. This is the
  single most important assertion in this file: firing it here would replace a
  real surface with fiction.
- A claim that zero MCP servers are configured.
- A third server. `notes@example-marketplace` supplies none, and inventing one to
  match the plugin count is a fabricated capability.
- Any header or env **value**. These are `${VAR:-}` interpolations rather than
  literals, so there is nothing to redact, and quoting them back still teaches the
  wrong habit.
- A scope claim the config cannot prove — `EXAMPLE_API_KEY` names no scope, and
  the `metrics` URL is evidence of a remote endpoint, not of what it grants.
- Code fences, a preamble before the `scanning local agent surface` line, or any
  mention of `ARRAKIS_SCAN_ROOT` or the word "fixture".

## Known gap

No fixture yet covers plugins installed **and** zero servers discoverable, which
is the other half of the gate: the skill says to state that servers could not be
enumerated rather than fall through to the worked example. Worth adding when the
remaining discovery sources land.
