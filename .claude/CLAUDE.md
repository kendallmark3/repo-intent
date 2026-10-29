# Repository Rules — RepoIntent

Built on the Intent-Driven Engineering starter (github.com/kendallmark3/intent-drive-starter).

## Read first
1. `intent/current-feature.md`, including any deltas appended to it.
2. `intents/001-repo-intelligence-v1.md` (the full master intent).
3. `policies/EVIDENCE_POLICY.md` and `contracts/REPORT_CONTRACT.md` — hard requirements, not guidance.
4. `playbooks/REPOSITORY_ANALYSIS_PLAYBOOK.md` — the operating model.

## Working rules
- Run `bash hooks/pre-implement.sh` before implementing.
- Build the smallest useful delta, then let the human observe it and decide: continue or stop. Feedback becomes a delta appended to `intent/current-feature.md` using `templates/delta-template.md`.
- Local-first. Do not add AWS, a database, embeddings, MCP, or a UI unless the intent cannot be met without them.
- Always write tests for code. Run `python3 -m unittest discover -s tests` and `bash hooks/pre-implement.sh` before declaring done.

## Analysis layout
- Target repos are cloned into `targets/<name>/` (gitignored — never commit them).
- Reports go to `reports/<name>/REPORT.md`, with the analyzed commit SHA recorded in section 1.
- Every report must pass `python3 tools/check_citations.py reports/<name>/REPORT.md --repo targets/<name>` before it is handed to a human.
- Eval scorecards go to `evals/runs/<name>.md`; repeated failures go to `evals/FAILURE_LOG.md`.

## Prime Directive
Never assert more than the repository evidence supports.
