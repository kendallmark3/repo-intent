# Repository Intelligence Report — Clinical-Evidence-Coordinator

## Management Summary

- **Where it is today:** A working reference prototype that checks whether a synthetic clinical-study evidence package is complete enough for a human reviewer. It runs locally with automated tests; cloud deployment and the AI model path are set up but not yet exercised [C-001, C-034, C-023, C-025].
- **Current credible radius:** Radius 2 of 5 (Prototype & Proof), with parts of Radius 3 in place [C-005, C-021].
- **What's working:** Rules, not the AI, make the final call, and a person always reviews [C-008, C-030]. Cloud-specific code is kept apart from business logic [C-021]. Tests cover the main scenarios [C-034].
- **Attention areas:** No sign-in was found on the API [C-027]. Records from simultaneous runs can overwrite each other [C-015].
- **Questions to settle before setting direction:** Is this a teaching reference or a path to production [C-035]? Who owns the AWS account and model access [C-024, C-025]?

## Architect Brief

- **What it is:** a reference implementation that checks whether a *synthetic* clinical-study evidence package is ready for a human reviewer; it makes no clinical or regulatory decisions [C-001, C-030, C-035].
- **Shape:** one Python/FastAPI service with two entry points: a local API with an upload page, and an Amazon Bedrock AgentCore runtime entry. AWS code is kept at the edges [C-002, C-003, C-021].
- **Where the intelligence is:** one model-backed step, Document Intake, which proposes requirement matches for uploaded PDFs. The other four "agents" and the final verdict are deterministic rules, and model output fails closed [C-006, C-007, C-008, C-009].
- **Implemented vs planned:**
  - *Implemented:* the local pipeline, fail-closed rules, the keyword mock, CI, and 18 tests [C-005, C-032, C-022, C-034].
  - *Planned or configured, no implementation found:* a Bedrock run, AgentCore deployment (dry-run only), S3/DynamoDB use, and App Runner (listed in the intent, not in the Terraform) [C-025, C-023, C-016, C-036].
  - *Descriptive only:* the YAML agent/workflow configs [C-017].
  - On AgentCore, no model call was found [C-012].
- **Radius position:**

  | Radius | Status | Basis |
  |---|---|---|
  | 1 Intent & Discovery | EVIDENCED | Written intent, success criteria, non-goals [C-035, C-001] |
  | 2 Prototype & Proof | PARTIAL | Working pipeline and tests [C-005, C-034]; model path not yet run [C-025] |
  | 3 Engineering & Integration | PARTIAL | Clean adapter boundary [C-021, C-003]; state/artifact interfaces and configs not wired [C-016, C-017] |
  | 4 Delivery & Production | NOT YET EVIDENCED | CI and deploy dry-run [C-022, C-023]; deployment unknown [C-024]; no API auth found [C-027] |
  | 5 Enterprise Operation & Governance | OUT OF SCOPE | Repo defines itself as a reference implementation with clinical/regulatory non-goals [C-035] |

- **Attention areas:**
  1. No authentication found on the API [C-027].
  2. Prompt-injection surface; no check of model claims against the source was found [C-029].
  3. Concurrent runs overwrite each other's audit artifacts [C-015].
- **Biggest unknowns:**
  1. Whether the Bedrock path and its default model ID work [C-025].
  2. Whether anything is deployed [C-024].
  3. Model classification accuracy; no evaluation set was found [C-029].
- **Smallest next step outward (option for the owners):** complete Radius 2 with one recorded `PROVIDER_MODE=bedrock` run over the three sample scenarios plus a small labeled evaluation set. Proof: scenario verdicts match the README's expected results and classification accuracy is recorded [C-025, C-029].

