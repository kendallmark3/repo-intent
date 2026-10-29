# Intent 001 — RepoIntent V1
## Evidence-Grounded Repository Understanding

### Intent
Create a local-first capability that can inspect an unfamiliar software repository and produce an accurate, concise, evidence-backed explanation of what the repository does, how it is structured, how execution and data flow through it, and what remains unknown.

The capability must favor **accuracy and traceability over completeness or confidence**.

It must not behave like a generic repository summarizer. It must reason from repository evidence, distinguish observation from inference, and refuse to invent missing architecture or business meaning.

---

## Human Zone

### Desired Outcome
A user can point the capability at an unfamiliar checked-out repository and quickly obtain a trustworthy Repository Intelligence Report suitable for initial architecture orientation.

The user should be able to challenge any material conclusion and immediately see the repository evidence that supports it.

### Primary User
An enterprise AI/software architect entering an unfamiliar codebase who needs rapid orientation without spending hours manually validating AI-generated statements.

### Inputs / Context
Minimum required input:
- a readable checked-out software repository.

Potential repository evidence includes:
- source files;
- manifests/package files;
- build files;
- configuration;
- infrastructure-as-code;
- tests;
- API specifications;
- schemas/migrations;
- README/docs/ADRs;
- container/deployment files;
- CI/CD configuration;
- generated metadata where clearly identified.

V1 must not require:
- AWS;
- a hosted service;
- a vector database;
- a graph database;
- MCP;
- Jira;
- Confluence;
- GitHub API access;
- persistent indexing.

Those may be considered later only when evidence demonstrates a need.

### Required Outputs
Produce one Repository Intelligence Report conforming to `contracts/REPORT_CONTRACT.md`.

The report must include:
1. Executive orientation.
2. Confidence/coverage summary.
3. What the system appears to do.
4. Entry points and execution paths.
5. Component/module map.
6. Data flow and persistence.
7. External integrations/dependencies.
8. APIs/interfaces.
9. Build/test/deployment/operations evidence.
10. Security/authentication evidence.
11. Domain/business concepts inferred from the repo.
12. Contradictions and stale documentation signals.
13. Important unknowns.
14. Claims ledger with evidence.
15. Recommended next inspection targets, ranked by information value.

### Success Criteria
V1 succeeds when all of the following are true:

- Every material factual statement has repository evidence.
- Every material inference identifies the observations from which it was derived.
- The system uses `UNKNOWN` when the evidence cannot support a conclusion.
- No fabricated file, symbol, endpoint, dependency, component, service, or behavior appears in the report.
- High-impact claims receive a second verification pass before final output.
- Exact evidence locations are provided at file + symbol/section/line level when practical.
- Documentation is not treated as automatically authoritative.
- Contradictions between docs/config/tests/code are surfaced rather than silently reconciled.
- The report is useful to a technical architect without requiring a follow-up Q&A session to understand the basic system.
- The first version works locally against multiple public repositories without cloud infrastructure.

### Hard Constraints
- **Accuracy > coverage.**
- **Evidence > plausibility.**
- **Unknown > invention.**
- Do not infer organizational ownership, production deployment, real-world usage, compliance status, performance, or security posture unless repository evidence supports those claims.
- Do not equate a dependency declaration with actual runtime usage without corroboration.
- Do not equate a README statement with implemented behavior without corroboration for material claims.
- Do not describe dead/example/test code as production execution without evidence.
- Do not claim an architecture pattern merely because familiar framework files exist.
- Do not introduce cloud infrastructure in V1 merely for sophistication.

### Stop Conditions
Stop analysis and report limitations when:
- the repository cannot be read;
- the repository is mostly generated/binary content and insufficient evidence exists;
- critical conclusions would require external systems unavailable to V1;
- evidence is too contradictory to support a responsible conclusion.

The correct output in those cases is a bounded report with explicit unknowns, not an invented complete architecture.

---

## AI Zone

Claude chooses the implementation approach.

The implementation should preserve the following behavioral stages, but Claude may determine how to realize them:

1. Scope and inventory.
2. Repository map.
3. Signal discovery.
4. Hypothesis formation.
5. Evidence verification.
6. Cross-source contradiction check.
7. High-impact claim re-verification.
8. Report generation.
9. Report self-audit against evidence policy.

Prefer cheap structural evidence before expensive deep reading.

Do not consume the entire repository context unless required.

The system should progressively narrow from global structure to the files/symbols with the highest information value.

---

## Required Reasoning Behavior

### Claim Classes
Every non-trivial conclusion must be classified as one of:
- `OBSERVED`
- `INFERRED`
- `UNKNOWN`
- `CONTRADICTED`

### Evidence Strength
Evidence should be characterized as:
- `DIRECT` — source/config/test/runtime evidence directly demonstrates the claim.
- `CORROBORATED` — multiple independent repo signals agree.
- `INDIRECT` — supports an inference but does not directly establish it.
- `INSUFFICIENT` — cannot responsibly establish the claim.

### Confidence
Use `HIGH`, `MEDIUM`, or `LOW`, but confidence must derive from evidence quality—not model certainty.

### Material Claim Rule
A material claim is any statement about:
- system purpose;
- architecture;
- runtime behavior;
- data flow;
- security/auth;
- persistence;
- integration;
- deployment;
- business/domain meaning;
- ownership/boundary;
- test/build/operational behavior.

Every material claim belongs in the claims ledger.

---

## Acceptance Evidence

Before Intent 001 is considered complete, demonstrate the capability against at least three repositories of different shapes/languages or frameworks.

For each test repository, provide:
- generated report;
- sampled claims with manually verified evidence;
- any unsupported claims discovered;
- missed major components;
- contradictions correctly/incorrectly identified;
- lessons for Intent 002.

At least one test should be a repository the evaluator already understands well.

---

## Definition of Done
Intent 001 is done when the capability can repeatedly provide a fast, useful architectural orientation while making it easy to distinguish **what the repository proves, what the system inferred, and what nobody can know from the repo alone**.
