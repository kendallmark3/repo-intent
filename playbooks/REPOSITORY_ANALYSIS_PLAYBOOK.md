# Repository Analysis Playbook

This playbook defines the analysis behavior, not implementation details.

## Phase 1 — Scope
Establish:
- repo root;
- obvious generated/vendor/build directories;
- dominant languages;
- repository size/shape;
- whether it is monorepo, service, library, CLI, frontend, IaC, or mixed (initial hypothesis only).

Do not deeply read files yet.

## Phase 2 — Map
Build a cheap structural map from repository facts:
- directory tree;
- manifests;
- build files;
- root docs;
- CI/CD files;
- container/IaC files;
- API/schema files;
- test locations;
- likely entry points.

Goal: determine where evidence is likely to live.

## Phase 3 — Discover Signals
Look for high-information signals:
- executable/bootstrap code;
- route/event/job registration;
- dependency injection/composition roots;
- configuration loading;
- persistence initialization;
- external clients;
- domain models;
- tests around central behavior.

Create tentative hypotheses but do not report them yet.

## Phase 4 — Form Claims
Turn hypotheses into candidate claims.

Each candidate claim must specify:
- exact wording;
- why it matters;
- evidence required to establish it;
- possible alternative explanations.

## Phase 5 — Verify
Actively search for corroborating or disconfirming evidence.

For example, if a file looks like the main server:
- who imports it?
- who starts it?
- is it referenced by build/run config?
- is another server entry point present?
- is it example/test-only?

## Phase 6 — Trace Important Flows
Select a few representative high-value flows rather than pretending to trace everything.

Examples:
- request -> handler -> service -> persistence -> response;
- event -> consumer -> domain operation -> outbound event;
- CLI -> command -> service;
- scheduled job -> work -> datastore/API.

Label representative flows as representative.

## Phase 7 — Cross-Source Check
Compare:
- docs vs code;
- tests vs code;
- config vs code;
- deployment vs build artifacts;
- API specs vs route implementations;
- schemas vs models.

Record disagreement.

## Phase 8 — High-Impact Re-Verification
Select the strongest/most consequential conclusions and attempt to disprove them.

No high-impact claim becomes final without this pass.

## Phase 9 — Write Report
Write from the claims ledger, not from memory.

The report prose is a presentation of verified claims—not a fresh generation step that adds new facts.

Write the Architect Brief last, from the finished ledger, and place it first. Then write section 17: the claims you would double-check before saying them aloud in an architecture meeting.

## Phase 10 — Self-Audit
Before completion:
- ensure every material statement maps to a claim;
- ensure every evidence reference exists;
- ensure evidence supports wording strength;
- downgrade unsupported certainty;
- move unresolved conclusions to UNKNOWN;
- reword absence claims as scoped findings with a `Search scope:` caveat;
- ensure contradictions are visible.

## Information-Value Rule
When deciding what to inspect next, choose the artifact most likely to change or validate the current model of the system.

Do not spend tokens reading low-value files simply because they exist.
