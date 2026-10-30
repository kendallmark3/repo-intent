# Repository Intelligence Report — MultiAgentSupplyChainSystem

## Management Summary

- **Where it is today:** A working multi-agent prototype: a warehouse photo goes in; an AI model counts items, a supplier is matched, shipping is estimated, and an email, calendar entry and spreadsheet row are sent [C-001, C-004]. It runs locally as four services [C-027].
- **Current credible radius:** Radius 2 of 5 (Prototype & Proof), with parts of Radius 3 in place [C-003, C-010].
- **What's working:** Each agent is a separate service with a capability card [C-003]. Inputs are screened before the AI and database [C-024, C-025]. Shipping uses plain, testable rules [C-012].
- **Attention areas:** The integration layer described in the documentation is not the one that runs [C-016, C-017]. If supplier lookup fails, the order still goes out with placeholder values [C-020].
- **Questions to settle before setting direction:** Who owns this code and its live demo [C-036, C-037]? Should orders require human approval [C-022]?

## Architect Brief

- **What it is:** a photo-to-order demo ending in Gmail/Calendar/Sheets confirmations, with no human step [C-001, C-004, C-022].
- **Shape:** a FastAPI Control Tower (HTTP + WebSocket) plus Vision, Supplier and Logistics agents as separate A2A services. Data lives in AlloyDB with vector search; the target is Google Cloud Run [C-002, C-003, C-010, C-028].
- **Where the intelligence is:** Gemini counts items (with code execution) and writes the search query; embeddings plus AlloyDB similarity pick the supplier; logistics and orchestration are deterministic [C-006, C-007, C-010, C-012].
- **Implemented vs planned:**
  - *Implemented:* the A2A services and discovery, the vector search, and direct Gmail/Calendar/Sheets API calls [C-003, C-010, C-015].
  - *Documented, but not the running path:* routing integrations through the MCP server (the MCP tools are stubs) and emailing the supplier [C-014, C-016, C-017].
  - *Configured, not wired:* the image-based supplier search and the Cloud Run startup of the agents [C-011, C-029].
- **Radius position:**

  | Radius | Status | Basis |
  |---|---|---|
  | 1 Intent & Discovery | PARTIAL | Problem statement in README [C-001]; no intent file, success criteria, or owners found [C-037] |
  | 2 Prototype & Proof | PARTIAL | End-to-end code path [C-004]; tests exercise copies of functions, not the agents [C-032] |
  | 3 Engineering & Integration | PARTIAL | A2A services and AlloyDB search [C-003, C-010]; documented MCP layer not in path [C-016] |
  | 4 Delivery & Production | NOT YET EVIDENCED | Deploy script exists [C-028]; deployed startup covers only the Control Tower [C-029]; no CI found [C-035] |
  | 5 Enterprise Operation & Governance | NOT YET EVIDENCED | Autonomous external side effects with no approval step found [C-022, C-028] |

- **Attention areas:**
  1. Supplier errors fall through to placeholder values, and the order proceeds [C-020].
  2. The public deployment can trigger real Workspace writes under a fixed account [C-018, C-028].
  3. Docs and code differ on integrations, DB auth and determinism [C-016, C-031, C-008].
- **Biggest unknowns:**
  1. What the live demo runs [C-036, C-029].
  2. Ownership and provenance of the code [C-037].
  3. How consistent the counts are [C-008].
- **Smallest next step outward (option for the owners):** make Radius 2 provable. Point the existing tests at the real agent modules, and stop the pipeline when the supplier reply is not valid JSON. Proof: tests import agent code and a forced supplier error produces no order [C-032, C-020].

## 1. Repository Identity
- **Repository:** https://github.com/kendallmark3/MultiAgentSupplyChainSystem
- **Commit SHA:** `d372e0f6bbd24d0105b86212889d2b35c4dd83f0` (2026-04-27, "Update README.md")
- **Analysis date:** 2026-10-29
- **Languages/frameworks observed:** Python (FastAPI, Starlette, a2a-sdk, google-genai, AlloyDB connector, FastMCP), vanilla JS frontend, PostgreSQL/AlloyDB SQL, shell deployment scripts.
- **Limitations:** Static, read-only inspection. Nothing was installed or executed, including tests. The live demo URL was not visited. Images were not inspected. `frontend/static/app.js`, `setup.sh`, `deploy/cleanup.sh`, the agent READMEs, and `database/seed.py` were sampled or skipped.

