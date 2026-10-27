# Methodology

## Purpose

AI Workforce Intelligence is a small, transparent prototype for turning technology job descriptions into structured capability signals.

It is designed for portfolio demonstration and research prototyping, not automated hiring decisions.

## Pipeline

1. **Input**: CSV records containing a role title and job description.
2. **Normalization**: Lowercase text and whitespace normalization.
3. **Extraction**: Deterministic whole-word/phrase matching against a versioned taxonomy, including explicitly listed surface-form aliases.
4. **Overlap handling**: When a longer skill phrase overlaps a shorter phrase (for example, "REST APIs" and "APIs"), retain the longer match for that text span to avoid double-counting the same phrase as both a specific and generic skill.
5. **Categorization**: Skills are mapped to canonical taxonomy labels and capability categories.
6. **Analysis**: Role coverage, category frequency and top-skill frequency are calculated.
7. **Output**: Human-readable terminal output or JSON for downstream analysis.

## Alias policy

The taxonomy lists plural forms for selected skills such as API, LLM, microcontroller, FPGA, ASIC and semiconductor. It also maps the abbreviation "AI" to the canonical label "artificial intelligence". When "AI" appears inside a longer listed phrase such as "generative AI", longest-phrase overlap handling preserves the more specific canonical label. Each alias maps to an existing canonical label; the extractor does not apply broad stemming or infer semantic equivalence. Additions should be explicit, tested, and reviewed for overlap with longer phrases.

## Why rule-based first?

A deterministic baseline makes the system auditable. Every extracted skill can be traced to an explicit taxonomy entry or alias and text match. This provides a useful baseline before experimenting with embeddings or LLM-assisted extraction.

## Limitations

- Job descriptions are not standardized.
- Synonyms and implied skills may be missed.
- Alias rules improve surface-form coverage but do not establish semantic equivalence.
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
