# GitHub settings runbook

Files in a repository cannot enforce who merges. Everything below is configured in
the GitHub UI or API by an org owner, and none of it is visible from a clone —
which is why it is written down here, so it can be audited and restored.

Work top to bottom. Items marked **required** are the ones that make the claim
"only Arrakis Security can approve" true.

---

## 1. Org: Arrakis-Security

Settings → Member privileges

- **required** Base permissions: **Read**. Not Write. With Write as the base, any
  org member can push to `main` and no ruleset short of code-owner review saves
  you.
- Repository creation: restrict to owners.
- Allow members to change repository visibilities: **off**.
- Allow members to delete or transfer repositories: **off**.
- Allow forking of private repositories: **off**.

Settings → Authentication security

- **required** Require two-factor authentication for everyone in the org.
- Require SSO if you have it.

Settings → Third-party Actions / OAuth app access

- Restrict third-party application access, and approve individually.
- Actions → Policies: allow only actions created by GitHub plus the specific
  pinned action this repository uses (`actions/checkout`). "Allow all actions" is
  how a supply-chain compromise reaches a runner.

Settings → Actions → General

- **required** Workflow permissions: **Read repository contents** by default.
- **required** "Allow GitHub Actions to create and approve pull requests": **off**.
  Left on, a workflow can approve its own change and satisfy review.
- **required** Fork pull request workflows from outside collaborators: **Require
  approval for all external contributors**. Not "first-time contributors".

Teams

- `security` — Arrakis Security staff who may approve merges here. Repository
  role: Maintain (or Write). This is the team named in `.github/CODEOWNERS`, and
  it owns every path. Membership is the whole access-control list for this
  repository, so keep it to people you would trust to ship to a candidate's
  laptop unreviewed.
- Outsourced contributors get **no** team and **no** write access. They fork.
- Worth doing once there is a second staff team: make it a co-owner of
  `.github/`, `scripts/`, `SECURITY.md` and the manifests, so disarming a
  guardrail needs two people rather than one.

---

## 2. Repository: Arrakis-Security/careers

Settings → General

- Default branch: `main`.
- Features: Wikis **off**, Projects **off**, Discussions off unless someone owns
  it. Issues **on** — the templates route security reports privately.
- Pull requests: allow **squash merge only**. Disable merge commits and rebase
  merging, so history stays one reviewed commit per change.
- **required** "Always suggest updating pull request branches" on; "Allow auto-merge"
  **off**. Auto-merge plus a passing CI run is a way to land a change nobody read.
- Automatically delete head branches: on.
- **required** Require contributors to sign off on web-based commits: on.

Settings → Advanced (danger zone)

- Do not enable "Allow force pushes" anywhere.

---

## 3. Ruleset for `main` — **required**

Settings → Rules → Rulesets → New branch ruleset. Name it `main-protected`,
enforcement **Active**, target the default branch.

Bypass list: **empty**. Not "organization admin", not you. A bypass list is the
setting that quietly makes every other line here optional.

Rules to enable:

- Restrict creations, **Restrict updates**, **Restrict deletions**.
- **Block force pushes**.
- **Require linear history**.
- **Require signed commits**.
- **Require a pull request before merging**, with:
  - Required approvals: **2** (1 is acceptable only while the team is smaller
    than three people — say which you chose and revisit it).
  - **Dismiss stale pull request approvals when new commits are pushed**.
  - **Require review from Code Owners**.
  - **Require approval of the most recent reviewable push** — this is what stops a
    maintainer approving their own final commit.
  - **Require conversation resolution before merging**.
- **Require status checks to pass**, with "Require branches to be up to date"
  and the check named **`guardrails`** (the job in `.github/workflows/ci.yml`).
- Block force pushes, and restrict who can dismiss reviews to `security`.

## 4. Ruleset for release tags — **required if you tag**

New **tag** ruleset, name `release-tags`, enforcement Active, target pattern
`v*`. Empty bypass list. Enable Restrict creations (to `security`), Restrict
updates, Restrict deletions, Require signed commits.

Installs are pinned to tags, so an overwritable tag is an overwritable install.

---

## 5. Code security

Settings → Advanced Security / Code security and analysis

- **required** Secret scanning: **on**.
- **required** Push protection: **on**. Note the consequence for this repository:
  `tests/fixtures/` contains deliberately fake credentials. If push protection
  blocks a legitimate push, resolve it as **"Used in tests"** in the UI — do not
  weaken the fixtures, and do not add a real-looking value that is actually real.
- Dependabot alerts and security updates: on (only the pinned Actions here).
- **required** Private vulnerability reporting: **on**. The issue template links to
  it, and that link 404s until this is enabled.
- CodeQL: not applicable — there is no code. Do not enable a default setup that
  will report "no languages found" every week and train people to ignore checks.

---

## 6. Public presentation

Repository main page → About (the gear)

- Description: *Scan your own agent attack surface, then apply to Arrakis
  Security from your terminal. Read-only, local-only, no résumé.*
- Website: `https://arrakis.security/careers`
- Topics: `agent-security`, `mcp`, `prompt-injection`, `claude-code`, `codex`,
  `security`, `careers`, `hiring`, `ai-security`.
- Releases and Packages: uncheck Packages, keep Releases. Publish `v0.1.0` so the
  sidebar is not empty — an empty Releases section on a security repository reads
  as unmaintained.

Settings → General → Social preview: upload a 1280×640 image. The default
autogenerated card is the single cheapest thing to fix about first impressions.

Community Standards (`/community`) should show all green once this branch merges:
description, README, code of conduct, contributing, licence, security policy,
issue templates, pull request template.

---

## 7. Audit this quarterly

Ten minutes, and it catches the drift that undoes all of the above:

- [ ] Ruleset bypass list still empty
- [ ] `security` membership still only staff; nobody added "temporarily"
- [ ] No outside collaborator holds write access
- [ ] Org base permission still Read
- [ ] Actions still cannot approve pull requests
- [ ] Fork workflow approval still "all external contributors"
- [ ] `main` still requires the `guardrails` check by that exact name
- [ ] Every published install command still matches a ticked box in
      `tests/INSTALL-CHECKLIST.md`
- [ ] Latest release tag is signed, and the README pins to a tag that exists
