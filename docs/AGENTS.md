# Agents

This document provides a comprehensive list of persona prompts available in the `codex-plugin` toolkit.

| Agent | Description |
|-------|-------------|
| **a11y-architect** | Accessibility Architect specializing in WCAG 2.2 compliance for Web and Native platforms. Use PROACTIVELY when designing UI components, establishing design systems, or auditing code for inclusive user experiences. |
| **architect** | Software architecture specialist for system design, scalability, and technical decision-making. Use PROACTIVELY when planning new features, refactoring large systems, or making architectural decisions. |
| **build-error-resolver** | Build and TypeScript error resolution specialist. Use PROACTIVELY when build fails or type errors occur. Fixes build/type errors only with minimal diffs, no architectural edits. |
| **code-architect** | Designs feature architectures by analyzing existing codebase patterns and conventions, then providing implementation blueprints with concrete files, interfaces, data flow, and build order. |
| **code-explorer** | Deeply analyzes existing codebase features by tracing execution paths, mapping architecture layers, and documenting dependencies to inform new development. |
| **code-reviewer** | Expert code review specialist. Proactively reviews code for quality, security, and maintainability. Use immediately after writing or modifying code. |
| **code-simplifier** | Simplifies and refines code for clarity, consistency, and maintainability while preserving behavior. |
| **comment-analyzer** | Analyze code comments for accuracy, completeness, maintainability, and comment rot risk. |
| **database-reviewer** | PostgreSQL database specialist for query optimization, schema design, security, and performance. Incorporates Supabase best practices. |
| **doc-updater** | Documentation and codemap specialist. Updates codemaps and documentation, generates docs/CODEMAPS/*, and updates READMEs and guides. |
| **docs-lookup** | Fetches current documentation and returns answers with examples for libraries, frameworks, or APIs using Context7 MCP. |
| **e2e-runner** | End-to-end testing specialist using Vercel Agent Browser (preferred) or Playwright. Manages test journeys and ensures critical user flows work. |
| **loop-operator** | Operate autonomous agent loops, monitor progress, and intervene safely when loops stall. |
| **observer** | Background agent that analyzes session observations to detect patterns and create instincts for project-scoped learning. |
| **opensource-forker** | Fork any project for open-sourcing by sanitizing secrets, replacing internal references, and cleaning git history. |
| **opensource-packager** | Generate complete open-source packaging (README, LICENSE, CONTRIBUTING.md, etc.) for a sanitized project. |
| **opensource-sanitizer** | Verify an open-source fork is fully sanitized before release. Scans for leaked secrets, PII, and internal references. |
| **performance-optimizer** | Performance analysis and optimization specialist. Identifies bottlenecks, optimizes slow code, and reduces bundle sizes. |
| **planner** | Expert planning specialist for complex features and refactoring. Automatically activated for planning tasks. |
| **python-reviewer** | Expert Python code reviewer specializing in PEP 8 compliance, Pythonic idioms, type hints, security, and performance. |
| **react-lead** | Senior React Engineering Lead with deep expertise in Next.js, TypeScript, and Tailwind CSS. |
| **refactor-cleaner** | Dead code cleanup and consolidation specialist. Identifies and safely removes unused code and duplicates. |
| **security-reviewer** | Security vulnerability detection and remediation specialist. Flags secrets, SSRF, injection, and OWASP Top 10 vulnerabilities. |
| **seo-specialist** | SEO specialist for technical SEO audits, on-page optimization, structured data, and content/keyword mapping. |
| **silent-failure-hunter** | Review code for silent failures, swallowed errors, bad fallbacks, and missing error propagation. |
| **typescript-reviewer** | Expert TypeScript/JavaScript code reviewer specializing in type safety, async correctness, and idiomatic patterns. |
| **web-researcher** | Web search and information retrieval specialist. Uses Tavily MCP to query the live web and extract clean markdown/structured data summaries. |
| **skill-comply-classifier** | Classifies tool calls against behavioral steps for skill compliance monitoring. |
| **skill-comply-scenario-generator** | Generates synthetic test scenarios to verify agent behavioral compliance. |
| **skill-comply-spec-generator** | Extracts observable behavioral sequences from natural language skill definitions. |
