from __future__ import annotations

import re
from typing import Any


def _contains_any(text: str, patterns: list[str]) -> bool:
    t = text.lower()
    return any(re.search(p, t) for p in patterns)


def judge_retrieval(question: str, q_type: str, retrieved: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Week2 minimal retrieval judge.
    We only check if retrieved chunks contain evidence-like keywords by type.
    This is intentionally rough: goal is to split failure modes.
    """
    chunks_text = "\n".join((c.get("text") or "") for c in retrieved)

    # R1: any relevance (very rough): shares at least one keyword with question
    # Week2: stabilize R1. If we retrieved any non-empty chunk, treat it as "has some relevant chunk".
    # (We will make this stricter in Week3+)
    r1 = bool(chunks_text.strip())

    # R2: type-specific "evidence exists" check (keyword-based)
    if q_type == "A":
        r2 = _contains_any(chunks_text, [r"開始条件", r"完了条件", r"手順", r"procedure", r"steps?"])
        r2_key = "R_has_specific_procedure_chunk"
    elif q_type == "B":
        r2 = _contains_any(chunks_text, [r"禁止", r"不可", r"例外", r"forbidden", r"not allowed", r"exception"])
        r2_key = "R_has_policy_or_rule_chunk"
    elif q_type == "C":
        r2 = _contains_any(chunks_text, [r"書類", r"invoice", r"packing", r"申告", r"証明", r"document"])
        r2_key = "R_has_documents_requirement_chunk"
    elif q_type == "D":
        r2 = _contains_any(chunks_text, [r"とは", r"定義", r"means", r"refers to"])
        r2_key = "R_has_definition_chunk"
    elif q_type == "E":
        r2 = _contains_any(chunks_text, [r"対応", r"手順", r"escalat", r"連絡", r"immediate", r"workaround"])
        r2_key = "R_has_specific_procedure_chunk"
    else:
        r2 = False
        r2_key = "R_unknown_type"

    checks = {
        "R_has_any_relevant_chunk": r1,
        r2_key: r2,
    }
    passed = all(checks.values())
    failure_reasons = [k for k, v in checks.items() if not v]

    # evidence: chunk_id (first match) or ""
    evidence: dict[str, str] = {"R_has_any_relevant_chunk": "", r2_key: ""}
    if r1 and retrieved:
        evidence["R_has_any_relevant_chunk"] = retrieved[0].get("chunk_id", "")
    if r2:
        # find first chunk that matches the type-specific patterns
        for c in retrieved:
            t = (c.get("text") or "")
            if q_type in ("A", "E") and _contains_any(t, [r"開始条件", r"完了条件", r"手順", r"procedure", r"steps?"]):
                evidence[r2_key] = c.get("chunk_id", "")
                break
            if q_type == "B" and _contains_any(t, [r"禁止", r"不可", r"例外", r"forbidden", r"not allowed", r"exception"]):
                evidence[r2_key] = c.get("chunk_id", "")
                break
            if q_type == "C" and _contains_any(t, [r"書類", r"invoice", r"packing", r"申告", r"証明", r"document"]):
                evidence[r2_key] = c.get("chunk_id", "")
                break
            if q_type == "D" and _contains_any(t, [r"とは", r"定義", r"means", r"refers to"]):
                evidence[r2_key] = c.get("chunk_id", "")
                break

    return {
        "checks": checks,
        "pass": passed,
        "failure_reasons": failure_reasons,
        "evidence": evidence,
    }
