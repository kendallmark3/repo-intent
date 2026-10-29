# Current Feature — Intent 001: RepoIntent V1

<!-- Full intent: intents/001-repo-intelligence-v1.md. This file is the Progressive Intent working copy; append deltas below, do not rewrite. -->

## Outcome
Running the `repo-intent` skill against a checked-out repository in `targets/<name>` produces `reports/<name>/REPORT.md`: a Repository Intelligence Report that conforms to `contracts/REPORT_CONTRACT.md`, where every material claim is in the claims ledger with exact repository evidence.

## Success / Evidence
- Reports exist for at least three repositories of different shapes (see `examples/OPEN_SOURCE_TARGETS.md`), at least one the evaluator knows well.
- `python3 tools/check_citations.py reports/<name>/REPORT.md --repo targets/<name>` passes for each report.
- A manual audit per `evals/EVALUATION_PLAN.md`, recorded in `evals/runs/<name>.md` from `evals/SCORECARD_TEMPLATE.md`, finds zero knowingly unsupported material claims.
- Failures observed are logged in `evals/FAILURE_LOG.md`; they, not imagination, choose Intent 002.

## Constraints / Boundaries
- Follow `intents/001-repo-intelligence-v1.md` Hard Constraints and Stop Conditions.
- Never commit cloned target repositories (`targets/` is gitignored).