## 2. Executive Orientation
- Purpose as documented: automate shelf counting and reordering from a photo [C-001].
- One Control Tower orchestrates three A2A agents in a fixed sequence, then calls Google Workspace APIs [C-004, C-015].
- AI is used for counting and query writing (Gemini) and for embeddings (Vertex). Supplier choice is nearest-vector lookup; shipping is a lookup table [C-006, C-007, C-010, C-012].
- Several documented behaviors differ from the code: the MCP path, the email recipient, IAM DB auth, and "deterministic" vision [C-016, C-017, C-031, C-008].
- The most important uncertainty is what is actually deployed at the live demo URL [C-036].

## 3. Coverage & Confidence
- **Read in full or in the relevant parts:** `frontend/app.py` (orchestration, integrations, routes), `frontend/mcp_server.py`, `agents/vision-agent/agent.py`, the supplier `agent_executor.py` + `inventory.py` (connection, search, executor), `agents/logistics-agent/shipping.py` (location lookup), `Dockerfile`, `deploy/deploy.sh`, `deploy/start.sh`, `run.sh` (relevant parts), `README.md`, test structure, `.dockerignore`, `frontend/requirements.txt`, `database/seed_data.sql` (schema, index, suppliers).
- **Confidence:** high for the code paths traced; low for anything about the deployed demo.

## 4. System Purpose
- **Documented:** replace manual shelf counting and reordering end to end, with no human required [C-001, C-022].
- **Implemented:** image → count → text query → nearest supplier part → shipping estimate → Gmail/Calendar/Sheets writes [C-004, C-015].
- **Unknowns:** intended users, ownership, and whether this is a learning project or a product [C-037].

## 5. Entry Points & Execution Paths
| Entry point | Start | Claims |
|---|---|---|
| Control Tower `frontend/app.py` (port 8080) | `run.sh` locally; Dockerfile `CMD` in a container | C-002, C-027, C-029 |
| Vision / Supplier / Logistics agents (8081–8083) | `run.sh` locally | C-003, C-027 |
| `deploy/start.sh` | not referenced by Dockerfile or deploy script | C-029 |

**Representative flow — `POST /api/analyze`:** empty-file check → background task → JPEG compression → Vision agent (Gemini count + bounding boxes; count = number of boxes) → Supplier agent (text query → embedding → nearest row) → random order ID broadcast → Logistics agent (table lookup) → background Gmail/Calendar/Sheets calls → WebSocket events [C-023, C-009, C-010, C-021, C-012, C-015, C-040].

## 6. Component Map
| Component | Responsibility | Key files | Claims |
|---|---|---|---|
| Control Tower | Orchestration, WebSocket events, Google API integrations | `frontend/app.py` | C-002, C-004, C-015, C-040 |
| Vision Agent | Image validation, Gemini counting, structured query | `agents/vision-agent/` | C-006, C-007, C-024 |
| Supplier Agent | Query sanitizing, embeddings, AlloyDB nearest match | `agents/supplier-agent/` | C-010, C-025, C-026 |
| Logistics Agent | Zone/weight shipping table | `agents/logistics-agent/` | C-012, C-013 |
| MCP server | Three stub tools | `frontend/mcp_server.py` | C-014, C-016 |
| Database | Inventory table, vector column, ScaNN index | `database/` | C-010, C-013 |

## 7. Data Flow & Persistence
- **Inputs:** an uploaded image [C-023].
- **Persistence:** the AlloyDB inventory table holds parts, suppliers and embeddings [C-010]. Orders are kept only as a Google Sheet row and email; no order store was found [C-021, C-015].
- **Outputs:** WebSocket events broadcast to all connected clients, plus the Google Workspace writes [C-040, C-015].
- **Configured, not wired:** the Supplier Agent has an image-based search; the Control Tower's requests observed carry only text queries [C-011].

