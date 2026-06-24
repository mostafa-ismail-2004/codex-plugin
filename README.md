# Codex Plugin

Codex Plugin is a Codex-native agentic development toolkit that equips your environment with reusable skills, expert persona prompts, lifecycle hooks, and development utilities.

## What Is Included

- **Skills:** 50+ reusable `SKILL.md` workflows under `skills/`.
- **Expert personas:** persona prompts under `agents/`.
- **Hooks:** Codex lifecycle hook configuration under `hooks/hooks.json`.
- **Utilities:** observer, skill compliance, project detection, and support scripts under `scripts/`.

## Codex Plugin Structure

```text
codex-plugin/
├── .codex-plugin/plugin.json   # Codex plugin manifest
├── hooks/hooks.json            # Plugin-bundled lifecycle hooks
├── skills/                     # Codex Agent Skills
├── agents/                     # Expert persona prompts
├── scripts/                    # Utility scripts and compliance tooling
└── docs/                       # Agent/skill indexes
```

## Install Locally In Codex

For local development, expose the plugin through a Codex plugin marketplace or install it from a marketplace that points at this folder.

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

Hooks are non-managed plugin hooks. Codex will require you to review and trust them before they run.

Observer hooks are disabled by default. To enable local observation:

```bash
export CODEX_PLUGIN_OBSERVER_ENABLED=true
```

Observation data is stored under:

```text
~/.codex/codex-plugin/continuous-learning/
```

## Skills

Skills are available under `skills/`. Codex can invoke them explicitly with `$skill-name` or implicitly when a task matches the skill description.

Examples:

- `$code-reviewer`
- `$team-builder`
- `$security-review`
- `$verification-loop`
- `$workspace-surface-audit`

## Agents

Codex plugins do not currently use `agents/` as a first-class manifest field. The `agents/` directory is preserved as a persona library, and skills such as `team-builder`, `code-reviewer`, and planning/review workflows can use those prompts as source material.

## Skill Compliance

The `skill-comply` tooling is preserved under `scripts/skill_comply/`.

```bash
python3 scripts/skill_comply/run.py skills/search-first/SKILL.md
```

## License

MIT.
