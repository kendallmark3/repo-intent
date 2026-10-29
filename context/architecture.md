# Architecture

V1 is a Claude Code workflow, not a service.

- **Skill:** `.claude/skills/repo-intent/SKILL.md` — the analysis behavior, invoked as `/repo-intent <target>`.
- **Rules:** `policies/EVIDENCE_POLICY.md` (hard), `contracts/REPORT_CONTRACT.md` (hard), `playbooks/REPOSITORY_ANALYSIS_PLAYBOOK.md` (operating model).
- **Mechanical check:** `tools/check_citations.py` — Python stdlib only; verifies citations exist and the ledger is consistent.
- **Layout:** `targets/<name>/` (input, gitignored) → `reports/<name>/REPORT.md` (output) → `evals/runs/<name>.md` (human audit).

No server, database, embeddings, MCP, or cloud. Add a layer only when `evals/FAILURE_LOG.md` shows a repeated failure that needs it.