## 1. Repository Identity
- **Repository:** https://github.com/kendallmark3/Clinical-Evidence-Coordinator
- **Commit SHA:** `71f250e7d5cf89f406e0cd8eebb2873f4e498b75` (2026-10-25, "docs: add Clinical Evidence Coordinator case study with workflow graphics")
- **Analysis date:** 2026-10-29
- **Languages/frameworks observed:** Python 3.12 / FastAPI / Pydantic (application), TypeScript / AWS CDK (AgentCore CLI-generated infra), Terraform (starter IaC), static HTML frontend.
- **Limitations:** Static, read-only inspection. No code was installed, built, or executed; tests were read, not run. Binary artifacts (sample PDFs, images, case-study zip) were not inspected. `agentcore/cdk/bin/cdk.ts`, `docs/` long-form prose, and `frontend/index.html` were sampled, not read in full.

## 2. Executive Orientation
- A demo/starter that checks whether a **synthetic clinical-study evidence package** is complete enough to hand to a human reviewer. It explicitly does not make clinical or regulatory decisions [C-001, C-030].
- Shape: one Python service with **two entry points** — a FastAPI app for local use and an Amazon Bedrock AgentCore runtime entry point [C-002, C-003].
- Of five "agents", **only Document Intake calls a model**; the other four are plain deterministic Python. A deterministic validator makes the final readiness call ("the model proposes, the rules decide") [C-006, C-007, C-008].
- **No model call was found on the AgentCore path.** It accepts JSON packages only, so the Bedrock provider is reachable only through the local FastAPI upload endpoint [C-012, C-013].
- Persistence is local JSON files with fixed names. Terraform provisions S3 and DynamoDB, but no code using them was found [C-014, C-016].
- Most important uncertainty: whether the Bedrock path works at all, and whether anything is deployed. Neither can be established from the repo, and the README says neither has happened [C-024, C-025].

## 3. Coverage & Confidence
- **Read in full:** all of `backend/app/` (application code), `agentcore_app.py`, `config/*.yaml`, `agent-manifest.yaml`, `Dockerfile`, `Makefile`, `requirements.txt`, `pyproject.toml`, both GitHub workflows, `agentcore/agentcore.json`, `infrastructure/terraform/main.tf` + `variables.tf`, `README.md`.
- **Sampled:** test files (setup + test names), `agentcore/cdk/lib/cdk-stack.ts` (conditionals), `docs/AI_ANALYSIS.md`, `CLAUDE.md` (targeted lines), `intents/Feature.md` (headings only).
- **Not inspected:** PDFs, images, `case-study/`, `scripts/make_synthetic_pdfs.py`, `prompts/*.md` content.
- Confidence is high for code structure and flow; there is no runtime evidence for any deployed or model-backed behavior.

## 4. System Purpose
- **Documented:** reviews synthetic clinical-study evidence packages for structural completeness, consistency, and traceability [C-001].
- **Implemented:** every run ends in exactly one of `READY_FOR_HUMAN_REVIEW` / `NOT_READY_FOR_HUMAN_REVIEW`, and human review is always required [C-008, C-030].
- **Documented intent:** a reference implementation for multi-agent orchestration, not a medical decision system, with explicit non-goals [C-035]. The README calls itself a starter repo for learning, and the manifest declares synthetic data only [C-028].
- **Unknowns:** real-world users and deployment [C-024].

## 5. Entry Points & Execution Paths
| Entry point | How it is started | Evidence |
|---|---|---|
| FastAPI `app` (5 routes) | `uvicorn backend.app.main:app` (Dockerfile, Makefile) | [C-002, C-004] |
| AgentCore `invoke` | `BedrockAgentCoreApp` entrypoint; `agentcore.json` points at `agentcore_app.py` | [C-003] |
| `scripts/run_demo.py`, `scripts/make_synthetic_pdfs.py` | dev utilities (not read in depth) | — |

**Representative flow A — PDF upload (local only):** `POST /api/review/documents` → size/count/`%PDF` checks → `pypdf` text extraction → `Orchestrator.run_documents` → `DocumentIntakeAgent` (model or mock proposes requirement IDs + status per doc; output shape-checked; fails closed) → standard pipeline below [C-026, C-007].

