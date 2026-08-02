# arrakis-careers

Two commands, in this order.

1. `/scan` — inspect this machine's agent surface read-only and report what it
   exposes. Follow `skills/agent-surface-scan/SKILL.md` exactly.
2. `/apply` — a three-question application to Arrakis Security. Follow
   `skills/apply-to-arrakis/SKILL.md` exactly.

Shared company context, the four hiring domains, and the required voice are in
`skills/shared/arrakis.md`, resolved inside this plugin's own directory —
not the directory you happen to be working in. Read it before producing any
candidate-facing output.

`scan` is read-only and local-only. Do not use web fetch, web search, curl, or
any other network tool while running it, and never send findings anywhere.
