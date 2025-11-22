# CLI Documentation Improvement Proposal

## Executive Summary

This proposal outlines recommended improvements to the VIPM CLI documentation structure and content based on a review of the current `docs/cli/` directory. The goal is to enhance discoverability, reduce content duplication, and provide a clearer learning path from beginner to advanced usage.

## Working Plan Tracker

### Phase Status Overview

| Phase | Focus | Status | Last Update | Notes |
|-------|-------|--------|-------------|-------|
| Phase 1 | Immediate fixes (typo, formatting, cross-links) | 🟠 In Progress | 2025-11-22 | Kicking off with typo fix + basic cross-links |
| Phase 2 | Core content gap fill (reference, quick start, troubleshooting, best practices) | ⚪ Not Started | _TBD_ | Will create foundational docs referenced by all guides |
| Phase 3 | Reorganization (hub, integrations, dedupe) | ⚪ Not Started | _TBD_ | Depends on Phase 2 deliverables |
| Phase 4 | Advanced/expansion (scripting, offline, multi-CI) | ⚪ Not Started | _TBD_ | Requires stable base content |

### Active Work Items

| ID | Description | Owner | Links | Status |
|----|-------------|-------|-------|--------|
| 1 | Fix `github-actions.md` header typo and add cross-links | _Unassigned_ | `docs/cli/github-actions.md` | ✅ Done |
| 2 | Standardize CLI example formatting in `index.md` and `docker.md` | _Unassigned_ | `docs/cli/index.md`, `docs/cli/docker.md` | ✅ Done |
| 3 | Draft consolidated command reference | _Unassigned_ | `docs/cli/command-reference.md` (new) | 🟠 In Progress |
| 4 | Draft quick-start/getting-started guide | _Unassigned_ | `docs/cli/getting-started.md` (new) | ✅ Done |

_Update the tables above each time we complete or add scope so this document stays the single source of truth._

## Progress Log

| Date | Activity | Outcome | Notes |
|------|----------|---------|-------|
| 2025-11-22 | Established tracking framework | ✅ | Added tracker, progress log, and instructions to keep proposal living |
| 2025-11-22 | Fixed GitHub Actions header and added cross-links | ✅ | `docs/cli/github-actions.md` heading corrected; both integration pages now reference each other + CLI overview |
| 2025-11-22 | Standardized CLI examples and added "Next Steps" guidance | ✅ | `docs/cli/index.md` now shows consistent command + output blocks; `docs/cli/docker.md` uses the same "Expected output" labeling |
| 2025-11-22 | Fixed root CLI link in site index | ✅ | `docs/index.md` now links to `cli/index.md`; MkDocs build warning resolved |
| 2025-11-22 | Added `AGENTS.md` onboarding notes | ✅ | Captured repo workflow guidance (planning, testing, communication) for future contributors |
| 2025-11-22 | Created initial `docs/cli/getting-started.md` outline | ✅ | Drafted step-by-step quick start (verify CLI, refresh list, install, list packages, next steps) |
| 2025-11-22 | Linked quick-start guide in nav + expanded troubleshooting tips | ✅ | `docs/cli/index.md`, `docs/cli/getting-started.md`, and `mkdocs.yml` updated so the new guide is discoverable and includes built-in help guidance |
| 2025-11-22 | Added placeholder `docs/cli/command-reference.md` | 🟠 | Stub page unblocks cross-links while Phase 2 content is authored |
| 2025-11-22 | Authored initial command reference sections | 🟠 | Added global options + detailed entries for install, uninstall, list, package-list-refresh, activate, build, version, about |
| 2025-11-22 | Documented `vipm search` command | 🟠 | Command reference now includes syntax, options, and examples for search |
| 2025-11-22 | Reduced duplicated examples across CLI docs | ✅ | Streamlined `docs/cli/index.md` and `docs/cli/docker.md`; both now point to the command reference instead of repeating full command walkthroughs |
| 2025-11-22 | Clarified CLI index navigation | ✅ | Updated `docs/cli/index.md` Getting Started section to explicitly link to downstream topic pages |
| 2025-11-22 | Synced CLI pages with command reference availability | ✅ | Updated `docs/cli/index.md`, `docs/cli/getting-started.md`, `docs/cli/docker.md`, and `docs/cli/github-actions.md` to reference the live command reference and current troubleshooting guidance |

## Decision Register

- 2025-11-22 — Use this document (`dev-docs/cli-docs-improvement-proposal.md`) as the canonical plan, progress, and notes tracker. We iterate asynchronously without a fixed cadence.

## Current State Analysis

### Existing Structure

```
docs/cli/
├── index.md           - Overview and basic CLI commands
├── docker.md          - Docker container usage
└── github-actions.md  - CI/CD integration examples
```

### Content Inventory

**index.md (65 lines)**
- CLI features overview
- Use cases
- Example commands (8 common commands)
- Brief getting started section

