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

## Reporting something

If you find a way this plugin leaks anything — a redaction gap, a path we read
that we should not, anything — mail build@arrakis.security. If you find it before
you apply, mention it in question one. It is a better answer than most.