## 8. External Integrations
| Integration | Usage | Claims |
|---|---|---|
| Vertex AI Gemini (`gemini-3-flash-preview`, `gemini-2.5-flash-lite`) | Direct | C-006, C-007 |
| Vertex AI `text-embedding-005` | Direct | C-010 |
| AlloyDB (Python Connector, pg8000) | Direct | C-010, C-031 |
| Gmail, Google Calendar, Google Sheets APIs (OAuth refresh token) | Direct, fire-and-forget | C-015, C-019 |
| FastMCP | Server defined; not in the execution path found | C-014, C-016 |
| `anthropic` SDK | Declared and imported; no use found | C-038 |
| Google Cloud Run | Deploy script | C-028 |

## 9. Interfaces / APIs
- Control Tower: `POST /api/analyze`, `GET /api/health`, `GET /api/test-images`, `GET /api/test-image/{name}`, `GET /`, and WebSocket `/ws` [C-002, C-039].
- Agents: A2A JSON-RPC with agent cards (`/.well-known/agent-card.json`) [C-003].
- MCP: `/mcp` HTTP app with three tools [C-014].

## 10. Build / Test / Deploy / Operate
- Local: `run.sh` starts all four services with health checks [C-027].
- Container: the Dockerfile installs Vision, Supplier and frontend requirements and its `CMD` starts the Control Tower; no startup of the agents was found [C-029].
- Deploy: `deploy/deploy.sh` → one Cloud Run service, `--allow-unauthenticated`, with env vars that omit the OAuth and agent URLs [C-028, C-030].
- Tests: 97 offline test cases against inline copies of the functions [C-032, C-033, C-034]. No CI configuration was found [C-035].
- Live environment: UNKNOWN [C-036].

## 11. Security & Authentication Evidence
- No authentication was found on Control Tower routes. The deploy script makes the service public [C-028].
- Guardrails: Vision checks size, MIME type and injection patterns (query text only) [C-024]. Supplier applies a character allowlist and returns a generic database error [C-025].
- `/api/analyze`: an empty-file check was found; no size or type check was found before processing [C-023].
- A fixed personal email address and spreadsheet ID are in source. Values are not reproduced here [C-018].
- AlloyDB uses connector credentials plus a database password; a base64 service-account key may be passed as an env var [C-031].
- None of this establishes overall security posture.

## 12. Domain / Business Concepts
Inventory part, supplier, stock level, shipping zone, carrier, ETA, and order confirmation [C-010, C-012, C-021]. "Order" here means a broadcast event plus Workspace writes, not a transaction in an order system [C-021].

