# Evaluation-driven RAG Prototype (Logistics)

This repository is a minimal, evaluation-first RAG prototype designed for internal logistics operations.

## Purpose
The goal of this project is not to maximize answer quality, but to:
- Separate **retrieval** and **generation** evaluation
- Make failures explicit via rubric-based judges
- Enable reproducible evaluation through CI

## What is evaluated
- Retrieval: whether relevant procedural chunks are retrieved
- Generation: whether answers satisfy task-specific rubrics (A–E)

Judgements are written to JSONL files for auditability.

## How to run
```bash
python -m rag_eval.app.eval
```

## Evaluation outputs are stored under:
```bash
reports/runs/<timestamp>/
```

# Status
Week2: Evaluation loop, judges, smoke test, and CI are implemented.