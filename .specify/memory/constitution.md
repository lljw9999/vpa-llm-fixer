# VPA (Verifier → Plan → Apply) Constitution

<!--
SYNC IMPACT REPORT - 2025-10-24
Version: 0.1.0 (Initial creation)
Modified Principles: None (initial version)
Added Sections: All (initial creation)
  - Core Principles (6 principles)
  - Quality Standards
  - Development Workflow
  - Governance
Removed Sections: None
Templates Requiring Updates:
  ✅ constitution.md - Created
  ⚠ plan-template.md - Review for alignment
  ⚠ spec-template.md - Review for alignment
  ⚠ tasks-template.md - Review for alignment
Follow-up TODOs:
  - Validate constitution principles against existing MVP roadmap
  - Review and align all templates with constitution principles
  - Establish regression test baseline for adapter gating
-->

## Core Principles

### I. Research-First Development

Every feature begins with rigorous research and evaluation before implementation. Research outputs must be documented in `research.md` with clear rationale, alternatives considered, and decisions made. This ensures:

- All unknowns are identified and resolved before coding
- Technology choices are justified with evidence
- Best practices are discovered and applied
- Integration patterns are validated before implementation

**Rationale**: VPA is a research project comparing multiple approaches (VPA vs best-of-N, Self-Refine, RL). Decisions must be evidence-based and reproducible.

### II. Verification-Centric Architecture

The verifier ensemble is the cornerstone of VPA. All components must support the verify-then-learn loop:

- Verifiers MUST be composable and independently testable
- Each verifier channel (factual, formal, style) MUST produce interpretable diagnostics
- Verification scores MUST be calibrated and measurable (precision, recall, Brier score)
- Verifier outputs MUST inform planner decisions

**Rationale**: The entire VPA approach depends on reliable verification signals. Poor verifiers produce bad training data and degrade model performance.

### III. Gated Adapter Updates (NON-NEGOTIABLE)

Every adapter update MUST pass through the regression gate before merging. No exceptions.

- Gate MUST use a frozen stability set (no data leakage)
- Acceptance criteria: ≥3 EM points on QA OR ≥5 pass@1 points on coding benchmarks
- Failed adapters MUST be quarantined (no merge to main)
- Gate results MUST be logged with reproducible configs

**Rationale**: This prevents catastrophic forgetting and ensures "sticky" improvements persist. Bypassing the gate undermines the core VPA value proposition.

### IV. Reproducibility & Experimentation Discipline

All experiments MUST be reproducible with fixed seeds, versioned configs, and documented hyperparameters:

- Every experiment MUST log: model checkpoint, LoRA config, verifier ensemble config, training data hash
- Results MUST include standard deviations across multiple runs
- Ablations MUST isolate single variables (e.g., remove one verifier channel at a time)
- Baseline comparisons MUST use identical evaluation harnesses

**Rationale**: VPA is positioned for publication. Reproducibility is mandatory for peer review and open science.

### V. Minimal LoRA Footprint

Keep adapter updates small and composable to avoid instability:

- Prefer LoRA rank ≤ 16 for initial experiments
- Each adapter MUST target specific domain (law, math, code) or error pattern
- Adapter routing MUST use similarity metrics (embedding distance, task classification)
- Monitor adapter interference (cross-domain performance deltas)

**Rationale**: Small adapters are easier to debug, compose, and route. Large updates risk the same instability problems as full fine-tuning.

### VI. Dataset & Metric Transparency

All datasets and evaluation metrics MUST be clearly documented and aligned with research questions:

- Each dataset MUST map to a specific research question (RQ1-RQ4)
- Metrics MUST be standard and comparable (EM/F1, pass@k, ECE, hallucination rate)
- Custom metrics MUST be justified and validated
- Data splits MUST prevent train/test leakage

**Rationale**: Experimental rigor requires transparent, standard evaluation. Ad-hoc metrics undermine comparisons and reproducibility.

## Quality Standards

### Testing Requirements

