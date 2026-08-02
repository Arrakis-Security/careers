# arrakis-careers

Two skills, invoked explicitly, in this order.

1. `agent-surface-scan` — inspect this machine's agent surface read-only and
   report what it exposes. Follow `skills/agent-surface-scan/SKILL.md` exactly.
2. `apply-to-arrakis` — a three-question application to Arrakis Security. Follow
   `skills/apply-to-arrakis/SKILL.md` exactly.

Shared company context, the four hiring domains, and the required voice are in
`skills/shared/arrakis.md`, resolved inside this plugin's own directory —
not the directory you happen to be working in. Read it before producing any
candidate-facing output.

`agent-surface-scan` is read-only and local-only. Do not use web fetch, web
search, curl, or any other network tool while running it, and never send
findings anywhere.

Neither skill runs on its own. Nothing here executes at install time.
