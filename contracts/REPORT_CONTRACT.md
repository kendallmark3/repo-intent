# Repository Intelligence Report — Output Contract

The final report must be useful to an architect and auditable by an engineer.

## Architect Brief (first, above section 1)
One page, at most 400 words: what an architect needs in two minutes. It sits above the forensic report and is written from the claims ledger like everything else. Every bullet cites claim IDs.

Required fields:
- **What it is** — one or two sentences.
- **Shape** — entry points, major components, runtime/platform.
- **Where the intelligence is** — what is AI/model-driven vs deterministic (or "not applicable").
- **What's real vs aspirational** — implemented and evidenced vs documented, configured, or provisioned but unused.
- **Top risks** — at most 3.
- **Biggest unknowns** — at most 3.

No new facts appear in the brief that are not in the ledger.

## 1. Repository Identity
- Repository/path
- Revision/commit SHA (required when the repo is a git checkout; citations are only valid at that revision)
- Analysis timestamp if available
- Languages/frameworks observed
- Analysis limitations

## 2. Executive Orientation
Maximum ~10 bullets or a short narrative.

Explain:
- what the repository appears to be;
- its primary purpose;
- major architectural shape;
- major execution boundary;
- most important uncertainty.

Every material statement must reference claim IDs.

## 3. Coverage & Confidence
Summarize what areas were inspected and where evidence is weak.

Do **not** imply complete coverage if the repository was sampled.

## 4. System Purpose
Separate:
- documented purpose;
- implemented evidence;
- inferred purpose;
- unknowns/contradictions.

## 5. Entry Points & Execution Paths
Identify likely runtime/build/test/CLI/job entry points and show evidence.

## 6. Component Map
For each major component:
- responsibility;
- key files/symbols;
- dependencies;
- callers/consumers when visible;
- claim IDs.

## 7. Data Flow & Persistence
Describe only flows supported by evidence.

Show:
- inputs;
- transformations;
- persistence;
- outputs;
- unresolved gaps.

## 8. External Integrations
For each observed/inferred integration:
- integration name/type;
- evidence;
- whether usage is direct, configured, optional, test-only, or uncertain.

## 9. Interfaces / APIs
Identify visible:
- HTTP APIs;
- events/messages;
- CLI;
- libraries/public interfaces;
- scheduled jobs;
- files/data contracts.

## 10. Build / Test / Deploy / Operate
Describe what the repo supports or documents.

Do not convert deployment files into claims about actual live environments.

## 11. Security & Authentication Evidence
Document visible mechanisms and boundaries without claiming the overall system is secure.

## 12. Domain / Business Concepts
List domain concepts that are directly named or strongly corroborated.

Mark speculative business interpretation as inference.

## 13. Contradictions / Drift
Examples:
- README says X, code implements Y;
- config references removed module;
- test behavior differs from docs;
- multiple competing entry points;
- stale deployment artifacts.

## 14. Important Unknowns
A short, valuable list—not generic questions.

For each unknown:
- what is unknown;
- why the repo cannot establish it;
- what evidence would resolve it.

## 15. Claims Ledger

| ID | Claim | Class | Strength | Confidence | Evidence | Verification | Caveat |
|---|---|---|---|---|---|---|---|
| C-001 | ... | OBSERVED/INFERRED/UNKNOWN/CONTRADICTED | DIRECT/CORROBORATED/INDIRECT/INSUFFICIENT | HIGH/MEDIUM/LOW | `path:L10-L25#symbol` (see format below) | VERIFIED/QUALIFIED/FAILED | ... |

Rules:
- OBSERVED, INFERRED, and CONTRADICTED claims need at least one citation. UNKNOWN claims state what evidence would resolve them instead.
- INFERRED claims list the claim IDs or citations they were derived from.
- A claim whose verification FAILED is rewritten, downgraded, or removed — never shipped as-is.
- **Absence claims** (something is not used, not present, never called, unenforced) follow Evidence Policy Rule 16: claim text says "no … found" / "not observed" rather than "does not exist", and the Caveat begins `Search scope:` stating what was searched and how.

### Evidence Citation Format
Evidence must be machine-checkable. Wrap each citation in backticks, paths relative to the analyzed repo root:

| Form | Meaning |
|---|---|
| `` `src/app.py` `` | whole file |
| `` `src/app.py:L42` `` | single line |
| `` `src/app.py:L42-L60` `` | line range |
| `` `src/app.py:L42-L60#create_app` `` | range that must contain `create_app` |
| `` `pyproject.toml#fastapi` `` | file that must contain `fastapi` |

Separate multiple citations with `;`. In the ledger's Evidence column, **every** backticked token must be a citation — put explanatory text outside backticks. In report prose, only tokens with a `:L` or `#` locator are checked, so ordinary inline code (`/api/health`, `0.2.0`) is fine there. Symbols may contain spaces. Before delivery, run:

```bash
python3 tools/check_citations.py reports/<name>/REPORT.md --repo targets/<name>
```

It verifies files exist, line ranges are in bounds, symbols appear where cited, every body claim ID is in the ledger, and ledger vocabulary is valid. Passing it is necessary, not sufficient: it cannot judge whether evidence supports the wording.

## 16. Next Inspection Targets
Recommend only a few next targets with the highest information value.

For each:
- target;
- uncertainty it resolves;
- expected value.

## 17. Verify Before Repeating
Final section, titled **"What I would verify before repeating this in an architecture meeting."**

A short list (3–7 items) of the conclusions most likely to be repeated aloud, each with:
- the statement as you would say it in the meeting;
- claim IDs it rests on;
- why it could be wrong or overstated (static-only analysis, absence claim, sampled coverage, documented-not-observed);
- the cheapest check that would confirm it (a command, a console, a person).

Prioritize high-impact claims, absence claims, and anything resting on documentation alone.

## Prohibited Output
The report must not:
- invent facts to make sections feel complete;
- hide uncertainty behind polished prose;
- cite files that do not contain the claimed evidence;
- claim production reality from repository artifacts alone;
- state an absence as fact ("X is never used") instead of a scoped finding ("no use of X found in <scope>");
- present generic framework knowledge as repository-specific evidence.
