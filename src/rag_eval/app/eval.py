from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from datetime import datetime

from rag_eval.core.reporting import write_json, write_jsonl, make_summary
from rag_eval.core.judge_generation import judge_generation
from rag_eval.core.judge_retrieval import judge_retrieval


@dataclass
class RunPaths:
    repo_root: Path
    questions_path: Path
    corpus_path: Path
    out_dir: Path


def parse_args() -> argparse.Namespace:
    ts = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    p = argparse.ArgumentParser(description="Eval runner (Week2 skeleton)")
    p.add_argument("--questions", default="data/eval/questions.jsonl")
    p.add_argument("--corpus", default="data/corpus/corpus.jsonl")
    p.add_argument("--out", default=f"reports/runs/{ts}")
    return p.parse_args()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def main() -> int:
    args = parse_args()

    repo_root = Path(__file__).resolve().parents[3]  # .../src/rag_eval/app/eval.py -> repo root
    paths = RunPaths(
        repo_root=repo_root,
        questions_path=(repo_root / args.questions).resolve(),
        corpus_path=(repo_root / args.corpus).resolve(),
        out_dir=(repo_root / args.out).resolve(),
    )
    paths.out_dir.mkdir(parents=True, exist_ok=True)

    questions = load_jsonl(paths.questions_path)
    corpus = load_jsonl(paths.corpus_path)

    # Week2 skeleton: no real RAG yet. We create predictable dummy outputs.
    predictions = []

    for q in questions:
        if q["type"] == "A":
            ans = (
                "開始条件: 依頼を受領し、必要情報が揃っている。\n"
                "実行: 書類確認→ブッキング→通関手配。\n"
                "完了条件: B/L発行および出港確認。\n"
                "次にやること: インボイス/パッキングリストを共有してください。\n"
                "確認事項: インコタームズと貨物の危険品該当有無を教えてください。\n"
            )
        else:
            ans = f"(DUMMY) Answer for {q['id']}"

        predictions.append(
            {
                "id": q["id"],
                "type": q["type"],
                "question": q["question"],
                "retrieved": [{"chunk_id": "dummy#0", "text": corpus[0]["text"] if corpus else ""}],
                "answer": ans,
            }
        )

    # Judge for Retrieval
    ret_judgements = []
    for p_ in predictions:
        j = judge_retrieval(question=p_["question"], q_type=p_["type"], retrieved=p_["retrieved"])
        ret_judgements.append(
            {
                "id": p_["id"],
                "type": p_["type"],
                **j,
            }
        )

    # Judge for Generation
    gen_judgements = []
    for p_ in predictions:
        j = judge_generation(answer=p_["answer"], q_type=p_["type"])
        gen_judgements.append(
            {
                "id": p_["id"],
                "type": p_["type"],
                **j,
            }
        )
    

    write_jsonl(paths.out_dir / "predictions.jsonl", predictions)
    write_jsonl(paths.out_dir / "judgements_generation.jsonl", gen_judgements)
    write_jsonl(paths.out_dir / "judgements_retrieval.jsonl", ret_judgements)

    summary = make_summary(gen_judgements, ret_judgements)
    write_json(paths.out_dir / "summary.json", summary)

    print(f"[OK] wrote reports to: {paths.out_dir}")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
