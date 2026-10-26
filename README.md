# AI Workforce Intelligence

[![CI](https://github.com/christos777-PM/ai-workforce-intelligence/actions/workflows/ci.yml/badge.svg)](https://github.com/christos777-PM/ai-workforce-intelligence/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)

A transparent, research-oriented prototype for turning technology job descriptions into structured workforce capability signals.

The project is designed around a simple engineering principle: **make the baseline auditable before making it intelligent**.

## Why this project exists

My research explores human-capital transitions driven by Artificial Intelligence and Quantum Computing in India. This repository is the technical companion: a small system for examining what skills appear in emerging-technology roles and how those requirements can be translated into capability categories.

It is a portfolio project, not a hiring or candidate-screening system.

## Architecture

```
CSV job descriptions
        │
        ▼
┌───────────────────┐
│ Text normalization│
└─────────┬─────────┘
          ▼
┌───────────────────┐
│ Skill extraction  │  ← versioned taxonomy
└─────────┬─────────┘
          ▼
┌───────────────────┐
│ Capability mapping│
└─────────┬─────────┘
          ▼
┌───────────────────┐
│ Workforce analysis│
└─────────┬─────────┘
          ▼
   JSON / terminal output
          │
          ▼
   Target-role gap analysis
          │
          ▼
   Optional role-fit ranking
          │
          ▼
   Optional benchmark JSONL export
```

## Current capabilities

- Structured CSV ingestion
- Deterministic whole-word and phrase matching
- Versioned capability taxonomy
- Role-level skill extraction
- Category-level frequency analysis
- Top-skill analysis
- Target-role coverage and skills-gap analysis
- Optional role ranking by transparent target-skill coverage
- JSON output for downstream workflows
- JSONL prediction export for external benchmark evaluation
- Automated tests
- GitHub Actions CI across Python 3.10–3.13
- Methodology and limitations documentation

### Capability taxonomy

**AI & ML · Cloud · Programming · Data & APIs · Embedded · VLSI · Project Management · Systems**

## Quick start

### 1. Clone and install

```bash
git clone https://github.com/christos777-PM/ai-workforce-intelligence.git
cd ai-workforce-intelligence
python -m pip install -e .
```

### 2. Analyze the sample dataset

```bash
workforce-intel data/sample_jobs.csv
```

Machine-readable output:

```bash
workforce-intel data/sample_jobs.csv --json
```

### 3. Run a target-role gap analysis

```bash
workforce-intel data/sample_jobs.csv --target data/targets/ai_project_manager.json
```

JSON output:

```bash
workforce-intel data/sample_jobs.csv --target data/targets/ai_project_manager.json --json
```

### 4. Rank observed roles against a target capability profile

```bash
workforce-intel data/sample_jobs.csv --target data/targets/ai_project_manager.json --rank-target
```

For a machine-readable ranking:

```bash
workforce-intel data/sample_jobs.csv --target data/targets/ai_project_manager.json --rank-target --json
```

The ranking orders the supplied job descriptions by the percentage of target skills detected in each description. It includes matched and missing skills so readers can inspect why a role received its score. The score is a description-level signal, not an assessment of a person's proficiency, employability or suitability. Results depend on the sample, taxonomy and deterministic matching rules.

### 5. Export predictions for benchmark evaluation

```bash
workforce-intel data/sample_jobs.csv --predictions-jsonl /tmp/workforce-predictions.jsonl
```

The command writes one JSON object per role, with a stable `role_id`, title and sorted unique `predicted_skills` array. By default, the ID is a normalized slug of the title. If a CSV includes a `role_id` column, that explicit value is used instead. Duplicate IDs are rejected rather than silently assigned order-dependent suffixes.

The output schema is compatible with the evaluator in [AI & Quantum Human Capital](https://github.com/christos777-PM/ai-quantum-human-capital). Evaluate it only against a reference JSONL file with matching role IDs and human-reviewed `gold_skills`. Exporting predictions is not itself evidence of accuracy; the benchmark's provenance, labels and limitations determine what conclusions are justified.

### 6. Run tests

```bash
python -m unittest discover -s tests -v
```

## Example output

The included sample dataset contains five illustrative technology roles spanning AI, cloud, semiconductor, embedded and product-management contexts.

The pipeline reports:

- number of roles analyzed
- capability-category frequency
- most frequently observed skills
- role-level extracted skills
- optional target-role coverage
- optional target-role skills gap
- optional ranked role descriptions with matched and missing target skills
- optional JSONL predictions for an external evaluator

The sample data is intentionally small and illustrative. It should not be interpreted as a labor-market estimate.

## Repository structure

```
.
├── data/
│   ├── sample_jobs.csv
│   └── targets/
│       └── ai_project_manager.json
├── docs/
│   └── methodology.md
├── src/
│   └── aw_intelligence/
│       ├── analysis.py
│       ├── benchmark.py
│       ├── cli.py
│       ├── extractor.py
│       ├── io.py
│       ├── role_fit.py
│       └── taxonomy.py
├── tests/
│   ├── test_benchmark_export.py
│   ├── test_cli.py
│   ├── test_extractor.py
│   ├── test_pipeline.py
│   └── test_role_fit.py
├── .github/workflows/ci.yml
├── pyproject.toml
└── README.md
```

## Design decisions

### Rule-based baseline first

A deterministic extractor is intentionally used before introducing embeddings or LLMs. This makes every result explainable and gives later intelligent methods a measurable baseline.

### Frequency is not importance

A skill appearing frequently is not automatically more valuable. The current analysis measures **observed presence across roles**, not skill criticality, salary impact, hiring difficulty or business value.

### Research-safe boundaries

The prototype should use public, licensed or synthetic job data. Do not upload personal candidate information. Do not use the output as an automated employment decision.

## Roadmap

- [x] Python skill extraction
- [x] Capability taxonomy
- [x] Role-level analysis
- [x] Frequency analysis
- [x] Skills-gap primitives
- [x] Target-role gap analysis
- [x] Target-role fit ranking in the CLI
- [x] JSONL prediction export for benchmark evaluation
- [x] Automated tests
- [x] CI across Python versions
- [ ] Larger licensed job dataset
- [ ] Pandas-based analytical layer
- [ ] Embedding-based semantic matching
- [ ] LLM-assisted extraction with evaluation
- [ ] Visualization dashboard
- [ ] Database-backed longitudinal analysis
- [ ] Cloud deployment

## Research connection

This repository supports my broader research question:

> How can organizations prepare people for technologies that are changing faster than traditional workforce-planning models?

The intended progression is:

**Research question → data → technical prototype → evidence → management insight.**
