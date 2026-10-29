#!/usr/bin/env python3
"""Mechanical evidence check for a RepoIntent report.

Checks that every evidence citation in a Repository Intelligence Report points at
something that actually exists in the analyzed repository, and that the claims
ledger is internally consistent. It does NOT judge whether the evidence supports
the wording of a claim; that remains the job of the self-audit and human review.

Citation format (see contracts/REPORT_CONTRACT.md, "Evidence Citation Format"):

    `path/to/file.ext`                 whole file
    `path/to/file.ext:L42`             single line
    `path/to/file.ext:L42-L60`         line range
    `path/to/file.ext:L42-L60#symbol`  range that must contain `symbol`
    `path/to/file.ext#symbol`          file that must contain `symbol`

Usage:
    python3 tools/check_citations.py REPORT.md --repo targets/<name>

Exit code 0 when no errors are found, 1 otherwise. Standard library only.
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

CITATION_RE = re.compile(
    r"`(?P<path>[^`\s:#]+)"
    r"(?::L(?P<start>\d+)(?:-L(?P<end>\d+))?)?"
    r"(?:#(?P<symbol>[^`\s]+))?`"
)
CLAIM_ID_RE = re.compile(r"\bC-\d{3,}\b")
CLASSES = {"OBSERVED", "INFERRED", "UNKNOWN", "CONTRADICTED"}
STRENGTHS = {"DIRECT", "CORROBORATED", "INDIRECT", "INSUFFICIENT"}
CONFIDENCES = {"HIGH", "MEDIUM", "LOW"}
VERIFICATIONS = {"VERIFIED", "QUALIFIED", "FAILED"}
PERCENT_RE = re.compile(r"\b\d{1,3}(?:\.\d+)?\s?%\s*(?:confiden|certain|sure|likely)", re.I)


@dataclass
class Citation:
    raw: str
    path: str
    start: int | None
    end: int | None
    symbol: str | None


@dataclass
class Result:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    citations_checked: int = 0
    claims: int = 0


def parse_citations(text: str) -> list[Citation]:
    out = []
    for m in CITATION_RE.finditer(text):
        path = m.group("path")
        # Only treat it as a citation if it looks like a path (has a slash or a dot extension)
        # or carries a line/symbol locator. Avoids flagging inline code like `UNKNOWN`.
        has_locator = m.group("start") or m.group("symbol")
        if not ("/" in path or "." in path or has_locator):
            continue
        start = int(m.group("start")) if m.group("start") else None
        end = int(m.group("end")) if m.group("end") else start
        out.append(Citation(m.group(0), path, start, end, m.group("symbol")))
    return out


def check_citation(c: Citation, repo: Path) -> str | None:
    target = (repo / c.path).resolve()
    try:
        target.relative_to(repo.resolve())
    except ValueError:
        return f"{c.raw}: path escapes the repository root"
    if not target.exists():
        return f"{c.raw}: file does not exist in {repo}"
    if target.is_dir():
        if c.start or c.symbol:
            return f"{c.raw}: line/symbol locator used on a directory"
        return None
    try:
        lines = target.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError as e:  # pragma: no cover - unreadable file
        return f"{c.raw}: cannot read file ({e})"
    if c.start is not None:
        if c.start < 1 or c.end < c.start:
            return f"{c.raw}: invalid line range"
        if c.end > len(lines):
            return f"{c.raw}: line {c.end} is past end of file ({len(lines)} lines)"
        scope = lines[c.start - 1 : c.end]
    else:
        scope = lines
    if c.symbol and not any(c.symbol in line for line in scope):
        where = f"lines {c.start}-{c.end}" if c.start else "file"
        return f"{c.raw}: symbol '{c.symbol}' not found in cited {where}"
    return None


def parse_ledger(text: str) -> tuple[list[dict], list[str]]:
    """Return ledger rows from the first markdown table whose header starts with ID | Claim."""
    rows, problems = [], []
    lines = text.splitlines()
    header_idx = None
    for i, line in enumerate(lines):
        cells = [c.strip().lower() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 8 and cells[0] == "id" and cells[1] == "claim":
            header_idx = i
            headers = cells
            break
    if header_idx is None:
        return rows, ["claims ledger table not found (header must begin `| ID | Claim |`)"]
    for line in lines[header_idx + 2 :]:
        if not line.strip().startswith("|"):
            break
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < len(headers):
            problems.append(f"ledger row has too few columns: {line.strip()[:80]}")
            continue
        rows.append(dict(zip(headers, cells)))
    return rows, problems


def check_report(report: Path, repo: Path) -> Result:
    res = Result()
    text = report.read_text(encoding="utf-8")

    rows, problems = parse_ledger(text)
    res.errors.extend(problems)
    res.claims = len(rows)
    ledger_ids = set()
    for row in rows:
        cid = row.get("id", "")
        if not CLAIM_ID_RE.fullmatch(cid):
            res.errors.append(f"ledger: bad claim ID '{cid}'")
            continue
        if cid in ledger_ids:
            res.errors.append(f"{cid}: duplicate claim ID")
        ledger_ids.add(cid)
        for col, allowed in (("class", CLASSES), ("strength", STRENGTHS),
                             ("confidence", CONFIDENCES), ("verification", VERIFICATIONS)):
            val = row.get(col, "").strip("*` ").upper()
            if val not in allowed:
                res.errors.append(f"{cid}: {col} '{row.get(col, '')}' not one of {sorted(allowed)}")
        cls = row.get("class", "").strip("*` ").upper()
        cites = parse_citations(row.get("evidence", ""))
        if cls in {"OBSERVED", "INFERRED", "CONTRADICTED"} and not cites:
            res.errors.append(f"{cid}: {cls} claim has no evidence citation")
        if row.get("verification", "").strip("*` ").upper() == "FAILED" and cls != "UNKNOWN":
            res.warnings.append(f"{cid}: verification FAILED but claim is still {cls}; downgrade or remove")

    # Every claim ID used in the body must exist in the ledger.
    for cid in sorted(set(CLAIM_ID_RE.findall(text)) - ledger_ids):
        res.errors.append(f"{cid}: referenced in report but missing from the claims ledger")
    unused = ledger_ids - set(CLAIM_ID_RE.findall(text.split("Claims Ledger")[0]))
    if rows and unused and len(unused) == len(ledger_ids):
        res.warnings.append("no ledger claim IDs are referenced from the report body")

    for c in parse_citations(text):
        res.citations_checked += 1
        err = check_citation(c, repo)
        if err:
            res.errors.append(err)

    for m in PERCENT_RE.finditer(text):
        res.warnings.append(f"numeric confidence found ('{m.group(0)}'); Evidence Policy Rule 13")
    return res


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("report", type=Path, help="path to the report markdown")
    ap.add_argument("--repo", type=Path, required=True, help="root of the analyzed repository")
    args = ap.parse_args(argv)
    if not args.report.is_file():
        print(f"report not found: {args.report}", file=sys.stderr)
        return 2
    if not args.repo.is_dir():
        print(f"repo not found: {args.repo}", file=sys.stderr)
        return 2
    res = check_report(args.report, args.repo)
    for e in res.errors:
        print(f"ERROR   {e}")
    for w in res.warnings:
        print(f"WARN    {w}")
    status = "PASS" if not res.errors else "FAIL"
    print(f"{status}: {res.claims} claims, {res.citations_checked} citations checked, "
          f"{len(res.errors)} errors, {len(res.warnings)} warnings")
    return 0 if not res.errors else 1


if __name__ == "__main__":
    sys.exit(main())
