# Failure Log

Evidence for Progressive Intent. Intent 002 is chosen from the most important **repeated** failure here — not from imagination.

Categories: unsupported claim · overstatement · missed component · false component · wrong entry point · broken evidence citation · contradiction missed · excessive UNKNOWN · wasted context/tokens · report too verbose.

| Date | Target | Category | Claim ID | What happened | Severity (H/M/L) |
|---|---|---|---|---|---|
| 2026-10-29 | clinical-evidence-coordinator | broken evidence citation (checker) | C-022, C-032 | Checker silently skipped citations whose `#symbol` contained a space, so some evidence was never verified; it also flagged prose inline code (`/ping`, `0.2.0`) as missing files. Fixed: strict parsing in the ledger, locator-only parsing in prose, spaces allowed in symbols. | H |
| 2026-10-29 | clinical-evidence-coordinator | overstatement | C-012, C-014, C-016, C-017, C-020, C-021, C-027, C-028, C-029 | Absence was stated as fact ("never calls", "no authentication", "unused") when only a scoped static search supported it. Fixed by Evidence Policy Rule 16 + checker enforcement on ledger rows; prose was swept by hand. | M |

## Pattern summary
<!-- Update after each run: which categories repeat, across which repo shapes. -->
- Run 1: the checker enforces Rule 16 on ledger rows only. If unscoped absence keeps appearing in prose on repo #2, that is a candidate for Intent 002.
