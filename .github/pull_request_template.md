<!--
Thanks for contributing. One thing to know before you fill this in: the markdown
in this repository is not documentation, it is instructions that run on other
people's laptops with access to their agent configuration. We review it the way
we would review a patch to a privileged binary. Small, single-purpose pull
requests get merged; large ones get questions.
-->

## What this changes

<!-- One or two sentences. If it changes candidate-visible output, paste the
     before and after. -->

## Why

<!-- Link an issue if there is one. -->

## Checks

- [ ] `python3 scripts/validate_manifests.py` passes locally
- [ ] `python3 scripts/check_content_safety.py` passes locally
- [ ] If a version changed, it changed in all four manifests and in the payload

## The prompt surface

Tick every line, or say why it does not apply.

- [ ] This change adds **no** instruction to make a network call, and no URL that
      an agent is told to fetch
- [ ] This change adds **no** instruction to write, move, or delete a file
      outside the documented single application file
- [ ] This change does **not** widen what the scan reads, and does not read the
      *contents* of any secret store (`.env`, key files, `~/.ssh`, keychains)
- [ ] This change does **not** weaken redaction, and prints no value that could
      be a credential — not even a prefix
- [ ] This change does **not** set `SUBMIT_ENABLED` to true, and adds no key,
      token, endpoint, or hostname
- [ ] Every character in the diff is one I typed — no invisible characters, no
      pasted blobs, no lookalike letters from another alphabet
- [ ] Nothing here tells the agent to ignore its earlier instructions, or is
      phrased as if it came from the system rather than from the repository
- [ ] Any new severity claim is bounded by what a config file can prove, per
      `skills/agent-surface-scan/references/severity.md`

## If it touches the scan or the application skill

- [ ] Run against every fixture under `tests/fixtures/` with `ARRAKIS_SCAN_ROOT`
      set, and confirm each `EXPECTED.md` still holds — including every
      "must never appear" line
- [ ] Paste one output per fixture, or say which you could not run and why

## Anything you are unsure about

<!-- Say it here. "I think this line could be read two ways" is a useful
     sentence and costs you nothing in review. -->
