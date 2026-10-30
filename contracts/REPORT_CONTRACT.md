# Repository Intelligence Report — Output Contract

The final report must be useful to an architect and auditable by an engineer.

## Report Altitudes
Every report is written at three altitudes, in this order, so each reader can stop when they have enough. All three are written from the same claims ledger; the upper levels add no facts.

| Level | Section | Reader | Length |
|---|---|---|---|
| 1 | Management Summary | Leadership, sponsors | ≤150 words, plain language |
| 2 | Architect Brief | Architects, tech leads | ≤400 words |
| 3 | Forensic Detail (sections 1–17) | Engineers, auditors | as needed |

The report describes **where the system is today**: the Repository State. It does not decide where the system should go; that is the owners' intent. Options are offered as options.

Tone: objective and neutral throughout (Evidence Policy Rule 17). Describe state, not merit. Strengths and attention areas meet the same evidence bar.

## Level 1 — Management Summary
At most 150 words. Plain language: no file paths, code, or code-formatted terms. Cite claim IDs in brackets.

Required fields:
- **Where it is today** — what the system is and how far it has progressed, in one or two sentences.
- **Current credible radius** — the highest of the five radii (below) the evidence supports, in plain words.
- **What's working** — up to 3 evidenced strengths.
- **Attention areas** — up to 3, stated as conditions, not faults.
- **Questions to settle before setting direction** — up to 3, for the owners.

## Level 2 — Architect Brief
At most 400 words. Every bullet cites claim IDs.

Required fields:
- **What it is** — one or two sentences.
- **Shape** — entry points, major components, runtime/platform.
- **Where the intelligence is** — what is model-driven vs deterministic (or "not applicable").
- **Implemented vs planned** — what is implemented and evidenced vs what is documented, configured, or provisioned without implementation found.
- **Radius position** — this table, one row per radius:

  | Radius | Status | Basis |
  |---|---|---|
  | 1 Intent & Discovery | ... | claim IDs |
  | 2 Prototype & Proof | ... | ... |
  | 3 Engineering & Integration | ... | ... |
  | 4 Delivery & Production | ... | ... |
  | 5 Enterprise Operation & Governance | ... | ... |

  Status vocabulary: `EVIDENCED` · `PARTIAL` · `NOT YET EVIDENCED` · `OUT OF SCOPE` (only when the repo's own intent or docs scope it out; cite that) · `UNKNOWN`. A radius beyond the repo's stated intent is OUT OF SCOPE, not a gap.
- **Attention areas** — at most 3.
- **Biggest unknowns** — at most 3.
- **Smallest next step outward** — one option to move up one radius, with the proof it would need. Offered as an option for the owners, not a prescription.

## Level 3 — Forensic Detail

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

## 13. Alignment Gaps (Contradictions / Drift)
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
- what could change it (static-only analysis, absence claim, sampled coverage, documented-not-observed);
- the cheapest check that would confirm it (a command, a console, a person).

Prioritize high-impact claims, absence claims, and anything resting on documentation alone.

## Prohibited Output
The report must not:
- invent facts to make sections feel complete;
- hide uncertainty behind polished prose;
- cite files that do not contain the claimed evidence;
- claim production reality from repository artifacts alone;
- state an absence as fact ("X is never used") instead of a scoped finding ("no use of X found in <scope>");
- present generic framework knowledge as repository-specific evidence;
- use loaded or judgmental language, or attribute motive or carelessness to the authors (Evidence Policy Rule 17).