## 13. Alignment Gaps (Contradictions / Drift)
- README says integrations run through MCP tools in `mcp_server.py`; the running code calls Google APIs directly, and the MCP tools are stubs [C-016, C-014].
- README says the confirmation email goes to the supplier; the code sends it to a fixed address [C-017].
- README says AlloyDB access is IAM-based; the code logs in with a database password (the README's own env table also lists `DB_PASS`) [C-031].
- README calls the counting "deterministic computer vision"; counting is done by a generative model with code execution [C-008].
- README says agents are composable "without touching orchestration code"; the call order and payloads are coded in the Control Tower [C-005].
- A test-file comment mentions integration-marked tests; none were found [C-034].
- `deploy.sh` requires `GEMINI_API_KEY`; no Python file was found that reads it [C-030].

## 14. Important Unknowns
| Unknown | Why the repo can't establish it | What would resolve it |
|---|---|---|
| What the live demo runs [C-036] | Committed container startup found covers the Control Tower alone [C-029] | Inspect the Cloud Run revision and its image |
| Ownership and provenance [C-037] | README points to a different account; no owner or intent file found | Ask the repo owner |
| Count consistency [C-008] | No repeated-run measurements were found in the repo | Run the same image N times and compare |
| ScaNN performance at this scale [C-041] | Figures are cited from external benchmarks | Benchmark on the 20-row dataset and a larger one |

## 15. Claims Ledger

| ID | Claim | Class | Strength | Confidence | Evidence | Verification | Caveat |
|---|---|---|---|---|---|---|---|
| C-001 | The documented purpose is to count shelf items from a photo, find a supplier, compute shipping, and confirm via Gmail, Calendar and Sheets | OBSERVED | CORROBORATED | HIGH | `README.md:L9-L22#Four specialized agents`; `frontend/app.py:L783-L791#run_workflow_with_events` | VERIFIED | Purpose from README; code path corroborates |
| C-002 | The Control Tower is a FastAPI app exposing `/api/analyze`, `/api/health`, test-image routes, `/`, and a `/ws` WebSocket | OBSERVED | DIRECT | HIGH | `frontend/app.py:L47#FastAPI`; `frontend/app.py:L771-L784#/api/analyze`; `frontend/app.py:L802-L850#/api/health` | VERIFIED | — |
| C-003 | Vision, Supplier and Logistics agents are separate A2A services, each defining an AgentCard | OBSERVED | CORROBORATED | HIGH | `agents/vision-agent/main.py:L35-L39#AgentCard`; `agents/supplier-agent/main.py:L57-L61#AgentCard`; `agents/logistics-agent/main.py:L58-L62#AgentCard` | VERIFIED | — |
| C-004 | The Control Tower calls Vision, then Supplier, then Logistics via A2A at env-configured URLs, then starts the Workspace integrations | OBSERVED | DIRECT | HIGH | `frontend/app.py:L43-L45#VISION_AGENT_URL`; `frontend/app.py:L243-L245#A2ACardResolver`; `frontend/app.py:L399-L401#supplier_resolver`; `frontend/app.py:L542-L544#logistics_resolver`; `frontend/app.py:L602#run_mcp_integrations` | VERIFIED | — |
| C-005 | Agent cards are fetched at runtime, but which agents are called, in what order, and with what payloads is coded in the Control Tower, while the README says agents can be swapped or added with orchestration code unchanged | CONTRADICTED | DIRECT | MEDIUM | `README.md:L309#without touching orchestration code`; `frontend/app.py:L546-L551#logistics_payload` | VERIFIED | Discovery is real; composition is not data-driven |
| C-006 | Vision counting calls `gemini-3-flash-preview` with a code-execution tool at temperature 0 | OBSERVED | DIRECT | HIGH | `agents/vision-agent/agent.py:L149-L161#gemini-3-flash-preview` | VERIFIED | — |
| C-007 | A second call to `gemini-2.5-flash-lite` produces structured count, type and search query | OBSERVED | DIRECT | HIGH | `agents/vision-agent/agent_executor.py:L66-L76#gemini-2.5-flash-lite` | VERIFIED | — |
| C-008 | The README describes counting as deterministic computer vision; the code obtains the count from a generative model that may write and run code | CONTRADICTED | DIRECT | MEDIUM | `README.md:L19#deterministic computer vision`; `agents/vision-agent/agent.py:L149-L161#generate_content` | QUALIFIED | Temperature 0 and code execution reduce variation; consistency is untested |
| C-009 | The Control Tower uses the number of returned bounding boxes as the item count | OBSERVED | DIRECT | HIGH | `frontend/app.py:L337#len(bounding_boxes)` | VERIFIED | — |
| C-010 | Supplier match is a Vertex `text-embedding-005` embedding plus an AlloyDB cosine-distance query returning the single nearest row; the schema defines a ScaNN index | OBSERVED | CORROBORATED | HIGH | `agents/supplier-agent/inventory.py:L111-L116#ORDER BY distance ASC`; `agents/supplier-agent/inventory.py:L253#text-embedding-005`; `database/seed_data.sql:L91-L92#scann` | VERIFIED | Index use at runtime depends on the DB planner |
| C-011 | The Control Tower's supplier request carries only a text query; no Control Tower request using the Supplier Agent's image-search path was found | OBSERVED | CORROBORATED | HIGH | `frontend/app.py:L451#query`; `agents/supplier-agent/agent_executor.py:L105-L110#find_supplier_by_image` | VERIFIED | Search scope: full read of Control Tower request construction; grep for `image_base64` in `frontend/app.py` |
| C-012 | Logistics is a deterministic supplier-location and zone table with a default location for unmatched names | OBSERVED | DIRECT | HIGH | `agents/logistics-agent/shipping.py:L14-L32#SUPPLIER_LOCATIONS`; `agents/logistics-agent/shipping.py:L100-L112#get_supplier_location` | VERIFIED | Destination is fixed to New York, NY by the Control Tower (`frontend/app.py:L550`) |
| C-013 | The supplier names seeded in the database appear in the logistics location table | OBSERVED | CORROBORATED | HIGH | `database/seed_data.sql:L41-L42#Packaging Solutions Inc`; `agents/logistics-agent/shipping.py:L15-L16#packaging solutions inc` | VERIFIED | Compared the full seeded name list by hand |
| C-014 | The MCP server defines three tools that return confirmation strings; no external service call was found in their bodies | OBSERVED | CORROBORATED | HIGH | `frontend/mcp_server.py:L5-L17#send_gmail_email`; `tests/test_supply_chain.py:L586-L590#MCP tool stubs` | VERIFIED | Search scope: full read of `frontend/mcp_server.py` (17 lines); the test file itself calls them stubs |
| C-015 | Gmail, Calendar and Sheets writes are made by the Control Tower directly through `googleapiclient`; no import or call of `mcp_server` was found | OBSERVED | CORROBORATED | HIGH | `frontend/app.py:L688#build("gmail"`; `frontend/app.py:L715#build("calendar"`; `frontend/app.py:L735#build("sheets"` | VERIFIED | Search scope: grep of all `.py`, `.sh`, `Dockerfile` for `mcp_server`, `mcp`, `fastmcp` |
| C-016 | The README states the Control Tower triggers three MCP tools via `mcp_server.py`, while the running integration path calls Google APIs directly | CONTRADICTED | CORROBORATED | HIGH | `README.md:L71#via` ; `frontend/app.py:L651-L660#run_mcp_integrations`; `frontend/app.py:L688#build` | VERIFIED | The function is named for MCP but does not use it |
| C-017 | The README says the confirmation email goes to the supplier contact; the code sets both From and To to a fixed configured address | CONTRADICTED | DIRECT | HIGH | `README.md:L96#supplier contact`; `frontend/app.py:L703-L704#USER_EMAIL` | VERIFIED | — |
| C-018 | A personal email address and a Google Sheet ID are hard-coded in Control Tower source | OBSERVED | DIRECT | HIGH | `frontend/app.py:L642-L648#USER_EMAIL` | VERIFIED | Values intentionally not reproduced in this report |
| C-019 | Integrations use an OAuth refresh token from env vars with gmail.send, calendar and spreadsheets scopes | OBSERVED | DIRECT | HIGH | `frontend/app.py:L665-L676#scopes` | VERIFIED | — |
| C-020 | When the Supplier Agent replies with plain text (its unmatched-query, rejection and database-error messages), the Control Tower keeps placeholder part, supplier and "High" confidence values and continues to the order and integration steps | INFERRED | CORROBORATED | HIGH | `frontend/app.py:L467-L469#Acme Industrial Supplies`; `frontend/app.py:L494-L495#JSONDecodeError`; `frontend/app.py:L520-L530#order_placed`; `agents/supplier-agent/agent_executor.py:L149#No matching supplier found`; `agents/supplier-agent/agent_executor.py:L157#Database error` | VERIFIED | Traced statically, not executed |
| C-021 | Order IDs are random 4-digit numbers, and "order placed" is a broadcast event; no order store was found | OBSERVED | CORROBORATED | HIGH | `frontend/app.py:L520-L530#random.randint` | VERIFIED | Search scope: full read of `frontend/app.py`; grep of all `.py` for order persistence |
| C-022 | No human approval step was found between supplier match and the order and integration steps; the README states no human is required | OBSERVED | CORROBORATED | HIGH | `README.md:L11#no human required`; `frontend/app.py:L520-L613#asyncio.create_task(run_mcp_integrations` | VERIFIED | Search scope: full read of `run_workflow_with_events` and the routes in `frontend/app.py` |
| C-023 | `/api/analyze` performs an empty-file check, then starts the workflow in the background; no size or type check was found at the Control Tower | OBSERVED | CORROBORATED | HIGH | `frontend/app.py:L783-L796#Empty file uploaded` | VERIFIED | Search scope: full read of `analyze_image` and `compress_image`; Vision validates downstream (C-024) |
| C-024 | The Vision agent caps images at 10 MB, allowlists MIME types, and blocks 11 injection phrases in the query text; the Control Tower's request carries only the image, so the default prompt is used | OBSERVED | CORROBORATED | HIGH | `agents/vision-agent/agent.py:L36-L75#PROMPT_INJECTION_PATTERNS`; `agents/vision-agent/agent.py:L143-L145#DEFAULT_QUERY`; `frontend/app.py:L294-L298#image_base64` | VERIFIED | The phrase filter applies to query text, not to text inside images |
| C-025 | The Supplier agent strips characters outside an allowlist and returns a generic message on database errors | OBSERVED | DIRECT | HIGH | `agents/supplier-agent/agent_executor.py:L30-L54#re.sub`; `agents/supplier-agent/agent_executor.py:L153-L158#exc_info=True` | VERIFIED | — |
| C-026 | Match confidence is a linear mapping of cosine distance (0–2) to a percentage | OBSERVED | DIRECT | HIGH | `agents/supplier-agent/agent_executor.py:L59-L69#compute_confidence` | VERIFIED | Not a calibrated probability |
| C-027 | `run.sh` starts all four services locally and checks their health endpoints | OBSERVED | DIRECT | HIGH | `run.sh:L187-L211#8083` | VERIFIED | — |
| C-028 | `deploy/deploy.sh` deploys one Cloud Run service from source with `--allow-unauthenticated` | OBSERVED | DIRECT | HIGH | `deploy/deploy.sh:L133-L140#--allow-unauthenticated` | VERIFIED | — |
| C-029 | No configuration was found that starts the three agents in the container: the Dockerfile starts only the Control Tower, and `deploy/start.sh` (Vision and Supplier only) is not referenced | INFERRED | CORROBORATED | MEDIUM | `Dockerfile:L17#frontend.app:app`; `deploy/start.sh:L10-L30#Supplier Agent` | VERIFIED | Search scope: grep of the repo for `start.sh`; the live demo may be built differently (C-036) |
| C-030 | The deploy env vars include `GEMINI_API_KEY`, which no Python file was found to read, and no OAuth or agent URL variables were found among them | OBSERVED | CORROBORATED | HIGH | `deploy/deploy.sh:L35-L38#GEMINI_API_KEY`; `deploy/deploy.sh:L141-L152#ALLOYDB_IP_TYPE` | VERIFIED | Search scope: grep of all `.py` for `GEMINI_API_KEY`; full read of the deploy env-var list |
| C-031 | The README says AlloyDB access is IAM-based; the code connects with connector credentials (ADC or a service-account key, optionally base64 in an env var) and a database password | CONTRADICTED | CORROBORATED | MEDIUM | `README.md:L160#IAM-based`; `README.md:L244#DB_PASS`; `agents/supplier-agent/inventory.py:L28-L57#ALLOYDB_SA_KEY_B64`; `agents/supplier-agent/inventory.py:L83-L90#DB_PASS` | VERIFIED | The connector's own authorization is IAM-based; the database login is not |
| C-032 | The suite has 86 plain test functions plus one parametrized over 11 patterns (97 cases, matching the README), all against inline copies of the functions; no import of agent modules was found | OBSERVED | CORROBORATED | HIGH | `tests/test_supply_chain.py:L17-L21#Inline the pure-logic functions`; `tests/test_supply_chain.py:L281#parametrize`; `README.md:L280#97 tests` | VERIFIED | Search scope: grep of `tests/` for agent imports; the copies could drift from the real code |
| C-033 | The MCP tests check copies of the stub return strings defined inside the test class | OBSERVED | DIRECT | HIGH | `tests/test_supply_chain.py:L586-L599#_send_gmail` | VERIFIED | — |
| C-034 | A test-file comment mentions integration-marked tests that are skipped by default; no such tests were found | CONTRADICTED | CORROBORATED | HIGH | `tests/test_supply_chain.py:L19-L21#integration` | VERIFIED | Search scope: grep of `tests/` for markers and `integration` |
| C-035 | The README documents a manual test run; no CI configuration was found | OBSERVED | CORROBORATED | HIGH | `README.md:L278-L285#Running Tests` | VERIFIED | Search scope: file listing of the full repository (no `.github/` or other CI files) |
| C-036 | Whether the live demo URL is running, and what code it runs, cannot be established from the repo | UNKNOWN | INSUFFICIENT | LOW | `README.md:L5#Live Demo` | VERIFIED | URL not visited |
| C-037 | The README's clone instructions point to a different GitHub account than this repository's; the repo is Apache-2.0 licensed | OBSERVED | DIRECT | HIGH | `README.md:L256#git clone`; `LICENSE:L1#Apache License` | VERIFIED | Relationship between the accounts is not established by the repo |
| C-038 | The `anthropic` package is declared and imported by the Control Tower; no use of it was found | OBSERVED | CORROBORATED | HIGH | `frontend/app.py:L23#import anthropic`; `frontend/requirements.txt:L9#anthropic` | VERIFIED | Search scope: grep of all `.py` for `anthropic` |
| C-039 | `/api/test-images` reads PNG/JPG files from `frontend/test-images`, while the repo's sample images are WebP files in a root `test-images` folder | INFERRED | CORROBORATED | MEDIUM | `frontend/app.py:L813-L822#test_images_dir`; `test-images/README.md` | VERIFIED | In this layout the endpoint would return an empty list |
| C-040 | Workflow events are broadcast to every connected WebSocket client, and the event cache is cleared per run, so concurrent users would share one event stream | INFERRED | CORROBORATED | HIGH | `frontend/app.py:L62-L95#broadcast`; `frontend/app.py:L221#clear_cache` | VERIFIED | Inferred from code; not exercised |
| C-041 | The ScaNN speed figures in the README are cited from external benchmarks; no benchmark of this system was found in the repo | OBSERVED | CORROBORATED | HIGH | `README.md:L173#10×`; `README.md:L307#10×` | VERIFIED | Search scope: repo file listing and grep for benchmark scripts or results |

## 16. Next Inspection Targets
| Target | Uncertainty it resolves | Value |
|---|---|---|
| The Cloud Run revision behind the live demo URL | C-036, C-029: what actually runs | High |
| `setup.sh` and `database/seed.py` | How embeddings are populated; whether the setup matches the README | Medium |
| `frontend/static/app.js` | How the UI presents placeholder results and integration status | Medium |
| Run the tests, then point them at the real modules | C-032: whether the copies match the code | High |

## 17. What I would verify before repeating this in an architecture meeting

| Statement as I'd say it | Claims | What could change it | Cheapest check |
|---|---|---|---|
| "The MCP layer isn't in the running path; it's direct Google API calls." | C-015, C-016 | Absence claim; an external MCP client could call `/mcp` | Ask the owner; check whether anything mounts the MCP app |
| "If supplier lookup fails, the order still goes out with placeholder values." | C-020 | Static trace only | Stop the DB and run one image locally; watch the WebSocket events |
| "The deployed container only runs the Control Tower." | C-029, C-036 | The live demo may use a different image or config | `gcloud run services describe` on the demo service |
| "Emails go to a fixed address, not the supplier." | C-017, C-018 | Direct read; low risk | Re-read `frontend/app.py` lines 703–704 at the deployed SHA |
| "97 tests, but they test copies of the code." | C-032 | Direct read; the copies may match the code today | `pytest -q`, then diff the copies against the agent modules |
| "DB access uses a password, not IAM database auth." | C-031 | The connector also uses IAM for authorization | Check the AlloyDB user type in the console |
