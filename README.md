# Codex Plugin

Codex Plugin is a Codex-native migration of `everything-agy`: a broad agentic
development toolkit with reusable skills, expert persona prompts, lifecycle
hooks, and utility scripts for deeper coding workflows.

The original `everything-agy` project is preserved separately. This repository
keeps the content, but restructures the runtime-facing pieces for Codex.

## What Is Included

- **Skills:** 50+ reusable `SKILL.md` workflows under `skills/`.
- **Expert personas:** migrated persona prompts under `agents/`.
- **Hooks:** Codex lifecycle hook configuration under `hooks/hooks.json`.
- **Utilities:** observer, skill compliance, project detection, and support
  scripts under `scripts/`.
- **Legacy references:** original Antigravity manifests under
  `docs/legacy-antigravity/`.

## Codex Plugin Structure

```text
codex-plugin/
├── .codex-plugin/plugin.json   # Codex plugin manifest
├── hooks/hooks.json            # Plugin-bundled lifecycle hooks
├── skills/                     # Codex Agent Skills
├── agents/                     # Expert persona prompts
├── scripts/                    # Utility scripts and compliance tooling
├── docs/                       # Agent/skill indexes and legacy manifests
└── assets/                     # Optional plugin assets
```

## Install Locally In Codex

For local development, expose the plugin through a Codex plugin marketplace or
install it from a marketplace that points at this folder.

The required manifest is:

```text
.codex-plugin/plugin.json
```

Validate the package before installing:

```bash
npm run validate
```

## Hooks

The plugin ships Codex lifecycle hooks for:

- `PreToolUse`
- `PostToolUse`

Hooks are non-managed plugin hooks. Codex will require you to review and trust
them before they run.

Observer hooks are disabled by default. To enable local observation:

```bash
export CODEX_PLUGIN_OBSERVER_ENABLED=true
```

Observation data is stored under:

```text
~/.codex/codex-plugin/continuous-learning/
```

## Skills

Skills are available under `skills/`. Codex can invoke them explicitly with
`$skill-name` or implicitly when a task matches the skill description.

Examples:

- `$code-reviewer`
- `$team-builder`
- `$security-review`
- `$verification-loop`
- `$workspace-surface-audit`

## Agents

Codex plugins do not currently use `agents/` as a first-class manifest field.
The migrated `agents/` directory is preserved as a persona library, and skills
such as `team-builder`, `code-reviewer`, and planning/review workflows can use
those prompts as source material.

## Skill Compliance

The `skill-comply` tooling is preserved under `scripts/skill_comply/`. It still
uses Gemini CLI internally for scenario generation/classification where the
original tool requires it.

```bash
python3 scripts/skill_comply/run.py skills/search-first/SKILL.md
```

## Migration Notes

This repo was migrated from `everything-agy` with these Codex-specific changes:

- Antigravity `plugin.json` moved to `docs/legacy-antigravity/plugin.json`.
- Antigravity MCP config removed; this Codex plugin does not bundle MCP
  servers.
- Antigravity `hooks.json` moved to `docs/legacy-antigravity/hooks.json`.
- Codex plugin manifest created at `.codex-plugin/plugin.json`.
- Codex hook config created at `hooks/hooks.json`.
- Runtime observer/config paths moved from the legacy Antigravity storage
  location to `~/.codex/codex-plugin`.

## License

MIT.
