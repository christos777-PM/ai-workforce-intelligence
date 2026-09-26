# Testing

Run the automated test suite from the repository root:

```bash
python -m unittest discover -s tests -v
```

The suite currently checks skill extraction, case-insensitive matching, skill frequency, and capability coverage.

Future versions will test data validation, NLP extraction, LLM responses, and API integrations.