- **Verifier Unit Tests**: Each verifier component MUST have unit tests validating scoring logic on known-good and known-bad examples
- **Integration Tests**: Draft → Verify → Plan → Apply pipeline MUST be tested end-to-end on small synthetic examples
- **Regression Tests**: Gate suite MUST be version-controlled and never modified without explicit justification
- **Contract Tests**: If multiple modules (e.g., external planner service), contracts MUST be tested independently

### Documentation Requirements

- **Research Decisions**: All technology/approach choices MUST be documented in `research.md` with rationale
- **Experiment Configs**: Every experiment MUST have a YAML config file with all hyperparameters
- **Results Documentation**: Experimental results MUST include plots (Pareto curves, calibration plots) and summary tables
- **Code Comments**: Complex verifier logic and scoring functions MUST include inline explanations

### Performance Standards

- **Draft Generation**: k-sampling MUST complete within 10 seconds for k ≤ 5 on 7B-13B models
- **Verification**: Verifier ensemble MUST process candidates in parallel, completing all checks in < 5 seconds per batch
- **Adapter Training**: LoRA SFT MUST converge in < 100 steps for rank ≤ 16 on small training sets (< 500 examples)
- **Gate Evaluation**: Regression suite MUST run in < 5 minutes to enable rapid iteration

## Development Workflow

### Feature Development Process

1. **Specification Phase**: Write `spec.md` with user stories (if applicable) or experimental goals
2. **Research Phase**: Generate `research.md` resolving all unknowns and technology choices
3. **Planning Phase**: Create `plan.md` with technical context, structure, and constitution check
4. **Design Phase**: Generate `data-model.md` (entities, schemas), `contracts/` (APIs if needed), `quickstart.md` (test scenarios)
5. **Implementation Phase**: Generate `tasks.md`, implement in dependency order, gate all changes
6. **Evaluation Phase**: Run experiments, generate plots, document results in paper

### Code Review Requirements

- All PRs MUST include constitution compliance check
- Complex verifier logic MUST be reviewed by at least two team members
- Adapter merges MUST show gate results in PR description
- Experimental results MUST be reproducible (include config file and random seed)

### Version Control Practices

- **Branch Strategy**: Feature branches for each verifier/planner/dataset addition
- **Commit Messages**: Follow conventional commits (feat, fix, docs, test, refactor)
- **Adapter Versioning**: Tag each successful adapter with domain + version (e.g., `math-v1.2`, `code-v2.0`)
- **Config Versioning**: Lock dependency versions in `requirements.txt` or `pyproject.toml`

## Governance

### Amendment Process

This constitution governs all VPA development practices. Amendments require:

1. **Proposal**: Document proposed change with rationale in GitHub issue
2. **Team Review**: Discuss impact on existing workflow, reproducibility, and publication readiness
3. **Approval**: Consensus from all active contributors (for research project of this size)
4. **Migration**: Update all templates, documentation, and existing artifacts to match
5. **Versioning**: Increment version according to semantic versioning (see below)

### Constitution Versioning

- **MAJOR** (X.0.0): Backward-incompatible changes (e.g., removing gate requirement)
- **MINOR** (0.X.0): New principles added or materially expanded (e.g., adding new verifier requirement)
- **PATCH** (0.0.X): Clarifications, wording fixes, non-semantic refinements

### Complexity Justification

Any complexity beyond these principles MUST be explicitly justified:

- Why is additional abstraction/tooling necessary?
- What simpler alternative was considered and rejected?
- How does it support the research goals (RQ1-RQ4)?

If complexity cannot be justified, the simpler approach MUST be used.

### Compliance Verification

- All `/speckit.*` commands MUST check constitution compliance
- All PRs MUST pass automated constitution checks (where automatable)
- Manual review MUST verify adherence to non-automated principles (e.g., research documentation quality)
- Violations MUST be flagged and justified in PR descriptions

**Version**: 0.1.0 | **Ratified**: 2025-10-24 | **Last Amended**: 2025-10-24
