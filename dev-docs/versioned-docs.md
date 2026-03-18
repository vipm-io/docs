# Versioned Documentation with mike

## Overview

The docs site uses [mike](https://github.com/jimporter/mike) to publish versioned documentation. Each VIPM release gets its own version of the docs that persists permanently, so users can always find documentation matching their installed version.

The version switcher dropdown appears in the site header, powered by MkDocs Material's built-in version provider.

## How it works

### Tools

- **mike** — manages multiple versions of the docs on the `gh-pages` branch. Each version is deployed to a path prefix (e.g., `/2026-Q1/`, `/dev/`).
- **MkDocs Material** — renders the version switcher UI via the `extra.version` config in `mkdocs.yml`.

### Configuration

**`mkdocs.yml`:**

```yaml
extra:
  version:
    provider: mike
    default: latest
```

**`pyproject.toml`:**

```toml
dependencies = [
    "mike>=2.1.0",
    ...
]
```

### Versioning scheme

Versions use quarter-based naming to match VIPM releases:

| Version label | Meaning |
|---------------|---------|
| `dev` | Unreleased docs from `main` branch |
| `2026-Q1` | VIPM 2026 Q1 GA release |
| `2026-Q3` | VIPM 2026 Q3 GA release |
| `latest` | Alias — always points to the most recent GA release |

The `latest` alias is what `docs.vipm.io/` redirects to by default.

## CI/CD workflow

The deploy logic lives in `.github/workflows/ci.yml`.

### Automatic deployments

| Trigger | Version deployed | Sets `latest`? |
|---------|-----------------|----------------|
| Push to `main` | `dev` | No |
| Push to `release/*` branch | Extracted from branch name (e.g., `release/2026-Q3` → `2026-Q3`) | No |

### Manual deployments

Use the **workflow_dispatch** trigger in GitHub Actions to deploy with custom parameters:

| Input | Description |
|-------|-------------|
| `version` | Version label to deploy (e.g., `2026-Q1`, `dev`) |
| `set_latest` | Whether to update the `latest` alias to point to this version |

This is used for:
- Deploying a GA release as `latest` for the first time
- Redeploying a hotfix to an existing version
- Bootstrapping historical versions

### PR builds

Pull requests build and validate with `--strict` but do **not** deploy any version. The `pr-preview-action` in `preview.yml` handles ephemeral PR previews separately.

## Release workflow

### Shipping a new VIPM release (e.g., 2026 Q3)

1. **During development:** `main` branch auto-deploys as `dev` on every push.

2. **At release time:** Push or merge to `release/2026-Q3` branch. CI auto-deploys version `2026-Q3`.

3. **Set as latest:** Trigger workflow_dispatch manually with `version: 2026-Q3` and `set_latest: true`. This updates the `latest` alias so `docs.vipm.io/` redirects to the Q3 docs.

4. **Post-release hotfixes:** Commit typo fixes or corrections to the `release/2026-Q3` branch. CI redeploys `2026-Q3` with updated content. Previous versions are not affected.

### First-time setup (bootstrapping)

This was completed on 2026-03-17. Steps are preserved here for reference.

When mike was first deployed, the `gh-pages` branch needed to be initialized:

1. Merged the mike PR to `main` → CI deployed `dev` version automatically.
2. Triggered workflow_dispatch manually with `version: 2026-Q1` and `set_latest: true` → deployed `2026-Q1` and set it as the default.
3. Rebased the `release/2026-Q1` branch onto `main` so it has the mike CI config, then pushed it.

**Lesson learned:** Release branches created before the mike PR was merged don't have the `release/**` CI trigger in their workflow file. GitHub Actions uses the workflow from the branch being pushed, not from `main`. The fix is to rebase the release branch onto `main` after the mike PR merges. Alternatively, use workflow_dispatch to deploy manually.

## Local development

### Preview the current docs (single version)

```bash
just dev
# or
uv run mkdocs serve
```

### List deployed versions

```bash
uv run mike list
```

### Deploy a version locally (for testing)

```bash
uv run mike deploy 2026-Q3
uv run mike deploy 2026-Q3 latest --update-aliases
```

### Preview all versions locally

```bash
uv run mike serve
```

This serves the full multi-version site from the `gh-pages` branch.

### Set the default version

```bash
uv run mike set-default latest
```

## Maintenance branches

Each GA release should have a persistent `release/<version>` branch:

| Branch | Version | Status |
|--------|---------|--------|
| `main` | `dev` | Active development |
| `release/2026-Q1` | `2026-Q1` | Maintenance (hotfixes only) — current `latest` |
| `release/2026-Q3` | `2026-Q3` | In development (Q3 preview → GA) |

Hotfixes to shipped docs are committed to the maintenance branch and CI redeploys that version automatically.

## File reference

| File | Role |
|------|------|
| `mkdocs.yml` | `extra.version` enables the version switcher |
| `pyproject.toml` | `mike` dependency |
| `.github/workflows/ci.yml` | Deploy logic (auto + manual) |
| `.github/workflows/preview.yml` | PR preview deploys (unchanged) |
