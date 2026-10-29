# Start Here — Round Two on the Laptop

## Objective
Build and prove **RepoIntent V1**: a local-first, evidence-grounded repository understanding capability.

## What's already in place
- The skill (`/repo-intent`), evidence policy, report contract, playbook, and eval plan.
- A machine-checkable citation format and `tools/check_citations.py` (with tests) so broken evidence is caught before a human reads the report.
- Intent 001 wired into the Progressive Intent loop: `intent/current-feature.md` passes `hooks/pre-implement.sh`.
- Scorecard and failure-log templates so V1 results feed Intent 002.

What is **not** done: running it against real repositories and proving the claims hold up. That is this session.

## Sequence

### 1. Clone and open
Prerequisite: the intent-drive-starter plugin is installed (see README → Prerequisites).
```bash
git clone https://github.com/kendallmark3/repo-intent.git && cd repo-intent
python3 -m unittest discover -s tests && bash hooks/pre-implement.sh
claude
```

### 2. Give Claude the build instruction
> Build Intent 001 from `intent/current-feature.md` and `intents/001-repo-intelligence-v1.md`. Treat `policies/EVIDENCE_POLICY.md` and `contracts/REPORT_CONTRACT.md` as mandatory. Use `playbooks/REPOSITORY_ANALYSIS_PLAYBOOK.md` as the operating model. Do not introduce AWS, a database, embeddings, MCP, or a UI unless the intent cannot be met without them. No unsupported claims are allowed.

### 3. First acceptance test — a repo you know
```bash
git clone --depth 1 <repo-you-know-well> targets/<name>
```
In Claude Code: `/repo-intent targets/<name>`

### 4. Mechanical check
```bash
python3 tools/check_citations.py reports/<name>/REPORT.md --repo targets/<name>
```
Must PASS. It proves citations exist — not that they support the wording.

### 5. Challenge every important claim
> Show me the exact evidence supporting C-00N.

The system passes only if the evidence really supports the wording used.

### 6. Run the evaluation set
Cover at least three shapes from `examples/OPEN_SOURCE_TARGETS.md`. For each, copy `evals/SCORECARD_TEMPLATE.md` to `evals/runs/<name>.md` and fill it in. Log every failure in `evals/FAILURE_LOG.md`.

### 7. Continue or Stop
Feedback on what you observed becomes a delta appended to `intent/current-feature.md` (`templates/delta-template.md`). Only after V1 evidence exists, write Intent 002 to fix the highest-value **repeated** failure.

Do not pre-design Intent 002.
