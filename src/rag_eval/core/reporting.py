from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def make_summary(gen: list[dict[str, Any]], ret: list[dict[str, Any]]) -> dict[str, Any]:
    def pass_rate(items: list[dict[str, Any]]) -> float:
        if not items:
            return 0.0
        passed = sum(1 for x in items if x.get("pass") is True)
        return passed / len(items)

    return {
        "n": len(gen),
        "generation_pass_rate": pass_rate(gen),
        "retrieval_pass_rate": pass_rate(ret),
        "overall_note": "Week2 skeleton: dummy judgements (expected near 0).",
    }
