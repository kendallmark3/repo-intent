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

---

# Intent Delta — 2026-10-29 (after run 1: clinical-evidence-coordinator)

## Observation
The first report was accurate and auditable but long; an architect needs the conclusion before the forensics. Several claims stated absence ("no code uses S3", "no authentication") more firmly than a static search can support. There was no explicit hand-off for what to double-check before repeating findings aloud.

## Keep
The forensic report, claims ledger, citation format, and checker.

## Change
1. Add a one-page **Architect Brief** above the full forensic report.
2. Require cautious, scoped language for absence claims (Evidence Policy Rule 16).
3. Add a final section: **"What I would verify before repeating this in an architecture meeting."**

## Evidence
`tools/check_citations.py` enforces all three (brief present before section 1 and within 400 words; absence claims phrased as findings with a `Search scope:` caveat; final verify section present and citing claim IDs), and the clinical-evidence-coordinator report is regenerated to pass.
