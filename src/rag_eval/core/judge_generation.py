from __future__ import annotations

import re
from typing import Any


def _has_any(text: str, patterns: list[str]) -> bool:
    t = text.lower()
    return any(re.search(p, t) for p in patterns)


def judge_generation(answer: str, q_type: str) -> dict[str, Any]:
    """
    Week2: rubric v0 (very rough heuristics).
    We only need: (1) keys fixed, (2) booleans, (3) pass computed.
    """
    a = answer.strip()

    if q_type == "A":
        checks = {
            "A_structure_start_execute_end": _has_any(a, [r"開始条件", r"start condition"]) and _has_any(a, [r"実行", r"steps?", r"procedure"]) and _has_any(a, [r"完了条件", r"done", r"completion"]),
            "A_has_next_action": _has_any(a, [r"次に", r"next action", r"やってください", r"してください"]),
            "A_has_questions_to_ask": _has_any(a, [r"確認", r"教えてください", r"need to confirm", r"please confirm", r"\?"]),
        }

    elif q_type == "B":
        checks = {
            "B_has_clear_conclusion": _has_any(a, [r"禁止", r"不可", r"not allowed", r"forbidden", r"条件付き", r"conditionally allowed"]),
            "B_has_condition_if_applicable": (("条件付き" in a) or ("conditionally" in a.lower())) and _has_any(a, [r"条件", r"if ", r"only if", r"場合"]),
            "B_has_confirmation_if_uncertain": _has_any(a, [r"不確実", r"depends", r"not sure", r"確認が必要"]) and _has_any(a, [r"確認", r"必要情報", r"please confirm", r"need to know"]),
        }

    elif q_type == "C":
        checks = {
            "C_lists_two_document_categories": sum(1 for p in [r"申告", r"運送", r"インボイス", r"invoice", r"packing", r"申請", r"証明", r"certificate"] if re.search(p, a, re.IGNORECASE)) >= 2,
            "C_declares_dependency_and_one_condition": _has_any(a, [r"状況依存", r"depends", r"ケース", r"case"]) and _has_any(a, [r"条件", r"if ", r"場合", r"depending on"]),
            "C_mentions_one_format_requirement": _has_any(a, [r"言語", r"署名", r"電子", r"original", r"copy", r"signature", r"format"]),
        }

    elif q_type == "D":
        checks = {
            "D_definition_includes_is_and_is_not": _has_any(a, [r"とは", r"means", r"refers to"]) and _has_any(a, [r"ではない", r"does not", r"not refer"]),
            "D_mentions_one_related_status_or_system_field": _has_any(a, [r"ステータス", r"status", r"項目", r"field", r"コード", r"code"]),
        }

    elif q_type == "E":
        checks = {
            "E_has_immediate_action": _has_any(a, [r"即時", r"すぐ", r"immediately", r"right away"]),
            "E_has_escalation": _has_any(a, [r"エスカレーション", r"上長", r"担当", r"連絡", r"escalate", r"contact"]),
            "E_has_one_item_to_confirm": _has_any(a, [r"確認", r"必要情報", r"need to confirm", r"need to know", r"\?"]),
        }
    else:
        checks = {"unknown_type": False}

    passed = all(bool(v) for v in checks.values())
    failure_reasons = [k for k, v in checks.items() if not v]

    return {
        "checks": checks,
        "pass": passed,
        "failure_reasons": failure_reasons,
    }
