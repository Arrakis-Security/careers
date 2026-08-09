# Releasing

## Why this document exists

`/plugin marketplace add Arrakis-Security/careers` resolves to the default
branch. Without releases, "shipping" means "merging", and every candidate who
installs or updates gets whatever landed a minute ago. That is a fine way to work
on a website and a poor one for instructions that execute on other people's
machines.

So: `main` is always installable, and a release is a signed tag that a candidate
can pin to and a reviewer can point at.

## Steps

1. **Confirm the guardrails are green on `main`.**

   ```bash
   python3 scripts/validate_manifests.py
   python3 scripts/check_tree.py
   python3 scripts/check_content_safety.py
   ```

2. **Bump the version in all four manifests and in the payload**, in one pull
   request:

   - `.claude-plugin/plugin.json`
   - `.claude-plugin/marketplace.json` (the plugin entry)
   - `.codex-plugin/plugin.json`
   - `gemini-extension.json`
   - `skills/apply-to-arrakis/SKILL.md` — `PLUGIN_VERSION` and the payload's
     `plugin_version`

   `validate_manifests.py` fails if any of these disagree, which is the point.

3. **Re-run the three fixtures** and confirm each `EXPECTED.md` still holds,
   including every "must never appear" line. Paste the outputs in the release pull
   request.

4. **Re-run every install command you publish** against the public repository,
   not a local checkout, and paste the runs in the release pull request. A
   command nobody re-ran does not appear in the README as verified. Update the
   version numbers the README claims verification against.

5. **Tag, signed and annotated:**

   ```bash
   git tag -s v0.1.0 -m "arrakis-careers v0.1.0"
   git push origin v0.1.0
   ```

   Tag creation is restricted to `careers-maintainers`, and tags are not
   overwritable — see [GITHUB-SETTINGS.md](GITHUB-SETTINGS.md).

6. **Write the release notes as a diff summary, not a changelog voice.** What
   changed in what the scan reads, what it prints, and what it claims. If nothing
   changed on the prompt surface, say that explicitly — it is the sentence a
   security-minded candidate is looking for before they update.

7. **Never move a published tag.** If a release is wrong, cut the next one. A tag
   that changes underneath a pinned install is exactly the failure this whole
   document is trying to prevent.

## Verifying a release, as a candidate

```bash
git clone --depth 1 --branch v0.1.0 https://github.com/Arrakis-Security/careers
cd careers
git verify-tag v0.1.0
python3 scripts/check_content_safety.py
```

The last command is our own guardrail, and it runs the same on a candidate's
machine as it does in our CI.
