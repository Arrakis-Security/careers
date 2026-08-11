# Where agent configuration lives

Read every path that exists. A missing path is normal and silent — most machines
have two or three of these, not all of them. Never create, modify, or delete any
file listed here.

If `ARRAKIS_SCAN_ROOT` is set, resolve every `~` below under that directory
instead of the real home directory. This exists so the fixtures in `tests/` can
be scanned; candidates never set it.

## MCP server configuration

| Agent | Paths | Shape |
|---|---|---|
| Claude Code | `~/.claude.json`, `./.mcp.json`, and every plugin listed in `~/.claude/plugins/installed_plugins.json` | JSON — see below, neither shape is what you expect |
| Claude Desktop | macOS `~/Library/Application Support/Claude/claude_desktop_config.json`, Linux `~/.config/Claude/claude_desktop_config.json`, Windows `%APPDATA%\Claude\claude_desktop_config.json` | JSON, key `mcpServers` |
| Codex | `~/.codex/config.toml` | TOML, tables `[mcp_servers.NAME]` |
| Cursor | `~/.cursor/mcp.json`, `./.cursor/mcp.json` | JSON, key `mcpServers` |
| Gemini CLI | `~/.gemini/settings.json`, `./.gemini/settings.json` | JSON, key `mcpServers` |
| Windsurf | `~/.codeium/windsurf/mcp_config.json` | JSON, key `mcpServers` |
| VS Code | macOS `~/Library/Application Support/Code/User/mcp.json`, Linux `~/.config/Code/User/mcp.json`, Windows `%APPDATA%\Code\User\mcp.json`, plus `./.vscode/mcp.json` | JSON, key `servers` or `mcp.servers` |

### `~/.claude.json` has two levels, and the one people actually use is nested

Do not read only the top-level `mcpServers` key. `claude mcp add` defaults to
**local** scope, which writes to `projects["<absolute project path>"].mcpServers`,
not to the top level. Only `claude mcp add -s user` writes the top-level key. On a
real machine the top-level key is often absent entirely while a dozen projects
each carry their own servers.

Read both. Report project-scoped servers with the project they belong to. A scan
that checks only the top level will tell a candidate they have no MCP servers
while their agent is running six, which is the one thing this scan must never do.

Also read, per project: `enabledMcpjsonServers` and `disabledMcpjsonServers`. A
server listed in `./.mcp.json` but named in `disabledMcpjsonServers` is not live,
and reporting it as live is a false positive.

This file is large — commonly thousands of lines, since it also holds session
history. If your read is truncated, say so in the output and give the counts you
can stand behind. Never present a partial read as a complete inventory.

Project-level paths (`./.mcp.json`, `./.cursor/mcp.json`, `./.vscode/mcp.json`,
`./.gemini/settings.json`) are read relative to the current working directory
only. Do not walk the filesystem looking for more.

### Servers that arrive with a plugin, which `~/.claude.json` never mentions

`~/.claude.json` records servers added with `claude mcp add`. It says nothing
about servers an installed plugin brings with it, and those are frequently the
only ones on the machine. Skipping this source is how a scan reports zero servers
to a candidate whose agent is running four.

Read, in order:

1. `~/.claude/plugins/installed_plugins.json`. Shape is
   `{"version": 2, "plugins": {"<name>@<marketplace>": [{"installPath": "…"}]}}`.
   One plugin can hold several entries; each has its own `installPath`.
2. For each `installPath`, read `<installPath>/.mcp.json`, key `mcpServers`.
3. Also read `<installPath>/.claude-plugin/plugin.json`. Its `mcpServers` is
   either the server object itself, **or a string naming another file** to read
   relative to `installPath` — `"./.dd_claude-code_mcp.json"` is a real example.
   A plugin may use both this and `.mcp.json`; merge what you find.

Attribute each server to the plugin it came from, so a candidate can tell which
of their installs added it. An empty top-level `mcpServers`, no project-scoped
servers, and several live plugin servers is the ordinary shape of a stock
install, not an edge case.

An absolute `installPath` is used as written. A relative one resolves under the
same root as the `~` paths above, which is how a fixture keeps its plugin tree
inside itself.

## Approval and sandbox posture

| Agent | Path | What to read |
|---|---|---|
| Claude Code | `~/.claude/settings.json`, `~/.claude/settings.local.json`, `./.claude/settings.json`, `./.claude/settings.local.json` | `permissions.allow`, `permissions.deny`, `permissions.defaultMode`, `enableAllProjectMcpServers` |
| Codex | `~/.codex/config.toml` | `approval_policy`, `sandbox_mode`, `sandbox_permissions`, trusted project entries |
| Cursor | `~/.cursor/mcp.json` and Cursor settings | auto-run / auto-approve toggles |
| Gemini CLI | `~/.gemini/settings.json` | `autoAccept`, approval mode |
| Windsurf | `~/.codeium/windsurf/mcp_config.json` | per-server auto-approve lists |

Values that mean approval is off: Claude Code `defaultMode` of
`bypassPermissions` or `acceptEdits`; a `permissions.allow` entry of `Bash(*)`,
`Bash`, or `*`; Codex `approval_policy = "never"`; Codex
`sandbox_mode = "danger-full-access"`; Gemini `autoAccept: true` or an approval
mode of `yolo`.

Those are the unambiguous ones, not the whole test. `severity.md` says how to
judge the rest of `permissions.allow`, entry by entry. An allow list containing
none of the strings above is not thereby a clean one.

## Which agents are installed

Presence alone is a low-severity inventory finding. Check for the directories
`~/.claude`, `~/.codex`, `~/.cursor`, `~/.gemini`, `~/.codeium/windsurf`, and for
the config paths above. Do not run version commands; reading is enough.

## Reading rules

- Read-only. Never write.
- Parse what you can. If a file is malformed or unreadable, say so in the output
  and continue — one bad file does not abort the scan.
- Do not follow symlinks outside the home directory.
- Do not read the contents of `.env` files, key files, or anything under `~/.ssh`.
  Their *existence and reachability* is the finding. Their contents are not.
- Read the keys you need, not whole files, where the format lets you. These
  configs can be megabytes.
- If any read was truncated or any path was unreadable, say so in the output.
  Silence implies completeness, and an inventory that quietly missed something is
  worse than one that admits a gap.
