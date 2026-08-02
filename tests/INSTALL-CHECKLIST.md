# Install verification

Run before publishing, and again after any manifest change. A command that
returns "plugin not found" is worse than no command at all.

No install command is advertised anywhere until its box below is ticked against
the public repo.

## Local path (run first, before pushing)

- [x] `codex plugin marketplace add .` from the repo root succeeds
- [x] `codex plugin list` shows `arrakis-careers`
- [x] `codex plugin add arrakis-careers@arrakis` succeeds
- [x] The scan skill is invocable in a Codex session
- [x] `claude plugin marketplace add /absolute/path/to/repo` succeeds
- [x] `claude plugin install arrakis-careers@arrakis` succeeds
- [x] `claude plugin details arrakis-careers` lists the scan and apply components

Verified 2026-08-02 against codex-cli 0.144.1 and Claude Code 2.1.143.

The bare `codex plugin add arrakis-careers` fails with
`plugin requires --marketplace unless passed as <plugin>@<marketplace>`. The
marketplace qualifier is mandatory, so every published Codex command carries it.

Codex reads `.claude-plugin/marketplace.json` for discovery, not
`.codex-plugin/`. Both manifests are still required: the former to be found, the
latter for Codex's own metadata and its `skills` pointer.

## Public repo — Claude Code

- [ ] `/plugin marketplace add Arrakis-Security/careers`
- [ ] `/plugin install arrakis-careers@arrakis`
- [ ] `/scan` runs and produces ranked output
- [ ] `/apply` runs, shows the payload, writes the file

## Public repo — Codex

- [ ] `codex plugin marketplace add Arrakis-Security/careers`
- [ ] `codex plugin add arrakis-careers@arrakis`
- [ ] The scan runs and produces ranked output
- [ ] Apply runs, shows the payload, writes the file

## Public repo — Antigravity

- [ ] `agy plugin install https://github.com/Arrakis-Security/careers`
- [ ] `agy plugin list` shows `arrakis-careers`
- [ ] The scan runs and produces ranked output
- [ ] Apply runs, shows the payload, writes the file

Verified from a local directory against Antigravity 1.1.9: install succeeds,
`agy plugin list` reports the plugin with `"source": "gemini-cli"`, and the scan
produces correct ranked output on the empty fixture.

`agy` reads `gemini-extension.json`, so that manifest and `GEMINI.md` are
load-bearing for this platform — do not remove them as unused.

Do **not** add a `plugin.json` at the repo root. `agy plugin validate` asks for
one, but adding it makes `agy` double-count: it picks up both the `.md` and
`.toml` command files and registers `skills/shared/` as a skill. Without it,
`agy` reads the `.claude-plugin` layout and gets the correct inventory.

Gemini CLI proper is untested — we ship the manifest it would use, but no
command for it is advertised.

## Command namespace

- [ ] Confirm in a real session whether the commands are `/scan` and `/apply` or
      namespaced as `/arrakis-careers:scan` and `/arrakis-careers:apply`, and
      make `README.md` say whichever is true
