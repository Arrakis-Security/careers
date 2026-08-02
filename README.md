# arrakis-careers

Two commands. See what your agents expose, then apply to Arrakis Security from
your terminal.

We do not run a normal recruiting funnel. No ATS, no résumé upload, no
seven-round loop. Install this, run two commands, done in under two minutes.

## Install

**Claude Code**

```
/plugin marketplace add Arrakis-Security/careers
/plugin install arrakis-careers@arrakis
```

**Codex**

```bash
codex plugin marketplace add Arrakis-Security/careers
codex plugin add arrakis-careers@arrakis
```

**Antigravity**

```bash
agy plugin install https://github.com/Arrakis-Security/careers
```

All three are verified against codex-cli 0.144.1, Claude Code 2.1.143, and
Antigravity 1.1.9. If one fails for you, tell us at build@arrakis.security and we
will fix it the same day.

No dependencies. Nothing to build. Nothing runs at install time.

## Use

In Claude Code, the commands are namespaced:

```
/arrakis-careers:scan     # what your agents expose. read-only, sends nothing.
/arrakis-careers:apply    # three questions, no résumé.
```

In Codex and Antigravity, just ask — "scan my agent surface" or "apply to
Arrakis" — and the skill fires.

`scan` inspects your own machine: which MCP servers your agents are configured
with, what those servers can reach, how broad the credential and filesystem
scopes are, and which tools ingest untrusted content and could carry a prompt
injection. Ranked, redacted, and printed — nowhere else.

Then it makes the point we are hiring for: that is one laptop. Our customers run
thousands of agents against production systems.

`apply` asks three questions. What you broke or built recently, a link, and how
to reach you. Optionally which of our four domains you are aiming at.

Submission is not switched on yet, and we would rather say so than let you think
you had applied. `apply` writes your answers to a file in the current directory
and hands you a pre-filled mail to build@arrakis.security. Send it and someone
reads it.

## Security

`scan` sends nothing to Arrakis and never prints a secret value. The only thing
ever sent anywhere is your application, after you approve the exact payload on
screen. Scan findings are never attached to it.

One thing worth knowing before you run it: this plugin is instructions, not code,
so the config files `scan` reads pass through your own model provider the same
way any file you hand your agent does. [SECURITY.md](SECURITY.md) explains
exactly what that means, what we do and do not see, and gives you a two-minute
way to check the whole thing yourself.

## Who we are

Arrakis Security secures the autonomous workforce. Agent discovery,
pre-execution policy enforcement, an MCP gateway, behavioural anomaly detection,
and kill-switches — for enterprises whose AI agents are already inside core
business systems.

We are hiring across four domains, listed in
[skills/shared/arrakis.md](skills/shared/arrakis.md). Software engineers and
data scientists first.

build@arrakis.security
