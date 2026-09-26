# Methodology

## Purpose

AI Workforce Intelligence is a small, transparent prototype for turning technology job descriptions into structured capability signals.

It is designed for portfolio demonstration and research prototyping, not automated hiring decisions.

## Pipeline

1. **Input**: CSV records containing a role title and job description.
2. **Normalization**: Lowercase text and whitespace normalization.
3. **Extraction**: Deterministic whole-word/phrase matching against a versioned taxonomy.
4. **Categorization**: Skills are mapped to capability categories.
5. **Analysis**: Role coverage, category frequency and top-skill frequency are calculated.
6. **Output**: Human-readable terminal output or JSON for downstream analysis.

## Why rule-based first?

A deterministic baseline makes the system auditable. Every extracted skill can be traced to an explicit taxonomy entry and text match. This provides a useful baseline before experimenting with embeddings or LLM-assisted extraction.

## Limitations

- Job descriptions are not standardized.
- Synonyms and implied skills may be missed.
- Frequency is not a measure of skill importance.
- The sample dataset is illustrative and not representative of the labor market.
- No personal or candidate-level data should be used with this prototype.

## Planned extensions

- Larger, licensed job dataset
- Embedding-based semantic matching
- LLM-assisted extraction with evaluation against the rule-based baseline
- Skills-gap scoring by target role
- Dashboard and visualization
- Database-backed longitudinal analysis
