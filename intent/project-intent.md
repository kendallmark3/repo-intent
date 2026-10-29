# Project Intent

## Purpose
RepoIntent: point Claude Code at an unfamiliar checked-out repository and get a fast, evidence-backed Repository Intelligence Report — what the system is, how it works, where its boundaries are, and what cannot be known from the repo alone.

## Business outcomes
- An architect entering an unfamiliar codebase gets a trustworthy orientation in minutes, not hours.
- Every material conclusion survives "Show me the evidence."

## Constraints
- Local-first. No AWS, hosted service, database, embeddings, MCP, or UI in V1 unless the intent cannot be met without them. Earn every layer.
- Accuracy > coverage. Evidence > plausibility. Unknown > invention.
- Hard requirements: `policies/EVIDENCE_POLICY.md`, `contracts/REPORT_CONTRACT.md`.
