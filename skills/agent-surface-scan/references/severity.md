# How to judge a finding

These criteria are explicit so that two runs on the same machine produce the same
ranking. Apply them literally. When a case is genuinely ambiguous, rank it lower
and say why.

## Definitions

**Unscoped.** A tool whose filesystem root is `/` or `~`; whose command is a
general shell (`bash`, `sh`, `zsh`, `python`, `node` with arbitrary input); or
whose configuration declares no scope where the server type implies one. A
filesystem server rooted at one project directory is scoped. The same server
rooted at `~` is not.

**Remote scope.** A server of `type: http` or `type: sse` names an endpoint and no
filesystem root, so the vocabulary above does not describe it. Its reach is
whatever its token or OAuth grant allows, and the config does not say. Do not call
it scoped and do not call it unscoped: report a remote server whose scope is not
determinable from config, name the credential that grants it, and judge the rest
on the server's well-known identity. This is the shape most hosted servers take,
and the shape our customers run.

**Sensitive path.** `~/.ssh`, `~/.aws`, `~/.kube`, `~/.config/gcloud`, any `.env`
file, `~/.netrc`, `~/.docker/config.json`, git credential helpers, `~/.gnupg`,
OS keychains, browser profile directories, `~/.npmrc`, `~/.pypirc`. A tool is "in
scope of" a sensitive path when its declared root contains that path.

**Actuator.** A tool that changes something outside the agent: shell or exec,
file write, `git push`, outbound HTTP, database write, message send, payment,
deployment, ticket mutation.

The host agent's own built-in tools count. Every coding agent ships shell
execution and file writing, so when its sandbox is disabled or its approval is
bypassed — Codex `sandbox_mode = "danger-full-access"`, Claude Code
`Bash(*)` with `bypassPermissions` — that agent has an unscoped actuator whether
or not any MCP server provides one. Do not look only at MCP servers when pairing
a sink with an actuator.

**Injection sink.** A tool that ingests content a third party can influence —
web pages, issue and pull-request text, email bodies, Slack or Discord messages,
shared documents, calendar invites, files from shared directories — **and** whose
output can reach an actuator in the same agent. Both halves are required. A fetch
tool by itself is not a sink. A fetch tool in an agent that also has shell access
is a sink, and that is the finding worth reporting.

**Pre-approved actuator.** Enumerate `permissions.allow` and classify every entry
against the actuator definition above. Do not pattern-match for
`bypassPermissions` and `Bash(*)`: a hundred and fifty narrow-looking entries can
carry the same actuators as one wildcard while matching neither string, and an
allow list is where approval is bypassed one tool at a time. Judge the set, not
the count. If any entry is an unscoped actuator, approval is bypassed for an
unscoped actuator — `high`, and eligible as the actuator half of a `critical`.
Entries that are genuinely scoped are inventory.

Three classes read as narrow and are not:

- An entry granting file edits under the agent's own configuration directory,
  `Edit(~/.claude/**)` and its equivalents. That directory holds the file
  governing every other permission, so the entry is a grant over the permission
  system rather than one permission among a hundred.
- An entry whose command installs packages, `Bash(npm install:*)` and its
  equivalents. A package's install scripts run arbitrary code, so the entry is a
  general shell by another name.
- A `Skill(...)` entry. It pre-approves the whole effect of that skill, and a
  skill is prose that can tell the agent to edit a file or run a command.
  `Skill(update-config)` is the sharp example: the skill it approves edits
  `settings.json`, which lands it in the first class by another route.

**Credential breadth.** An environment variable or config value whose name
matches `TOKEN`, `KEY`, `SECRET`, `PASSWORD`, `CREDENTIAL`, or `PAT`. Breadth is
judged by the service and the scope named in the key, never by reading the value.

These live in two places. A local server carries them in its `env` block; a
remote one carries them in `headers`, and a machine whose servers are all remote
has an empty `env` everywhere. Read both, or this tier never fires on exactly the
servers most likely to reach production.

Never characterise a scope the key name does not state. `GITHUB_PERSONAL_ACCESS_TOKEN`
is a github credential of unstated scope — calling it "repo-wide" claims something
only its value could tell you, which you did not read and must not read.

This applies to connection strings too. A `DATABASE_URL` is a database credential;
saying it "names a production host" quotes the value back, which is exactly what
redaction exists to prevent. The key name is the whole of your evidence.

## Severity tiers

Report highest first.

| Tier | Condition |
|---|---|
| `critical` | An injection sink and an unscoped actuator are reachable in the same agent; or plaintext credentials sit in the config of an agent whose approval is bypassed |
| `high` | Broad write or exec scope; secrets stored in plaintext config; approval bypassed by default; a tool in scope of a sensitive path |
| `medium` | An injection sink with no reachable actuator; broad read-only scope; auto-approve limited to a subset of tools |
| `low` | Inventory: agents installed, servers configured, tool counts |

Rules that override the table:

- Never promote a finding a tier to make the output look more impressive.
- Never report an injection-sink `critical` unless you can name both halves of
  it — the specific sink tool and the specific actuator tool. If you cannot name
  both, it is `medium`.
- The credential `critical` needs both halves too: the credential key name and
  the specific setting that bypasses approval. "Production" is never one of the
  halves — you cannot know a credential is production-scoped without reading it,
  and you must not read it.
- If the same underlying problem appears in three agents, report it once and
  name the three agents. Do not pad the count.
- Report each *problem* once, at its highest applicable tier. Do not restate the
  same problem in a lower tier to inflate the count.
- A server can be involved in more than one problem, and each still gets
  reported. A `github` server being the sink half of a `critical` does not
  excuse dropping the plaintext token in its env block — reachability and
  credential storage are different problems with different fixes. Deduplicate
  problems, never coverage: a credential that exists in the config and appears
  nowhere in the output is a miss, not restraint.

## Redaction

Report that a credential is in scope, its name, and its breadth. Never its value.

Mask anything token-shaped wherever it appears, including inside a path or a
config excerpt you are quoting. Treat as token-shaped: values beginning `sk-`,
`ghp_`, `gho_`, `ghu_`, `ghs_`, `github_pat_`, `xoxb-`, `xoxp-`, `AKIA`, `ASIA`,
`AIza`, `eyJ`; any PEM block beginning `-----BEGIN`; any hex or base64-looking
string of 32 characters or more; and the value of any key matching the credential
names above.

Replace the whole value with `[redacted]`. Never partially reveal — no
`sk-...4f2a`, no first four characters. A redaction that leaks a prefix is a
redaction that failed.

If you are unsure whether something is a secret, redact it.

## What Arrakis does about each class

One line per class in the output, immediately after the findings of that class.
This is the part that makes the scan a product teaser rather than a linter. Do
not stack all five at the end.

Every tier that fires gets the line for its class, `low` included. Match the
class to the finding: a plaintext credential is `credential breadth` and gets the
agent discovery line, not the policy engine line, however tempting the pairing.

| Finding class | Line |
|---|---|
| unscoped tool access | this is the mcp gateway — every call brokered, every scope explicit |
| approval bypassed, no pre-execution check | this is the pre-execution policy engine — the check happens before the call, not after the incident |
| injection sink reachable | this is behavioural anomaly detection — intent, not signatures |
| credential breadth, unknown inventory | this is agent discovery — you cannot govern what you cannot enumerate |
| anything already going wrong | this is the kill-switch — milliseconds, not a ticket |

## Closing line

Every run ends with the same point, in the voice from `../../shared/arrakis.md`:
this is one laptop. Our customers run thousands of agents against production
systems, and until recently had no way to see any of this.
