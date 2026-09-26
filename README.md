# AI Workforce Intelligence

An AI-driven prototype for analyzing technology job roles, skills requirements, and workforce readiness across emerging technology domains.

## Current pipeline

```
Job Descriptions → CSV → Python → Skill Extraction → Capability Categories → Frequency Analysis
```

### Current capabilities
- Structured CSV input
- Python text normalization
- Rule-based skill extraction
- Capability taxonomy
- Role-level analysis
- Skill-frequency analysis
- Capability-coverage analysis
- Automated tests

### Categories
**AI & ML · Cloud · Programming · Data & APIs · Embedded · VLSI · Project Management · Systems**

## Run

```bash
python src/skill_extractor.py
```

Run tests:

```bash
python -m unittest discover -s tests -v
```

## Roadmap
- [x] Python skill extraction
- [x] Frequency analysis
- [x] Automated tests
- [ ] Pandas analysis
- [ ] Larger job dataset
- [ ] SQL skills database
- [ ] LLM-assisted extraction
- [ ] Skills-gap scoring
- [ ] Visualization
- [ ] Cloud deployment

This project is a technical companion to research into human-capital transitions driven by AI and Quantum Computing in India.
