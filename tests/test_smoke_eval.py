from __future__ import annotations

import json
import subprocess
from pathlib import Path
import sys


def test_smoke_eval_creates_summary(tmp_path: Path) -> None:
    # Run eval into a temp output dir so tests are deterministic
    out_dir = tmp_path / "run"
    cmd = [
        sys.executable,
        "-m",
        "rag_eval.app.eval",
        "--out",
        str(out_dir),
        "--questions",
        "data/eval/questions.jsonl",
        "--corpus",
        "data/corpus/corpus.jsonl",
    ]
    subprocess.check_call(cmd)

    summary_path = out_dir / "summary.json"
    assert summary_path.exists()

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    assert "n" in summary
    assert summary["n"] > 0