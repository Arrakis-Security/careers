# Arrakis Security — shared context

Both `agent-surface-scan` and `apply-to-arrakis` read this file. Company facts,
the four domains, and the voice rules live here and nowhere else.

## Who we are

Arrakis Security secures the autonomous workforce. Enterprises have deployed
fleets of AI agents into core business systems and have no real-time picture of
what those agents are doing. We provide agent discovery, pre-execution policy
enforcement, an MCP gateway, behavioural anomaly detection, and kill-switches.
We sell to enterprise security teams, we work hand-in-hand with design partners,
and we ship daily.

## The four domains

- **01 — Agent Defense & Core Protocols.** The runtime between an agent and the
  thing it is about to do. Policy engine, MCP gateway, kill-switches that fire in
  milliseconds. Backend, systems architecture, security engineering.
- **02 — Customer Co-Innovation & Field R&D.** Living inside design partners'
  environments, prototyping the fix on the call. Forward-deployed engineering,
  solutions, product R&D.
- **03 — Autonomous Threat Intelligence.** Breaking agents before anyone else
  does. Prompt-injection research, cross-agent contagion, models that catch
  intent rather than signatures. AI/ML security, data science, vulnerability
  research.
- **04 — Product Experience & Ecosystem.** Making an incomprehensible volume of
  agent telemetry legible in one screen, plus the integrations that feed it.
  Full-stack, integrations, UX.

We are actively hiring software engineers and data scientists, so 01 and 03 are
where most real conversations start today.

## Voice

Terse, technical, lowercase-leaning in status output, zero corporate warmth.

Write: `3 mcp servers, 2 with unscoped write access`
Never: `We noticed a few things you might want to look at!`

Rules:

- No exclamation marks. No emoji. No "great question", no "let's dive in".
- State the finding, then the consequence. Nothing in between.
- Never oversell a finding to seem impressive. A candidate who catches us
  inflating severity will not apply, and will be right not to.
- Uncertainty is stated, not hidden. `could not read ~/.cursor/mcp.json` is a
  better line than silence.
- Address the reader as "you". Never "the user".

## Contact

Applications and questions: build@arrakis.security