**Representative flow B — standard pipeline (both entry points):** `Orchestrator.run`: normalize-requirements → map-evidence → inspect-quality → prepare-human-review → deterministic-validation, each step writing a JSON artifact [C-005, C-014].

## 6. Component Map
| Component | Responsibility | Key files | Claims |
|---|---|---|---|
| API | HTTP surface, upload validation, serves the frontend | `backend/app/main.py` | C-002, C-004, C-026 |
| AgentCore entry | AgentCore runtime → adapter → orchestrator | `agentcore_app.py`, `backend/app/runtime/agentcore_adapter.py` | C-003, C-012 |
| Orchestrator | Fixed 5-step sequence; explicit `WorkflowState` | `backend/app/orchestration/orchestrator.py` | C-005 |
| Document Intake Agent | Only model-backed step; fail-closed parsing | `backend/app/agents/document_intake_agent.py` | C-006, C-007, C-029 |
| Requirements / Evidence / Quality / Review agents | Deterministic transforms and checks | `backend/app/agents/*.py` | C-006, C-009 |
| Validator | Final readiness rule | `backend/app/validation/validator.py` | C-008 |
| Providers | `mock` (keyword match) or `bedrock` (Claude) chosen by env | `backend/app/providers/` | C-010, C-011, C-032 |
| Platform contracts | Abstract interfaces; two are unimplemented | `backend/app/platform/contracts.py` | C-016, C-020 |

## 7. Data Flow & Persistence
- **Inputs:** a JSON `StudyPackage` (requirements + evidence items) or uploaded PDFs + requirements [C-031, C-026].
- **Transformations:** see flows A/B above.
- **Persistence:** `ArtifactStore` writes JSON files with fixed names into `ARTIFACT_DIR`. No database client use was found in application code [C-014]. Concurrent runs would overwrite each other's artifacts; the repo's own analysis doc acknowledges this [C-015].
- **Outputs:** a `ReviewResponse` with status, missing requirement IDs, blocking findings, and all intermediate artifacts inline [C-008].
- **Provisioned, not wired:** S3 and DynamoDB appear in Terraform; no application use was found [C-016].

## 8. External Integrations
| Integration | Evidence | Usage |
|---|---|---|
| Claude on Amazon Bedrock (via `anthropic` SDK `AnthropicBedrockMantle`) | C-011 | Direct but **optional**: only when `PROVIDER_MODE=bedrock`, only on the upload path. Never run, per the README [C-025] |
| Amazon Bedrock AgentCore Runtime | C-003, C-023 | Configured; deploy is dry-run only |
| AWS ECR / S3 / DynamoDB | C-016 | Provisioned by Terraform; no code use found |
| GitHub Actions + AWS OIDC role | C-022, C-023 | CI on push/PR; manual deploy dry-run |

## 9. Interfaces / APIs
- HTTP: `GET /`, `GET /api/health`, `GET /api/config/status`, `POST /api/review` (JSON), `POST /api/review/documents` (multipart) [C-004].
- AgentCore: `/ping` and `/invocations` (exercised by tests) [C-003, C-034].
- Data contract: `schemas/study-package.schema.json` plus Pydantic models [C-031]. Whether the two agree was not checked.

## 10. Build / Test / Deploy / Operate
- Build: Dockerfile (python:3.12-slim, defaults to mock provider) [C-002].
- Test: 18 pytest test functions across 4 files, covering the workflow, fail-closed intake, adapter parity, and the AgentCore entry point. Tests use mock/fixed providers only [C-034, C-025].
- CI: compile + pytest + docker build [C-022].
- Deploy: manual workflow; `agentcore deploy --dry-run` only, with the real deploy step commented out [C-023]. The CDK stack is CLI-generated; its payment/MCP constructs are conditional and not activated by current config [C-033].
- Live environment: UNKNOWN [C-024].