**docker.md (207 lines)**
- Docker setup and configuration
- Detailed CLI command examples with expected output
- Verification steps
- Use cases and resources

**github-actions.md (253 lines)**
- GitHub Actions setup
- Workflow examples (basic, build/test, release)
- Troubleshooting section
- Resources

## Issues Identified

### 1. Content Quality Issues

- **Typo in github-actions.md:1** - First line shows "ko#" instead of "#"
- **Inconsistent command documentation** - Some commands have expected output examples, others don't
- **Mixed audience levels** - Beginner and advanced content interspersed without clear progression

### 2. Content Duplication

- CLI commands appear in both `index.md` and `docker.md` with varying levels of detail
- Installation/activation steps repeated across files
- Troubleshooting content scattered across multiple files

### 3. Structural Gaps

- **No comprehensive CLI reference** - Missing detailed documentation for all commands and their flags/options
- **No command syntax documentation** - Flags and options not systematically documented
- **Missing scripting guide** - No guidance on writing automation scripts
- **No offline usage guide** - Users may not know about air-gapped or restricted network scenarios
- **Limited error handling** - Few examples of handling common errors in scripts

### 4. Organization Issues

- Use case-driven structure (Docker, GitHub Actions) makes it hard to find specific command documentation
- No clear separation between:
  - Command reference (what commands exist)
  - Task guides (how to accomplish specific goals)
  - Concepts (understanding the CLI architecture)
- Cross-linking could be improved

### 5. Discovery and Navigation

- No quick start or "common tasks" guide
- Beginner users may struggle to find the right starting point
- Advanced users have to search through examples to find specific flags
- No search-friendly command index

## Proposed Structure

### Recommended Organization

```
docs/cli/
├── index.md                          # Overview, quickstart, navigation hub
├── installation.md                   # Installing VIPM CLI (new)
├── getting-started.md                # Quick start guide (new)
│
├── commands/                         # Command reference (new section)
│   ├── index.md                      # Commands overview
│   ├── install.md                    # vipm install command
│   ├── uninstall.md                  # vipm uninstall command
│   ├── list.md                       # vipm list command
│   ├── build.md                      # vipm build command
│   ├── vipm-activate.md              # vipm vipm-activate command
│   └── package-list-refresh.md       # vipm package-list-refresh command
│
├── guides/                           # Task-oriented guides
│   ├── index.md                      # Guides overview
│   ├── managing-dependencies.md      # Working with .vipc files (new)
│   ├── building-packages.md          # Building VI packages (new)
│   ├── scripting-automation.md       # Writing automation scripts (new)
│   └── offline-usage.md              # Air-gapped/offline scenarios (new)
│
├── integration/                      # Integration guides (reorganized)
│   ├── index.md                      # Integration overview
│   ├── docker.md                     # Docker integration (existing, refined)
│   ├── github-actions.md             # GitHub Actions (existing, refined)
│   ├── gitlab-ci.md                  # GitLab CI (new, if applicable)
│   └── other-ci-systems.md           # Other CI platforms (new, if applicable)
│
├── troubleshooting.md                # Consolidated troubleshooting (new)
├── best-practices.md                 # Best practices guide (new)
└── examples.md                       # Complete example scripts (new)
```

### Alternative: Simplified Structure

If the above is too granular for current needs:

```
docs/cli/
├── index.md                    # Overview and quickstart
├── command-reference.md        # All commands with full options (new)
├── getting-started.md          # Step-by-step tutorial (new)
├── docker.md                   # Docker usage (existing, refined)
├── ci-cd.md                    # CI/CD integration (consolidate github-actions)
├── scripting-guide.md          # Automation and scripting patterns (new)
├── troubleshooting.md          # Common issues and solutions (new)
└── best-practices.md           # Recommendations and tips (new)
```

## Content Improvements

### 1. Enhanced Command Reference

Each command should document:
- **Syntax**: Full command syntax with all options
- **Description**: What the command does
- **Options/Flags**: All available flags with descriptions
- **Examples**: Common usage examples
- **Expected Output**: What users should see
- **Exit Codes**: Return codes and their meanings
- **Common Errors**: Typical issues and solutions

**Example format:**

```markdown
# vipm install

## Syntax

```bash
vipm install [options] <package-name> [<package-name>...]
vipm install [options] <path-to-vipc-file>
```

## Description

Installs one or more VI packages into a LabVIEW installation.

## Options

| Option | Description |
|--------|-------------|
| `--labview-version <version>` | Target specific LabVIEW version |
| `--force` | Force reinstallation of packages |
| `--no-dependencies` | Skip dependency installation |

## Examples

Install a single package:
```bash
vipm install oglib_boolean
```

Install multiple packages:
```bash
vipm install oglib_boolean oglib_numeric
```

Install from configuration file:
```bash
vipm install project.vipc
```

## Exit Codes

- `0` - Success
- `1` - General error
- `2` - Package not found

## Common Issues

**Package not found**
- Run `vipm package-list-refresh` first
- Check package name spelling
```

