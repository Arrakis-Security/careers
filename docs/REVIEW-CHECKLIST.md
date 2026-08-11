# Maintainer review checklist

For anyone in `@Arrakis-Security/careers-maintainers` about to approve a pull
request. The contributor's checklist is in the pull request template; this is
the reviewer's, and it assumes the contributor may have ticked boxes without
meaning them.

Read the diff. Not the description of the diff.

## Every pull request

- [ ] CI `guardrails` green — and if `check_content_safety.py` was satisfied by a
      new entry in `.github/allowed-lines.txt`, **read the allowlisted line
      itself**. That file is where a hostile change hides in plain sight: the hash
      makes it look reviewed.
- [ ] Diff is small enough that you read every line. If it is not, ask for a split
      rather than skimming. Skimming a prose repository is not review.
- [ ] Character-level: no invisible characters, no bidi controls, no Latin
      lookalikes from another script, no base64 blob. CI checks this; confirm you
      believe it.
- [ ] Author has no write access they should not have, and did not approve their
      own change.
- [ ] Commit is signed.

## If it touches `skills/`, `commands/`, `AGENTS.md`, or `GEMINI.md`

This is the code-execution surface. For each added or changed sentence, ask:

- [ ] Could an agent read this as a licence to make a network call?
- [ ] Could an agent read this as a licence to write, move, or delete a file?
- [ ] Does it widen what gets read — a new path, a new glob, a walk instead of a
      fixed list, "and any other config you find"?
- [ ] Does it read the *contents* of a secret store, rather than noting that the
      store is reachable?
- [ ] Does it weaken redaction, including in an example? A masked value in a
      sample output that shows four real characters is a leak in the product.
- [ ] Does it let a severity claim rest on something a config file cannot prove?
      Fabricated capability is the defect `tests/fixtures/engineer/EXPECTED.md`
      exists to catch, and it always looks confident.
- [ ] Would this sentence still be safe if the file it describes were written by
      an attacker? That is the actual runtime condition.
- [ ] Voice: no exclamation marks, no emoji, no encouragement, no marketing.
- [ ] Scope, per `CONTRIBUTING.md` "What this plugin is for": does this add
      something genuinely missing, or align a claim with behaviour? A change that
      widens the scan past what the page promises is out of scope even when it
      finds real problems — decide to advertise it first, then build it.
- [ ] Length: does the run get longer, and is the finding worth it? Ten lines of
      guidance for one line of output is a rewrite, not an approval.
- [ ] Does it publish more of *how we rank* than the teaser needs?
      `references/severity.md` is the file to watch.

## If it touches the application skill

- [ ] `SUBMIT_ENABLED` is still `false`, `SUBMIT_URL` and `SUBMIT_ANON_KEY` still
      empty. CI enforces it; look anyway.
- [ ] The confirmation-before-transmission step is intact and unconditional.
- [ ] The fallback still writes the file **first**, prints the absolute path, and
      says which outcome happened. Losing an application silently is the one
      unacceptable behaviour.
- [ ] Nothing new enters the payload. Not a scan summary, not a count, not an
      environment fingerprint, not the repository name.

## If it touches manifests or install docs

- [ ] Version changed in all four manifests and in the payload `plugin_version`.
      CI checks this.
- [ ] Every install command the README publishes has been run against the public
      repository, at the version the README names, and the pull request says who
      ran it and when. A command that returns "plugin not found" is worse than
      no command.
- [ ] Version claims in the README name versions someone actually ran.

## If it touches `.github/` or `scripts/`

- [ ] You are not the author. These files are the guardrails, and a change here
      can switch off every check above — it is the one class of change worth
      finding a second pair of eyes for even when the ruleset does not force it.
- [ ] No workflow gained write permission, a secret, or the privileged
      `pull_request` trigger variant.
- [ ] Every action still pinned to a full commit SHA.
- [ ] No check was deleted or made non-blocking to get something merged. If a
      check is wrong, fix the check in its own pull request.

## Before you click merge

- [ ] Squash, with a message that says what changed rather than "address review".
- [ ] If this reaches candidates, the release step in
      [RELEASING.md](RELEASING.md) is next — merging is not shipping, and a
      moving default branch is not a release.