## 11. Security & Authentication Evidence
- No authentication was found on the FastAPI routes in `backend/app/main.py`; a gateway outside the repo could still provide it [C-027].
- Upload guards: ≤20 files, ≤10 MB each, `%PDF` magic-byte check [C-026].
- Model safety: shape validation with fail-closed defaults, unknown requirement IDs block readiness, and a deterministic final rule [C-007, C-009, C-008].
- **Prompt-injection surface:** raw document text is inserted into the model prompt. The guards above limit what a manipulated model answer can do, but no check of the model's claims against the source text was found, and the repo's own analysis doc says the same [C-029].
- "Synthetic data only / no PHI" is declared; no code enforcing it was found [C-028].
- CI deploy uses an OIDC-assumed role with `contents: read` [C-023].
- None of this establishes that the system is secure.

## 12. Domain / Business Concepts
Directly named in code: study package, protocol requirement (`evidence_required`), evidence item (`complete` / `incomplete` / `missing`), readiness status, blocking finding, human review [C-031, C-030]. Requirement content (e.g. adverse-event reconciliation) comes from sample data, not code.

## 13. Alignment Gaps (Contradictions / Drift)
- **Acknowledged drift:** `config/agents.yaml`, `config/workflow.yaml`, `agent-manifest.yaml`, and four of five prompt files describe the design, but no code loading them was found. The repo's own CLAUDE.md and AI_ANALYSIS.md say so [C-017].
- `agent-manifest.yaml` lists four workers and omits `document_intake`, which `config/agents.yaml` defines [C-018].
- Version labels disagree: API `0.2.0` vs package `0.1.0` vs manifest/workflow `"0.1"` [C-019].
- Two overlapping model-provider abstractions exist; no use of the platform one was found [C-020].
- `PROVIDER_MODE` is set in `agentcore.json`, but no provider use was found on the AgentCore path [C-013].
- README line 5 headlines "AgentCore Runtime → Bedrock" while its own status table says Bedrock has not run and AgentCore does not take documents. The README qualifies itself; read the headline as the planned path [C-024, C-025].
- The intent's engineering criteria list App Runner in the Terraform starter; the Terraform omits it, with a comment explaining why [C-036].

## 14. Important Unknowns
| Unknown | Why the repo can't establish it | What would resolve it |
|---|---|---|
| Does the Bedrock path work, and is `anthropic.claude-opus-5` a valid model ID for the target account/region? [C-025] | No test or run evidence; README says never run | One real `PROVIDER_MODE=bedrock` run against scenario 1 |
| Is anything deployed? [C-024] | Deploy workflow is dry-run only | AWS account inspection / AgentCore console |
| Model classification accuracy [C-029] | No evaluation set was found in the repo | A labeled set over the three scenarios plus adversarial PDFs |

## 15. Claims Ledger

