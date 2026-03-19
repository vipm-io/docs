---
title: Environment Variables
---

# Environment Variables

The VIPM CLI recognizes several environment variables that control its behavior. These are useful for CI/CD pipelines, automation scripts, and troubleshooting.

## CI Environment Detection

VIPM automatically detects CI environments and adjusts its behavior — for example, using longer default timeouts to account for slower CI runners. The following CI systems are detected automatically:

| Variable | CI System |
|----------|-----------|
| `CI` | Generic CI convention |
| `CONTINUOUS_INTEGRATION` | Generic CI convention |
| `GITHUB_ACTIONS` | GitHub Actions |
| `GITLAB_CI` | GitLab CI |
| `JENKINS_URL` | Jenkins |
| `TRAVIS` | Travis CI |
| `CIRCLECI` | CircleCI |
| `BUILDKITE` | Buildkite |
| `DRONE` | Drone |
| `APPVEYOR` | AppVeyor |
| `TF_BUILD` | Azure DevOps |
| `TEAMCITY_VERSION` | TeamCity |

No configuration is needed — if any of these variables are set, VIPM treats the environment as CI.

When a CI environment is detected and `VIPM_NONINTERACTIVE` is not explicitly set, VIPM automatically enables non-interactive mode: confirmation prompts are auto-accepted and missing required parameters cause immediate errors instead of hanging. See [Non-Interactive Mode](#vipm_noninteractive) below.

## Non-Interactive Mode

### `VIPM_NONINTERACTIVE`

Disables all interactive prompts. Confirmation prompts are auto-accepted and missing required parameters cause immediate errors instead of blocking on stdin. This prevents commands from hanging in headless environments.

**Auto-enabled in CI** — when a CI environment is detected (see [table above](#ci-environment-detection)) and `VIPM_NONINTERACTIVE` is not explicitly set, non-interactive mode activates automatically. Set `VIPM_NONINTERACTIVE=0` to override this and restore interactive behavior (useful for debugging in CI).

```bash
# Docker — no prompts at all
export VIPM_NONINTERACTIVE=1
vipm install project.vipc

# CI — auto-detected, no configuration needed
vipm install project.vipc

# Override CI detection for debugging
VIPM_NONINTERACTIVE=0 vipm install project.vipc
```

| Value | Behavior |
|-------|----------|
| `1`, `true`, `yes` (any truthy value) | Non-interactive: auto-confirm + error on missing params |
| `0`, `false` | Disabled (overrides CI auto-detection) |
| Empty string | Disabled (a warning is logged) |
| Unset + CI detected | Non-interactive (auto-enabled) |
| Unset + no CI | Interactive (default) |

### `VIPM_ASSUME_YES`

Auto-confirms confirmation prompts only (e.g., "Install 5 packages?") without requiring the `--yes` / `-y` flag on each command. Unlike `VIPM_NONINTERACTIVE`, commands with missing required parameters will still prompt for input.

```bash
export VIPM_ASSUME_YES=1
vipm install project.vipc     # no confirmation prompt
vipm uninstall oglib_boolean  # no confirmation prompt
```

| Value | Behavior |
|-------|----------|
| `1`, `true`, `yes` (any truthy value) | Auto-confirm all prompts |
| `0`, `false` | Disabled (prompts as normal) |
| Empty string | Disabled (a warning is logged) |

Alternatively, use the `--yes` / `-y` flag on individual commands:

```bash
vipm install -y project.vipc
```

### Precedence

When multiple settings apply, VIPM uses this precedence order:

1. `VIPM_NONINTERACTIVE=1` — non-interactive mode
2. `VIPM_NONINTERACTIVE=0` — interactive (overrides CI detection)
3. CI detected (if `VIPM_NONINTERACTIVE` unset) — non-interactive mode
4. `VIPM_ASSUME_YES=1` — auto-confirm only (parameter prompts still work)
5. `--yes` flag — auto-confirm for that command
6. Default — fully interactive

## Timeouts

### `VIPM_TIMEOUT`

Overrides the default operation timeout (in seconds). When set, this takes precedence over the `--timeout` flag and any CI-adjusted defaults.

```bash
export VIPM_TIMEOUT=300   # 5 minutes
vipm install project.vipc
```

## Debugging

### `VIPM_DEBUG`

Enables verbose debug output for troubleshooting.

```bash
export VIPM_DEBUG=1
vipm install oglib_boolean
```

## Output

### `NO_COLOR`

Disables colored output, following the [no-color.org](https://no-color.org/) standard. Equivalent to `--color-mode never`.

```bash
export NO_COLOR=1
```

### `SOURCE_DATE_EPOCH`

When set, VIPM uses this Unix timestamp for the `generated_at` field in `--json` output instead of the current time. This supports [reproducible builds](https://reproducible-builds.org/specs/source-date-epoch/).

```bash
export SOURCE_DATE_EPOCH=1710000000
```

## Edition

### `VIPM_COMMUNITY_EDITION`

Forces VIPM to operate in Community Edition mode, regardless of activation status.

```bash
export VIPM_COMMUNITY_EDITION=1
```

## Related Resources

- [CLI Command Reference](command-reference.md) — command flags and options
- [Docker and Containers](docker.md) — container-specific environment setup
- [GitHub Actions and CI/CD](github-actions.md) — CI workflow examples

--8<-- "need-help.md"
