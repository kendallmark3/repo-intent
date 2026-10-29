# Glossary

- **Material claim** — any statement about purpose, architecture, runtime behavior, data flow, security/auth, persistence, integration, deployment, domain meaning, ownership/boundary, or test/build/ops behavior. Every one goes in the claims ledger.
- **Claim class** — OBSERVED (directly evidenced) · INFERRED (reasoned from observations, path shown) · UNKNOWN (repo cannot establish it) · CONTRADICTED (sources disagree).
- **Evidence strength** — DIRECT · CORROBORATED · INDIRECT · INSUFFICIENT.
- **Confidence** — HIGH · MEDIUM · LOW, derived from evidence quality, never model certainty. No percentages.
- **Verification** — VERIFIED · QUALIFIED (supports a weaker statement) · FAILED.
- **High-impact claim** — purpose, primary entry point, auth, persistence, external integration, deployment topology, architectural boundary. Requires a second, disconfirming pass.
- **Target** — the repository being analyzed, cloned under `targets/`.
