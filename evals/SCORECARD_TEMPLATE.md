# Eval Run — <target name>

Copy to `evals/runs/<name>.md` for each analyzed repository.

## Identity
- Target: <name / URL>
- Commit SHA: <sha>
- Shape: small/clear | medium multi-layer | framework/library/CLI | known-deeply | deceptive/stale
- Evaluator knows this repo well: yes | no
- Report: `reports/<name>/REPORT.md`
- Citation checker: PASS | FAIL — <summary line>
- Analysis cost (approx. tokens / wall-clock): <...>

## Claims Audit
Minimum sample: 5 high-impact, 5 ordinary observed, 3 inferred, all contradictions, all HIGH-confidence security/auth/deployment claims.

| Claim ID | Type | Result (PASS / QUALIFIED / FAIL) | Note |
|---|---|---|---|
| C-001 | high-impact | | |

## Scores
| Dimension | Result | Note |
|---|---|---|
| Unsupported claim rate | <n FAIL / n sampled> | |
| Evidence precision | <PASS / QUALIFIED / FAIL counts> | |
| Major component recall | <found / expected> — missed: | |
| Entry-point accuracy | | |
| Representative flow accuracy | | |
| Unknown honesty | | |
| Contradiction detection | <correct / missed / false> | |
| Hallucination traps | <resisted / fell for> | |
| Repeatability (if re-run) | | |
| Architect usefulness (1 sentence) | | |

## Failures → `evals/FAILURE_LOG.md`
- <failure category>: <what happened> (claim ID)