| ID | Claim | Class | Strength | Confidence | Evidence | Verification | Caveat |
|---|---|---|---|---|---|---|---|
| C-001 | The system assesses readiness of synthetic clinical-study evidence packages for human review and disclaims clinical/regulatory decisions | OBSERVED | CORROBORATED | HIGH | `README.md:L7#synthetic`; `backend/app/agents/review_agent.py:L22-L25#decision_boundary`; `backend/app/validation/validator.py:L18#READY_FOR_HUMAN_REVIEW` | VERIFIED | Purpose wording is from README; code corroborates the readiness-only output |
| C-002 | The primary local entry point is the FastAPI `app` in `backend/app/main.py`, started by uvicorn | OBSERVED | CORROBORATED | HIGH | `backend/app/main.py:L18-L22#FastAPI`; `Dockerfile:L14#backend.app.main:app`; `Makefile:L11#uvicorn` | VERIFIED | — |
| C-003 | A second entry point, `agentcore_app.py`, exposes an AgentCore runtime that validates a `StudyPackage` and calls the orchestrator via an adapter | OBSERVED | CORROBORATED | HIGH | `agentcore_app.py:L18-L31#entrypoint`; `agentcore/agentcore.json:L14#agentcore_app.py`; `backend/tests/test_agentcore_entrypoint.py:L20-L21#ping` | VERIFIED | — |
| C-004 | The API exposes five routes: `/`, `/api/health`, `/api/config/status`, `POST /api/review`, `POST /api/review/documents` | OBSERVED | DIRECT | HIGH | `backend/app/main.py:L24-L46#/api/review` | VERIFIED | — |
| C-005 | `Orchestrator.run` is a fixed five-step Python sequence with explicit `WorkflowState` | OBSERVED | DIRECT | HIGH | `backend/app/orchestration/orchestrator.py:L41-L84#current_step`; `backend/app/orchestration/state_manager.py:L5-L16#WorkflowState` | VERIFIED | — |
| C-006 | Only `DocumentIntakeAgent` calls a model provider; the Requirements, Evidence, Quality, and Review agents are deterministic Python | OBSERVED | CORROBORATED | HIGH | `backend/app/agents/document_intake_agent.py:L61#generate`; `backend/app/agents/requirements_agent.py:L6-L18#run`; `backend/app/agents/evidence_agent.py:L6-L25#run`; `backend/app/agents/quality_agent.py:L7-L39#run`; `backend/app/agents/review_agent.py:L6-L26#run`; `README.md:L20#no LLM` | VERIFIED | Absence of provider calls in the four agents confirmed by full read + grep |
| C-007 | Model output is shape-checked; any provider error, non-JSON reply, invalid IDs, or invalid status fails closed to an empty requirement list with status incomplete | OBSERVED | CORROBORATED | HIGH | `backend/app/agents/document_intake_agent.py:L60-L97#_fail_closed`; `backend/tests/test_document_intake.py:L71#test_bad_model_output_fails_closed` | VERIFIED | — |
| C-008 | Final readiness is decided by the deterministic validator: every required requirement needs complete evidence and the blocking-findings list must be empty | OBSERVED | DIRECT | HIGH | `backend/app/validation/validator.py:L1-L27#ready`; `backend/app/orchestration/orchestrator.py:L77-L82#validate` | VERIFIED | — |
| C-009 | A model that invents requirement IDs cannot make a package ready; unknown IDs become blocking findings | OBSERVED | CORROBORATED | HIGH | `backend/app/agents/quality_agent.py:L21-L26#unknown requirement`; `backend/tests/test_document_intake.py:L77#test_model_cannot_invent_requirements` | VERIFIED | `_parse` itself accepts any string IDs; the block happens downstream |
| C-010 | The provider is selected by the `PROVIDER_MODE` env var and defaults to `mock` | OBSERVED | CORROBORATED | HIGH | `backend/app/config.py:L6#PROVIDER_MODE`; `backend/app/providers/factory.py:L6-L12#mock` | VERIFIED | — |
| C-011 | `BedrockProvider` calls Claude through the `anthropic` SDK's `AnthropicBedrockMantle` client, with default model ID `anthropic.claude-opus-5` | OBSERVED | DIRECT | HIGH | `backend/app/providers/bedrock_provider.py:L3-L20#AnthropicBedrockMantle` | VERIFIED | Validity of the model ID is C-025 |
| C-012 | On the AgentCore path, no model call was found: the adapter builds an `Orchestrator` without a provider, and no use of `self.provider` was observed in `run` | OBSERVED | CORROBORATED | HIGH | `backend/app/runtime/agentcore_adapter.py:L20-L24#Orchestrator(artifact_dir)`; `backend/app/orchestration/orchestrator.py:L41-L91#def run`; `README.md:L46#JSON study packages only` | VERIFIED | Search scope: full read of `orchestrator.py`, `agentcore_adapter.py`, `agentcore_app.py`; second pass grepped `run` for `provider` |
| C-013 | No effect of `PROVIDER_MODE` on the AgentCore path was found; the env var in `agentcore.json` appears inert there | INFERRED | CORROBORATED | HIGH | `agentcore/agentcore.json:L21-L22#PROVIDER_MODE`; `backend/app/runtime/agentcore_adapter.py:L21#Orchestrator(artifact_dir)` | VERIFIED | Search scope: derived from C-012; would change if documents were routed through AgentCore |
| C-014 | Persistence observed is local JSON files with fixed names in `ARTIFACT_DIR`; no database client use was found in application code | OBSERVED | CORROBORATED | HIGH | `backend/app/orchestration/artifact_store.py:L9-L12#write_text`; `backend/app/orchestration/orchestrator.py:L49#requirements.json`; `backend/app/config.py:L9#ARTIFACT_DIR` | VERIFIED | Search scope: full read of `backend/app/`; grep of all `.py` for boto3, dynamodb, s3, sqlalchemy |
| C-015 | Concurrent runs would overwrite each other's artifacts | INFERRED | CORROBORATED | HIGH | `backend/app/orchestration/artifact_store.py:L9-L11#name`; `docs/AI_ANALYSIS.md:L62#overwrite` | VERIFIED | Inferred from fixed filenames; not observed at runtime |
| C-016 | Terraform provisions ECR, S3, and DynamoDB; no implementations of `StateRepository` or `ArtifactRepository` and no S3/DynamoDB client code were found | OBSERVED | CORROBORATED | HIGH | `infrastructure/terraform/main.tf:L15-L46#aws_dynamodb_table`; `backend/app/platform/contracts.py:L14-L26#ArtifactRepository`; `README.md:L36#optional` | VERIFIED | Search scope: repo-wide grep of `.py` for the interface names and boto3; another repo or a later layer could consume these resources |
| C-017 | No code was found that loads the YAML configs, `agent-manifest.yaml`, or any prompt except `document_intake.md`; the repo documents this itself | OBSERVED | CORROBORATED | HIGH | `backend/app/agents/document_intake_agent.py:L8#document_intake.md`; `CLAUDE.md:L27#not loaded at runtime`; `docs/AI_ANALYSIS.md:L63#no code reads them` | VERIFIED | Search scope: grep of `.py`, Makefile, Dockerfile, and TOML for `yaml`, `config/`, `prompts/`; PyYAML is declared but no import was found |
| C-018 | `agent-manifest.yaml` lists four workers and omits `document_intake`, which `config/agents.yaml` defines | CONTRADICTED | DIRECT | HIGH | `agent-manifest.yaml:L12-L16#workers`; `config/agents.yaml:L2-L3#DocumentIntakeAgent` | VERIFIED | Descriptive files only (C-017); no runtime impact |
| C-019 | Version labels disagree across API, package, and manifests | CONTRADICTED | DIRECT | HIGH | `backend/app/main.py:L20#0.2.0`; `pyproject.toml:L6#0.1.0`; `agent-manifest.yaml:L3#0.1` | VERIFIED | Cosmetic |
| C-020 | Two overlapping provider abstractions exist; both providers extend `providers.base.Provider`, and no use of `platform.contracts.ModelProvider` was found | OBSERVED | CORROBORATED | HIGH | `backend/app/providers/base.py:L3-L8#Provider`; `backend/app/platform/contracts.py:L4-L7#ModelProvider`; `backend/app/providers/bedrock_provider.py:L5#BedrockProvider(Provider)` | VERIFIED | Search scope: grep of all `.py` for `ModelProvider` |
| C-021 | Cloud SDK imports were found only in `agentcore_app.py` and the lazily imported Bedrock provider; none were observed in domain agents, orchestration, or validation | OBSERVED | CORROBORATED | HIGH | `agentcore_app.py:L11#bedrock_agentcore`; `backend/app/providers/bedrock_provider.py:L15-L16#import AnthropicBedrockMantle`; `backend/app/runtime/agentcore_adapter.py:L1-L14#NOT` | VERIFIED | Search scope: grep of `backend/`, `scripts/`, `agentcore_app.py` for boto3, anthropic, bedrock_agentcore, aws |
| C-022 | CI compiles, runs pytest, and builds the Docker image on push to main/feature branches and on PRs | OBSERVED | DIRECT | HIGH | `.github/workflows/ci.yml:L3-L32#docker build` | VERIFIED | Whether CI currently passes is unknown |
| C-023 | The AgentCore deploy workflow is manual, assumes an AWS role via OIDC, and only runs `agentcore deploy --dry-run`; the real deploy is commented out | OBSERVED | DIRECT | HIGH | `.github/workflows/agentcore-deploy.yml:L3-L4#workflow_dispatch`; `.github/workflows/agentcore-deploy.yml:L34-L38#role-to-assume`; `.github/workflows/agentcore-deploy.yml:L57-L63#dry-run` | VERIFIED | — |
| C-024 | Whether any environment is deployed cannot be established from the repo; the README states it is not deployed | UNKNOWN | INSUFFICIENT | LOW | `README.md:L45#Not deployed` | VERIFIED | Documented status only |
| C-025 | Whether the Bedrock provider works, including the default model ID, is unknown; the README says it has not been run and no test exercises it | UNKNOWN | INSUFFICIENT | LOW | `README.md:L44#not yet run`; `backend/tests/test_document_intake.py:L24-L41#FixedProvider` | VERIFIED | — |
| C-026 | The upload endpoint accepts at most 20 files of ≤10 MB, rejects non-`%PDF` content, and extracts text with pypdf | OBSERVED | DIRECT | HIGH | `backend/app/main.py:L15-L16#MAX_FILE_BYTES`; `backend/app/main.py:L59-L69#%PDF`; `backend/app/documents/pdf_text.py:L6-L12#PdfReader` | VERIFIED | — |
| C-027 | No authentication or authorization was found on the FastAPI routes | OBSERVED | CORROBORATED | MEDIUM | `backend/app/main.py:L18-L46#app.post` | VERIFIED | Search scope: full read of `backend/app/main.py`; an upstream gateway or AgentCore-level auth outside the repo could still apply |
| C-028 | "Synthetic data only / no PHI" is declared in the manifest and hard-coded in the status endpoint; no code enforcing it was found | OBSERVED | CORROBORATED | HIGH | `agent-manifest.yaml:L28-L30#phi_allowed`; `backend/app/main.py:L38#synthetic_data_only` | VERIFIED | Search scope: full read of the upload path (`main.py`, `pdf_text.py`, `document_intake_agent.py`) |
| C-029 | Raw document text goes straight into the model prompt, so a crafted PDF could steer classification; downstream rules limit the impact, but no check of the model's claims against the source text was found | INFERRED | CORROBORATED | MEDIUM | `backend/app/agents/document_intake_agent.py:L55-L59#<document>`; `docs/AI_ANALYSIS.md:L57#Nothing checks the model` | QUALIFIED | Search scope: full read of intake, quality, and validator modules; severity untested; a manipulated model could still mark a real requirement complete |
| C-030 | Human review is always required: the response model, validator, and review agent all hard-set it | OBSERVED | CORROBORATED | HIGH | `backend/app/models.py:L29#human_review_required`; `backend/app/validation/validator.py:L19#human_review_required`; `backend/app/agents/review_agent.py:L21#human_review_required` | VERIFIED | — |
| C-031 | Core domain types are `StudyPackage`, `ProtocolRequirement` (with `evidence_required`), and `EvidenceItem` with status complete/incomplete/missing | OBSERVED | DIRECT | HIGH | `backend/app/models.py:L4-L23#EvidenceStatus` | VERIFIED | — |
| C-032 | The mock provider is keyword matching, explicitly "not AI", marking documents incomplete on draft/pending/partial | OBSERVED | DIRECT | HIGH | `backend/app/providers/mock_provider.py:L11-L21#Not AI` | VERIFIED | — |
| C-033 | The CDK stack is AgentCore-CLI-generated; its MCP and payment constructs are conditional and current config enables neither | INFERRED | CORROBORATED | HIGH | `agentcore/agentcore.json:L7#agentcore-cli`; `agentcore/agentcore.json:L36#agentCoreGateways`; `agentcore/agentcore.json:L43#payments`; `agentcore/cdk/lib/cdk-stack.ts:L128-L130#agentCoreGateways`; `agentcore/cdk/lib/cdk-stack.ts:L139-L141#paymentSpec` | VERIFIED | Payment IAM grants exist in generated code but are not activated |
| C-034 | 18 pytest test functions across 4 files cover the workflow, fail-closed intake, local-vs-AgentCore adapter parity, and the AgentCore HTTP entry point | OBSERVED | DIRECT | HIGH | `backend/tests/test_runtime_adapters.py:L11#test_local_and_agentcore_adapters_preserve_domain_result`; `backend/tests/test_workflow.py:L10-L30#def test`; `backend/tests/test_agentcore_entrypoint.py:L20-L33#def test`; `backend/tests/test_document_intake.py:L43-L102#def test` | VERIFIED | Counted from `def test` lines; parametrized cases not expanded; tests not executed |
| C-035 | The repo's own intent defines it as a reference implementation for multi-agent orchestration, not a medical decision system, and lists non-goals including PHI, production clinical data, and regulatory decisions | OBSERVED | DIRECT | HIGH | `intents/Feature.md:L7#reference implementation`; `intents/Feature.md:L169-L179#Non-Goals` | VERIFIED | Documented intent; the Radius 5 OUT OF SCOPE status rests on it |
| C-036 | The intent's engineering criteria say the Terraform starter supports App Runner; the Terraform omits App Runner, with a comment explaining the choice | CONTRADICTED | DIRECT | HIGH | `intents/Feature.md:L166#App Runner`; `infrastructure/terraform/main.tf:L48-L50#App Runner is intentionally omitted` | VERIFIED | Explained in a comment; documentation drift, not hidden |

