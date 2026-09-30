# Target-role analysis

The target-role layer converts the workforce prototype from descriptive counting into a decision-support experiment.

## Question

Given a target capability profile, which observed roles in the dataset are closest to it?

## Method

For each observed role:

1. Extract the role's canonical skills with the deterministic taxonomy.
2. Compare those skills with the target role's required skill set.
3. Calculate coverage as:

`coverage = |required ∩ present| / |required| × 100`

4. Report matched and missing skills.
5. Rank roles by coverage, then by role title for deterministic tie-breaking.

## Interpretation

A higher score means the role description contains more of the target vocabulary. It **does not** mean:

- the person performing the role has those skills;
- the role is more senior;
- the role is more valuable;
- the organization should hire that person;
- the skills have equal importance.

The output is therefore a workforce-analysis signal, not a hiring score.

## Why this matters for Engineering Management

The same analytical pattern can support questions such as:

- Which existing roles are closest to a future technology role?
- What capability gaps appear between today's roles and tomorrow's requirements?
- Which skills should be prioritized for learning or reskilling?
- How can workforce-planning assumptions be made explicit and reproducible?

The next research step is to compare this transparent baseline with semantic and LLM-assisted approaches using a labelled evaluation set.
