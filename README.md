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

The Claude Code command is verified against this repository — not a local
checkout — on 2026-08-06, Claude Code 2.1.143. The Codex and Antigravity
commands come from testing against a local checkout and have not been re-run
against the public repository. We would rather name the gap than let a command
that returns "plugin not found" be your first impression. If one fails for you,
mail build@arrakis.security and we will fix it fast.

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

## Why you can trust what you install

You are being asked to run instructions against your own credential stores by a
company you may not know. That deserves infrastructure, not assurances.

- **Nobody outside Arrakis Security can approve a change here.** Every path is
  owned in [.github/CODEOWNERS](.github/CODEOWNERS), code-owner review is
  required on the default branch, and the ruleset has no bypass list. Outside
  contributions are welcome and arrive as pull requests from forks.
- **Every pull request is machine-checked before a human sees it.**
  [scripts/check_content_safety.py](scripts/check_content_safety.py) fails any new
  line in the prompt surface that touches a network verb, a secret path, a shell,
  or an instruction override until a maintainer records that exact line. It also
  rejects invisible characters, lookalike letters, and base64 blobs — the shapes a
  malicious contribution takes in a repository made of prose.
- **`SUBMIT_ENABLED = false` is enforced by CI**, not by convention.
- **Signed commits, linear history, signed release tags**, and installs you can
  pin to a tag: [docs/RELEASING.md](docs/RELEASING.md).
- **The threat model is written down**, including the attacks we think are most
  likely against this repository specifically:
  [docs/THREAT-MODEL.md](docs/THREAT-MODEL.md).

Run our own guardrail on your clone before you install, if you like:

```bash
git clone --depth 1 https://github.com/Arrakis-Security/careers && cd careers
python3 scripts/check_content_safety.py
```

## Contributing

Pull requests welcome, including from outside. Read
[CONTRIBUTING.md](CONTRIBUTING.md) first — the constraint is that markdown here is
executable, so review is line by line and only staff can merge.

Security defects go to
[private reporting](https://github.com/Arrakis-Security/careers/security/advisories/new)
or build@arrakis.security, never a public issue.

## Who we are

Arrakis Security secures the autonomous workforce. Agent discovery,
pre-execution policy enforcement, an MCP gateway, behavioural anomaly detection,
and kill-switches — for enterprises whose AI agents are already inside core
business systems.

We are hiring across four domains, listed in
[skills/shared/arrakis.md](skills/shared/arrakis.md). Software engineers and
data scientists first.

build@arrakis.security
