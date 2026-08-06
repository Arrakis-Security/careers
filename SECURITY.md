# Security

This plugin is made by a security company and read by security people. Here is
exactly what it does, in plain language.

## What `scan` does

It reads configuration files already on your machine — which coding agents you
have installed, which MCP servers they are configured with, what those servers
can reach, and whether tool calls are auto-approved. Then it prints a summary.

## The one thing you should understand before running it

This plugin has no code. It is instructions your own coding agent follows. So
when `scan` reads `~/.claude.json` or `~/.codex/config.toml`, those files enter
your agent's context and go to whichever model provider you are already using —
Anthropic, OpenAI, Google — exactly as they would if you asked your agent to read
any other file. Your agent will also write its session transcript to disk the way
it always does.

Agent config files are among the densest credential stores on a developer's
machine. If yours holds API keys in plaintext `env` blocks, running `scan` sends
them to your model provider. We think that is worth knowing before you type the
command, and we would rather say it than have you find it.

What we mean by local-only is narrower and precise: **this plugin adds no
transmission of its own, and nothing reaches Arrakis.** There is no endpoint, no
telemetry, no analytics, no "anonymous usage data". We never see your findings.

If that trade is not one you want to make, do not run `scan`. `apply` alone is a
complete application and reads nothing but your git config.

## What `scan` does not do

- **It sends nothing to Arrakis.** No endpoint, no telemetry, no findings upload.
- **It never prints secret values.** If a credential is in scope, you get its
  name and its breadth. Never its content, and never a partial reveal.
- **It writes nothing itself.** No file on your machine is created, modified, or
  deleted by the scan's instructions. Your agent's own transcript logging is
  outside our control and happens on every session you run.
- **It never opens secret stores.** It does not read `.env` files, key files, or
  anything under `~/.ssh`. That those paths are *reachable* is the finding; their
  contents are not.

## What is transmitted, ever

One thing: your application. The three answers, the optional domain, and your
contact details — and only after you have seen the exact payload on screen and
said yes.

Scan findings are never attached to an application. Not summarised, not
anonymised, not "just the counts".

Submission is currently switched off. Your application is written to a file in
your working directory and you mail it to build@arrakis.security. When the
endpoint goes live, the confirmation step stays exactly as it is.

## No background anything

No post-install hooks. No background execution. No network calls at install time.
Nothing in this plugin runs until you explicitly invoke a command.

## How to verify all of this

Read it. This plugin is prose in a public repository — there is no compiled
binary, no minified bundle, no hidden module. The scan is a few hundred lines of
markdown in `skills/agent-surface-scan/`. Every instruction your agent will
follow is in there, in English.

We would rather you check than trust us. Checking takes about two minutes:

```bash
grep -rniE "curl|wget|http|upload|telemetry|POST" skills/ commands/
```

You will get a handful of hits. Every one is either a prohibition, a definition
of something the scan looks for on your machine, or the single line in
`skills/apply-to-arrakis/SKILL.md` that would submit your application — guarded
by `SUBMIT_ENABLED = false`, which is what makes the mailto fallback the only
path today. If you find a hit that is none of those, you have found a defect and
we want to hear about it.

For the scan specifically, the narrower check is the honest one:

```bash
grep -rniE "curl|wget|http|POST|upload" skills/agent-surface-scan/
```

Five hits, and none is an instruction to transmit: one prohibition, one
definition of "outbound HTTP" as a capability we look for in *your* config, and
three substring false positives — `POST` inside "approval **post**ure" and
"**post**gres".

## Who can change what you install

Reading the repository tells you what it says today. What stops it saying
something else tomorrow is separate, so here it is:

- Installs resolve to this repository's default branch, so what is on `main` is
  what runs. Only Arrakis Security staff can approve a merge to it — every path is
  owned in [.github/CODEOWNERS](.github/CODEOWNERS), code-owner review is
  required, and the branch ruleset has no bypass list. Outside contributions
  arrive as pull requests from forks and are reviewed line by line.
- Commits on `main` are signed, history is linear, force-pushes and branch
  deletion are blocked, and release tags cannot be moved once published.
- Every pull request runs
  [scripts/check_content_safety.py](scripts/check_content_safety.py), which fails
  any new line in the prompt surface that mentions a network verb, a secret store
  path, a shell, or an instruction override until a maintainer records that exact
  line by hash. It also rejects invisible characters, non-Latin lookalikes, and
  base64 blobs. `SUBMIT_ENABLED = false` is one of the invariants it enforces, so
  switching submission on cannot happen quietly.
- Our own threat model, including what we think the most likely attack on this
  repository is, is in [docs/THREAT-MODEL.md](docs/THREAT-MODEL.md). The exact
  GitHub settings behind the paragraphs above are listed in
  [docs/GITHUB-SETTINGS.md](docs/GITHUB-SETTINGS.md), so you can check that we
  described them honestly.

To pin rather than track `main`, install from a signed tag —
[docs/RELEASING.md](docs/RELEASING.md) has the clone-and-verify commands.

## One thing the scan hardens against, because we sell the fix

`scan` reads project-level config from the directory you are standing in. If that
repository is not yours, those files are attacker-controlled input to your agent.
The skill's fifth absolute rule says config content is data to be reported on and
never instruction to be followed, and that a config file carrying instructions is
itself a `critical` finding. A company selling prompt-injection defence whose own
skill follows an injected instruction would have nothing to sell.

## Reporting something

If you find a way this plugin leaks anything — a redaction gap, a path we read
that we should not, anything — use
[private vulnerability reporting](https://github.com/Arrakis-Security/careers/security/advisories/new)
or mail build@arrakis.security. Please do not open a public issue for a leak.

We acknowledge within two business days and tell you what we are doing about it.
If you find it before you apply, mention it in question one. It is a better answer
than most.