## 16. Next Inspection Targets
| Target | Uncertainty it resolves | Value |
|---|---|---|
| Run `pytest -q` locally | Whether the 18 tests pass at this SHA | High; cheap |
| One `PROVIDER_MODE=bedrock` run on `samples/scenarios/1-ready` | C-025: does the model path work at all | High; the core AI claim is untested |
| `prompts/document_intake.md` + an adversarial PDF | C-029: practical prompt-injection exposure | Medium-High |
| `schemas/study-package.schema.json` vs `backend/app/models.py` | Schema/model drift | Medium |

## 17. What I would verify before repeating this in an architecture meeting

| Statement as I'd say it | Claims | What could change it | Cheapest check |
|---|---|---|---|
| "Only one step uses an LLM; everything else is rules." | C-006, C-012 | Static read only; a provider could be reached through a path I didn't trace | `grep -rn "generate(" backend agentcore_app.py` plus a breakpoint run of both entry points |
| "The AgentCore deployment doesn't call a model." | C-012, C-013 | Absence claim; the deployed code could differ from this SHA | Confirm the deployed artifact's commit, then invoke `/invocations` with model logging on |
| "There's no auth on the API." | C-027 | Absence claim; a gateway, ALB, or AgentCore auth outside the repo could cover it | Ask the owner how the service is fronted; check the AWS console |
| "S3 and DynamoDB are provisioned but unused." | C-016 | Absence claim; another service or repo could use them | Check whether the Terraform has been applied, and CloudTrail for data-plane calls |
| "Bedrock has never been run." | C-025 | Documentation only (README status table) | Ask the owner, or run one `PROVIDER_MODE=bedrock` review on scenario 1 |
| "The tests pass." | C-034 | Tests were read, not executed | `pip install -r requirements.txt && pytest -q` |
