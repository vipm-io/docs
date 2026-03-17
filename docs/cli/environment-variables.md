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

!!! note
    CI detection affects **timeouts only**. It does not automatically skip confirmation prompts. Use `VIPM_ASSUME_YES` or the `--yes` flag to skip prompts in CI. See [Confirmation Prompts](#confirmation-prompts) below.

## Confirmation Prompts

### `VIPM_ASSUME_YES`

Auto-confirms all interactive prompts without requiring the `--yes` / `-y` flag on each command. This is the recommended approach for CI/CD pipelines where you want all commands to proceed non-interactively.

```bash
export VIPM_ASSUME_YES=1
vipm install project.vipc     # no prompt
vipm uninstall oglib_boolean  # no prompt
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
