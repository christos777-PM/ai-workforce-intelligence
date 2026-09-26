# System Architecture

## Version 1

1. CSV dataset stores representative technology roles.
2. Python reads the role descriptions.
3. A skill taxonomy defines initial categories.
4. Keyword extraction identifies known skills.
5. Role analysis produces structured output.

## Why start with keyword extraction?

The first implementation is deliberately transparent. A technical reviewer can inspect exactly how the baseline works before we introduce NLP and LLM approaches.

## Planned architecture

```
Job Descriptions
      |
      v
Data Ingestion
      |
      +------> Rule / Keyword Baseline
      |
      +------> NLP Extraction
      |
      +------> LLM Extraction
      |
      v
Skills Database
      |
      v
Role & Skills Analysis
      |
      v
Workforce Intelligence
```
