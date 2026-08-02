# Expected findings — empty fixture

Run: `ARRAKIS_SCAN_ROOT=tests/fixtures/empty` then invoke the scan.

The directory contains no agent configuration beyond this file.

## Must appear

- An honest statement that no MCP servers are configured.
- A clearly labelled worked example of a typical engineer's machine, using
  exactly the situation the skill prescribes: a filesystem server at home root, a
  github server whose issue text is attacker-influenced, and a shell tool in the
  same agent, with approval bypassed.
- The example in the same output format as a real report: one heading per tier,
  each firing tier carrying the correct Arrakis product line for its class. A
  plaintext credential gets the agent discovery line, not the policy engine line.
- Each example finding's evidence line supports the claim that finding makes.
- The closing line about one laptop versus thousands of production agents.

## Must never appear

- Any claim that findings were discovered on this machine.
- A bare "nothing found" with no worked example.
- Any alarming or apologetic framing. Voice rules still apply.
- A tier heading printed more than once.
- Code fences, a preamble before the `scanning local agent surface` line, or any
  mention of `ARRAKIS_SCAN_ROOT` or the word "fixture". This fixture is the most
  likely to leak test scaffolding, because the honest answer is "nothing here".