### 2. Quick Start Guide

Create a streamlined getting-started.md with:
1. Installation verification
2. First command (package-list-refresh)
3. Installing your first package
4. Listing installed packages
5. Next steps

### 3. Improved docker.md

**Current**: Mixes setup, commands, and examples

**Proposed changes**:
- Focus on Docker-specific considerations
- Link to command reference for command details
- Keep Docker environment setup and configuration
- Add docker-compose examples
- Include volume mounting best practices
- Add caching strategies

### 4. Improved CI/CD Documentation

**Current**: github-actions.md is comprehensive but GitHub-specific

**Proposed changes**:
- Rename to `ci-cd.md` or keep in `integration/` folder
- Extract common CI patterns applicable to all platforms
- Keep GitHub Actions as primary example
- Add brief examples for GitLab CI, Jenkins, etc.
- Focus on patterns rather than just YAML syntax
- Add section on managing secrets across platforms

### 5. New Scripting Guide

Add scripting-automation.md covering:
- Error handling in bash scripts
- Checking exit codes
- Capturing and parsing output
- Idempotent scripts
- Logging and debugging
- Example: Complete automation script with error handling

### 6. Troubleshooting Consolidation

Create comprehensive troubleshooting.md with:
- Activation issues (from github-actions.md)
- Package installation failures (from github-actions.md)
- Container issues (from github-actions.md)
- Network/proxy issues (new)
- Permission errors (new)
- Common error messages with solutions

### 7. Best Practices Guide

Add best-practices.md covering:
- When to use .vipc files vs direct package names
- Version pinning strategies
- Caching in CI environments
- Security considerations (credentials, secrets)
- Reproducible builds
- Performance optimization

## Content Migration Plan

### Phase 1: Fix Immediate Issues

1. Fix typo in github-actions.md:1 (ko# → #)
2. Standardize command output examples format
3. Add missing cross-links between existing pages

### Phase 2: Add Missing Core Content

1. Create command-reference.md with all commands fully documented
2. Create getting-started.md with step-by-step tutorial
3. Create troubleshooting.md consolidating existing troubleshooting content
4. Create best-practices.md

### Phase 3: Reorganize Existing Content

1. Refactor index.md to be a better hub/overview
2. Refactor docker.md to focus on Docker-specific concerns
3. Refactor github-actions.md to ci-cd.md (or keep in integration/)
4. Remove duplicated CLI command examples (link to reference instead)

### Phase 4: Add Advanced Content

1. Create scripting-guide.md
2. Create offline-usage.md
3. Add more CI platform examples
4. Expand examples.md with real-world scenarios

## Implementation Notes

### Writing Guidelines

- **Be consistent** - Use the same format for all command documentation
- **Show expected output** - Users need to know what success looks like
- **Include error examples** - Show common failures and how to fix them
- **Link liberally** - Cross-reference related commands and guides
- **Test all examples** - Verify every command example works

### Maintenance Considerations

- Keep command reference in sync with actual CLI
- Update examples when CLI changes
- Review and update troubleshooting as new issues emerge
- Consider auto-generating command reference from CLI help text

### Available Resources for Documentation

**Note**: The `vipm` command is available in this development environment and can be used to obtain help documentation for different commands. This means:
- Command syntax and options can be verified by running `vipm <command> --help`
- Expected output can be captured directly from running commands
- New commands or flags can be discovered and documented from the CLI itself
- Documentation accuracy can be maintained by testing against the actual tool

### User Testing

Before finalizing:
- Test with beginner users (can they get started?)
- Test with advanced users (can they find detailed options?)
- Test discoverability (can users find what they need?)

## Benefits of Proposed Changes

1. **Faster onboarding** - Clear getting-started path
2. **Better discoverability** - Easy to find specific commands and options
3. **Reduced frustration** - Comprehensive troubleshooting
4. **Less duplication** - Single source of truth for each command
5. **Improved maintenance** - Easier to keep documentation current
6. **Better SEO** - More pages with focused keywords
7. **Scalability** - Easy to add new commands or guides

## Open Questions

1. Should we create separate pages per command or consolidate in command-reference.md?
   - **Recommendation**: Start consolidated, split if it becomes too large

2. Should we keep the use-case driven structure (Docker, CI/CD) or move to a more reference-style?
   - **Recommendation**: Hybrid - reference for commands, guides for use cases

3. How much content overlap is acceptable between command reference and guides?
   - **Recommendation**: Reference shows syntax/options, guides show context/workflow

4. Should troubleshooting be a separate section or embedded in each page?
   - **Recommendation**: Dedicated page for common issues, specific issues in relevant pages

5. Do we need version-specific documentation?
   - **Recommendation**: Add "since version X" notes, keep single current version docs

## Next Steps

1. Review and approve this proposal
2. Prioritize which phases to implement first
3. Assign documentation writing tasks
4. Create style guide for consistent formatting
5. Set up review process for new content
6. Schedule user testing sessions
