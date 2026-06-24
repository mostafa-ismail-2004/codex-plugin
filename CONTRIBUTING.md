# Contributing to Codex Plugin

Thanks for helping improve Codex Plugin. This project packages reusable Codex
skills, persona prompts, hooks, MCP configuration, and utility scripts.

## Adding a New Persona

Persona prompts live in `agents/`.

1. Create a new `.md` file in `agents/`.
2. Add frontmatter with `name` and `description` when useful.
3. Keep the prompt focused on one role or review lens.
4. Update `docs/AGENTS.md` with the new persona name and summary.

## Adding a New Skill

Skills live in `skills/<skill-name>/SKILL.md`.

1. Create a new directory under `skills/`.
2. Add a `SKILL.md` file with `name` and `description` frontmatter.
3. Write clear trigger conditions and concrete workflow steps.
4. Update `docs/SKILLS.md` with the new skill.

## Modifying Hooks or Scripts

When changing `hooks/` or `scripts/`:

1. Keep shell scripts POSIX-friendly where practical.
2. Avoid hardcoded machine-local paths.
3. Do not commit secrets, tokens, `.env` files, or generated caches.
4. Update `README.md` when environment variables or setup steps change.

## Validation

Run:

```bash
npm run validate
bash -n hooks/observe.sh hooks/sync-config.sh hooks/suggest-compact.sh scripts/start-observer.sh scripts/observer-loop.sh scripts/session-guardian.sh scripts/watch.sh
python3 -m compileall scripts
```

If `pytest` is installed, also run:

```bash
python3 -m pytest scripts/test_parse_instinct.py
```

## License

By contributing, you agree that your contributions will be licensed under the
same license as this project.
