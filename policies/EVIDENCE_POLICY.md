# RepoIntent Evidence Policy

This is a hard policy, not guidance.

## Rule 1 — Evidence Before Claim
No material claim may enter the final report until supporting repository evidence has been identified.

## Rule 2 — Exactness
Evidence must support the **exact strength of the wording**.

Bad:
> The application uses PostgreSQL in production.

If the only evidence is a PostgreSQL dependency or development compose file, that wording is too strong.

Better:
> The repository contains PostgreSQL integration/configuration evidence; production use cannot be established from the repository alone.

## Rule 3 — Observation vs Inference
Never present an inference as an observation.

Observed:
> `src/api/server.*` registers routes under `/api`.

Inferred:
> This appears to be the primary HTTP entry point because the application bootstrap imports and starts that server.

## Rule 4 — Unknown Is Success
When evidence is missing, write `UNKNOWN` and state what evidence would resolve it.

## Rule 5 — No Authority by README
README/docs are evidence of documented intent, not automatic proof of implementation.

For material behavior, corroborate important documentation claims against source/config/tests/runtime evidence when possible.

## Rule 6 — No Authority by Source Alone
Source code can also mislead:
- dead code;
- examples;
- unused modules;
- feature flags;
- alternate implementations;
- test fixtures;
- deprecated paths.

Establish reachability/use when material.

## Rule 7 — Dependency Does Not Equal Usage
A manifest entry proves declaration, not execution.

## Rule 8 — Test Does Not Equal Production
Tests establish expected or tested behavior in their scope. They do not prove production configuration or usage.

## Rule 9 — Configuration Must Be Contextualized
Identify whether configuration is:
- default;
- local/development;
- test;
- CI;
- production-labeled;
- example/template;
- unknown.

## Rule 10 — Contradictions Are First-Class Findings
If two sources disagree, do not silently choose one. Record the contradiction and explain which evidence appears stronger and why.

## Rule 11 — Two-Pass Verification for High-Impact Claims
High-impact claims require:
1. discovery evidence;
2. a separate verification pass intended to disprove or qualify the claim.

High-impact examples:
- primary system purpose;
- primary runtime entry point;
- authentication mechanism;
- database/persistence layer;
- external service integration;
- deployment topology;
- architectural boundary.

## Rule 12 — Claims Ledger
Each material claim must capture:
- claim ID;
- claim text;
- classification;
- evidence strength;
- confidence;
- evidence references;
- verification result;
- caveats/unknowns.

## Rule 13 — No Precision Theater
Do not output numeric confidence percentages unless backed by a defined measured calibration process.

## Rule 14 — Cite Primary Repository Evidence
Prefer direct repository artifacts over secondary summaries.

## Rule 15 — Final Self-Audit
Before delivering the report, attempt to invalidate the strongest conclusions.

Ask:
- What else could explain this evidence?
- Is this code actually reachable?
- Could this be test/example/dead code?
- Does another file contradict it?
- Am I claiming production truth from repository intent?
- Am I converting naming conventions into facts?

If the claim weakens under challenge, rewrite it.

## Rule 16 — Absence Claims Are Scoped Findings, Not Facts
A search that finds nothing proves only that the search found nothing. Absence can be hidden by dynamic imports, reflection, string-built names, generated code, external configuration, other repositories, or files outside the inspected scope.

For any claim that something is absent, unused, never called, or unenforced:
- Word it as a finding: "No use of S3 or DynamoDB clients was found in `backend/`", not "The app does not use S3."
- Begin the ledger Caveat with `Search scope:` and state what was searched (paths, patterns, file types) and how (full read, grep, both).
- Evidence strength is at most CORROBORATED; an absence is never DIRECT.
- Name the plausible ways the search could have missed it when they are realistic.

Bad:
> No authentication exists.

Better:
> No authentication or authorization was found on the FastAPI routes in `backend/app/main.py`; an upstream gateway outside the repository could still provide it.

## Rule 17 — Objective, Neutral Language
The report is a map of current state, not a critique. Its readers include the people who built the system.

- Describe state, not merit: "no authentication was found on the API routes", not "the API is insecure".
- State conditions, not faults: "attention areas", not "problems" or "failures" (literal technical terms like "fails closed" are fine).
- Balance: report evidenced strengths with the same rigor as attention areas. Both need claims and evidence.
- Do not judge capabilities beyond the repository's own intent. Out of scope is not a defect (see the Radius position in the report contract).
- No loaded adjectives (broken, sloppy, naive, hacky, messy, toy, flawed, poor, …), no sarcasm, no "just"/"merely"/"only a demo" minimizers, and no guesses about authors' motives or competence.
- Severity is expressed through evidence and impact ("concurrent runs would overwrite audit artifacts"), not through adjectives.

`tools/check_citations.py` rejects a list of loaded terms outside code spans. Passing that list is necessary, not sufficient.
