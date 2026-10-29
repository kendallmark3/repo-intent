# RepoIntent
## Evidence-Grounded Repository Understanding

**Purpose:** Point RepoIntent at an unfamiliar software repository and obtain a fast, evidence-backed explanation of what the system is, how it works, where the important boundaries are, and what remains unknown.

RepoIntent is deliberately **not** a generic "summarize this repo" prompt. It is an evidence-first reasoning workflow designed to reduce confident but unsupported conclusions.

## The Core Promise

> Never assert more than the repository evidence supports.

RepoIntent must distinguish:
- **Observed** — directly supported by repository evidence.
- **Inferred** — reasoned from multiple observed facts; inference path must be shown.
- **Unknown** — insufficient evidence in the repository.
- **Contradicted** — repository evidence conflicts with another claim or document.

Every material claim must be traceable to file paths, symbols, configuration, tests, documentation, or runtime evidence when runtime inspection is allowed.

## V1 Goal

Given a local repo or cloned public GitHub repository, produce a compact **Repository Intelligence Report** that answers:

1. What is this system trying to do?
2. What are its major components and boundaries?
3. Where does execution begin?
4. How does data move through it?
5. What external systems does it depend on?
6. How is it configured, built, tested, deployed, and operated?
7. What security/authentication patterns are visible?
8. What business/domain concepts appear to matter?
9. Where do documentation, tests, code, and configuration disagree?
10. What important things cannot be known from this repository alone?

## Prerequisites

RepoIntent is built on Intent-Driven Engineering and expects the **[intent-drive-starter](https://github.com/kendallmark3/intent-drive-starter)** Claude Code plugin. This repo ships the RepoIntent-specific pieces (skill, policy, contract, checker, evals) plus the starter's intent/context/templates scaffold — it does **not** bundle the starter's plugin skills, agents, or hooks. Install the starter once:

```bash
claude plugin marketplace add kendallmark3/intent-drive-starter && claude plugin install intent-drive-starter@intent-drive-starter
```

That gives you `/intent-drive-starter:start`, the feature-planner and progressive-intent skills, the planner/developer/qa/reviewer agents, and the pre-implement edit gate. See the starter's [install guide](https://github.com/kendallmark3/intent-drive-starter/blob/main/install-plugin.md).

Also required: `git`, `bash`, Python 3.9+ (standard library only), and Claude Code.

## Quick Start

```bash
git clone https://github.com/kendallmark3/repo-intent.git && cd repo-intent
git clone --depth 1 https://github.com/<owner>/<repo>.git targets/<repo>
claude
```

Then in Claude Code:

```text
/repo-intent targets/<repo>
```

The report lands in `reports/<repo>/REPORT.md`. Verify its citations mechanically:

```bash
python3 tools/check_citations.py reports/<repo>/REPORT.md --repo targets/<repo>
```

Then challenge it by hand: *"Show me the evidence for C-003."*

## V1 Is Local-First

Do **not** start with AWS.

The first version should run inside Claude Code against a checked-out repository. Hosting, indexing services, databases, MCP servers, and persistent knowledge graphs are later options only if real usage proves they are necessary.

## Suggested Workflow

1. Open Claude Code in this repository (built on the [intent-drive-starter](https://github.com/kendallmark3/intent-drive-starter) scaffold).
2. Clone the target repository into `targets/` (gitignored).
3. Start with `intents/001-repo-intelligence-v1.md`.
4. Require Claude to follow `policies/EVIDENCE_POLICY.md`.
5. Require the final output to satisfy `contracts/REPORT_CONTRACT.md`.
6. Test against several known open-source repositories using `evals/EVALUATION_PLAN.md`.
7. Only add complexity after evidence shows a specific failure mode.

## Recommended Command to Claude

> Implement Intent 001 exactly as written. Do not add hosting, a UI, a database, embeddings, MCP, or cloud infrastructure unless required by the intent. Preserve the evidence policy and report contract as hard requirements. Build the smallest local-first version that can analyze a checked-out repository accurately.

## Design Principles

- Evidence before explanation.
- Global orientation before local detail.
- Source code outranks generated prose when they conflict.
- Tests describe intended/verified behavior but may be incomplete.
- Runtime evidence outranks static assumptions when available.
- Documentation is evidence, not truth.
- Inferences must expose their supporting observations.
- Unknown is a valid and desirable answer.
- No fabricated files, symbols, endpoints, dependencies, or architecture.
- Minimal sufficient context; do not read the entire repo indiscriminately.
- Separate discovery from verification.
- Verify high-impact claims independently before finalizing.

## Package Contents

| Path | What it is |
|---|---|
| `00-START-HERE.md` | Laptop session sequence for building Intent 001 |
| `intent/current-feature.md` | Progressive Intent working copy of Intent 001 (append deltas here) |
| `intent/project-intent.md` | Project-level purpose and constraints |
| `intents/001-repo-intelligence-v1.md` | Master build intent |
| `policies/EVIDENCE_POLICY.md` | Anti-hallucination rules (hard) |
| `contracts/REPORT_CONTRACT.md` | Report structure + machine-checkable citation format (hard) |
| `playbooks/REPOSITORY_ANALYSIS_PLAYBOOK.md` | Reasoning sequence |
| `.claude/skills/repo-intent/SKILL.md` | The skill — `/repo-intent <target>` |
| `.claude/CLAUDE.md` | Repository rules Claude Code loads automatically |
| `tools/check_citations.py` | Verifies every citation exists, line ranges are in bounds, symbols appear where cited, and the ledger is consistent |
| `evals/EVALUATION_PLAN.md` | How to prove accuracy |
| `evals/SCORECARD_TEMPLATE.md` · `evals/FAILURE_LOG.md` | Per-run audit record and the evidence that chooses Intent 002 |
| `examples/OPEN_SOURCE_TARGETS.md` | Candidate repo shapes for testing |
| `context/` · `templates/` · `hooks/pre-implement.sh` | Intent-Driven Engineering starter scaffold |
| `targets/` (gitignored) · `reports/` | Input repos · output reports |

Tests: `python3 -m unittest discover -s tests` · Intent gate: `bash hooks/pre-implement.sh`

## Future, Not V1

Only after V1 proves useful:
- Multi-repo analysis.
- Git history reasoning.
- Runtime tracing.
- AST / language-server backed code graph.
- MCP connectors for GitHub/GitLab/Jira/Confluence.
- Persistent repository intelligence cache.
- Enterprise governance controls.
- Web UI / architecture visualization.
- AWS-hosted shared service.

The rule is simple: **earn every layer.**
