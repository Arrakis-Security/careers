# Contributing

Pull requests are welcome, including from people who do not work here. Read this
first — it is short, and it explains a constraint that is unusual.

## What this plugin is for

A taste of what Arrakis does, built to interest people in working here. It is not
agent governance and completeness is not the goal, which rules more out than it
sounds like:

- **Two jobs: add what is genuinely missing, and make what we claim match what we
  do.** A change that does neither is out of scope however good it is.
- **A mismatch can be fixed from either end, and the claim is usually the cheaper
  one.** Growing the plugin to satisfy a promise we did not need to make is how
  scope escapes.
- **The run stays short.** Every source added means more reads, more findings, and
  more output. Length is a defect here, not thoroughness.
- **Nothing proprietary ships.** This repository is public and the detection
  method is the asset.
- **Admitting a gap beats covering it.** Saying plainly what we read, what we
  cannot see, and what never leaves the machine is the point, and it costs no
  runtime.

## The constraint

This repository contains no code. It contains instructions that a candidate's own
coding agent follows on their own laptop, with access to their agent
configuration. A one-line change to a markdown file here is a change to what runs
on somebody else's machine.

So we review contributions the way we would review a patch to a privileged
binary, and:

- **Only Arrakis Security staff can approve and merge.** Every path is owned in
  [`.github/CODEOWNERS`](.github/CODEOWNERS), code-owner review is required, and
  nobody — including us — bypasses it. This is not a comment on contributors. It
  is that the blast radius of a merge here is other people's laptops.
- **Contribute from a fork.** Nobody outside the org has push access, and we do
  not hand out write access to move faster.
- **Small and single-purpose gets merged.** A pull request that changes one thing
  and says what it changes can be reviewed line by line, which is the only review
  that means anything for prose that executes.

## Before you open a pull request

```bash
python3 scripts/validate_manifests.py     # manifests, versions, links
python3 scripts/check_tree.py             # text only, no binaries or symlinks
python3 scripts/check_content_safety.py   # the prompt surface
```

All three run in CI on your pull request. They need nothing but Python 3.

`check_content_safety.py` will fail on any line that mentions a network verb, a
secret path, a shell, or an instruction override — including lines that *prohibit*
those things, which is most of the existing ones. That is deliberate. Every such
line is recorded in [`.github/allowed-lines.txt`](.github/allowed-lines.txt) by
the hash of its exact text *and the file it appears in*, so rewording one — or
moving it to another skill — puts it back in front of a human. The check reads
every file under `skills/` and `commands/`, not just the markdown ones. If your
change is legitimate, run:

```bash
python3 scripts/check_content_safety.py --hashes
```

and add the printed lines to the allowlist **in the same pull request**, so the
reviewer sees the sentence and its hash together.

## What will not be merged

- Any instruction to make a network call, fetch a URL, or send findings anywhere
- Any widening of what the scan reads, or any read of the *contents* of a secret
  store — `.env`, key files, `~/.ssh`, keychains. That those paths are reachable
  is the finding; their contents are never ours to look at
- Any weakening of redaction, including partial reveals. `sk-...4f2a` is a leak
- `SUBMIT_ENABLED = true`, or any endpoint, key, token, or hostname
- Invisible characters, bidi controls, non-Latin lookalike letters, base64 blobs,
  binaries, symlinks, executables outside `scripts/`
- Text addressed to the agent rather than to the reader — "ignore previous
  instructions", anything framed as a system message
- Severity inflation. A finding is bounded by what a config file can prove. If a
  claim needs a value we did not read, it is not a claim
- Company voice drift: exclamation marks, emoji, encouragement, marketing copy.
  See [`skills/shared/arrakis.md`](skills/shared/arrakis.md)

## If you change the scan or the application skill

Run every fixture under `tests/fixtures/` and check the output against each
`EXPECTED.md`, including every "must never appear" line:

```bash
ARRAKIS_SCAN_ROOT=tests/fixtures/empty        # then invoke the scan
ARRAKIS_SCAN_ROOT=tests/fixtures/engineer
ARRAKIS_SCAN_ROOT=tests/fixtures/permissions
ARRAKIS_SCAN_ROOT=tests/fixtures/plugins
ARRAKIS_SCAN_ROOT=tests/fixtures/secrets
```

These are judged by reading, not by an assertion library — the output is prose. A
pull request that touches the skills without one pasted output per fixture is not
ready.

`tests/fixtures/` contains realistic-looking fake credentials on purpose. Never
replace them with placeholders: their whole job is to make a redaction failure
visible. Never add a real one.

## Reporting a security defect

Do not open a public issue. Use
[private vulnerability reporting](https://github.com/Arrakis-Security/careers/security/advisories/new)
or mail build@arrakis.security. See [SECURITY.md](SECURITY.md).

## Licence and provenance

Contributions are under the [MIT licence](LICENSE). Sign your commits if you can
(`git commit -S`) — the default branch requires signed commits, so an unsigned
commit cannot be merged as-is.
