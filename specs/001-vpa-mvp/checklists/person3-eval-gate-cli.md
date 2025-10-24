# Person 3: Eval, Gate & CLI Lead - Quality Checklist

**Purpose**: Quality checklist for Evaluation, Regression Gate, CLI, and Testing infrastructure
**Created**: 2025-10-24
**Focus Areas**: Requirements completeness, metric correctness, gate reliability, CLI usability, test coverage

## Requirement Completeness

- [ ] CHK001 - Are all required metrics (EM, F1, pass@k, accuracy, Brier, ECE) clearly specified? [Completeness, Spec §FR-015]
- [ ] CHK002 - Are gate acceptance criteria (≥3 EM or ≥5 pass@1 improvement) precisely defined? [Clarity, Spec §FR-010]
- [ ] CHK003 - Are gate regression thresholds (>3 point drop) clearly specified? [Clarity, Spec §FR-011]
- [ ] CHK004 - Is stability set construction (20% of training data, frozen) documented? [Completeness, Gate Design]
- [ ] CHK005 - Are CLI command interfaces (arguments, flags, outputs) fully specified? [Completeness, Spec §US1-6]
- [ ] CHK006 - Are experiment tracking requirements (metadata, logging, WandB) documented? [Completeness, Spec §FR-013]
- [ ] CHK007 - Are gate performance requirements (<5min on 200 examples) measurable? [Measurability, Spec §SC-004]
- [ ] CHK008 - Are edge cases for metrics documented (empty predictions, malformed code, division by zero)? [Coverage, Edge Cases]
- [ ] CHK009 - Are edge cases for gate documented (borderline scores, metric conflicts, stability set staleness)? [Coverage, Edge Cases]
- [ ] CHK010 - Are edge cases for CLI documented (missing files, invalid configs, interrupted runs)? [Coverage, Edge Cases]

## Implementation Quality - Metrics

- [ ] CHK011 - Does EM (exact match) metric handle string normalization correctly? [Correctness, Spec §FR-015]
- [ ] CHK012 - Does F1 metric correctly compute token-level precision and recall? [Correctness, Spec §FR-015]
- [ ] CHK013 - Does pass@k metric correctly execute code and aggregate results? [Correctness, Spec §FR-015]
- [ ] CHK014 - Does accuracy metric handle different answer formats (numeric, string, multiple choice)? [Robustness]
- [ ] CHK015 - Does Brier score correctly measure calibration with confidence scores? [Correctness, Spec §FR-015]
- [ ] CHK016 - Does ECE (Expected Calibration Error) use proper binning strategy? [Correctness, Spec §FR-015]
- [ ] CHK017 - Does hallucination rate metric correctly identify contradictions? [Correctness, Spec §FR-015]
- [ ] CHK018 - Are all metrics tested on known examples with expected outputs? [Testing]

## Implementation Quality - Evaluation Harnesses

- [ ] CHK019 - Does QA evaluation harness correctly load and process HotpotQA data? [Spec §FR-014]
- [ ] CHK020 - Does QA harness compute both EM and F1 metrics per specification? [Spec §FR-015]
- [ ] CHK021 - Does code evaluation harness safely execute code in sandbox? [Security, Spec §FR-015]
- [ ] CHK022 - Does code harness compute pass@1 and pass@k for multiple k values? [Spec §FR-015]
- [ ] CHK023 - Does math evaluation harness correctly parse and compare numeric answers? [Correctness]
- [ ] CHK024 - Do all harnesses handle edge cases gracefully (missing data, timeouts, errors)? [Robustness]
- [ ] CHK025 - Are evaluation results logged with all metadata (model, dataset, timestamp)? [Observability]

## Implementation Quality - Regression Gate

- [ ] CHK026 - Does Gate correctly construct frozen stability set (20% of training data)? [Spec §US5]
- [ ] CHK027 - Does Gate evaluate adapter on stability set without data leakage? [Correctness]
- [ ] CHK028 - Does Gate correctly compute performance deltas (new - old)? [Correctness]
- [ ] CHK029 - Does Gate apply acceptance criteria correctly (≥3 EM or ≥5 pass@1)? [Spec §FR-010]
- [ ] CHK030 - Does Gate detect regressions correctly (>3 point drop on any metric)? [Spec §FR-011]
- [ ] CHK031 - Does Gate produce pass/fail decision with detailed metrics report? [Spec §US5]
- [ ] CHK032 - Does Gate quarantine failed adapters to separate directory? [Spec §FR-011]
- [ ] CHK033 - Does Gate log all evaluations with timestamps and configs? [Observability, Spec §FR-013]
- [ ] CHK034 - Is Gate evaluation reproducible with same adapter and stability set? [Reproducibility]

## Implementation Quality - CLI

- [ ] CHK035 - Does `vpa draft` command accept all required arguments (dataset, k, tools)? [Spec §US1]
- [ ] CHK036 - Does `vpa verify` command integrate with verifier ensemble correctly? [Spec §US2]
- [ ] CHK037 - Does `vpa plan` command invoke planner with verifier results? [Spec §US3]
- [ ] CHK038 - Does `vpa train` command accept LoRA training parameters? [Spec §US4]
- [ ] CHK039 - Does `vpa gate` command run regression gate and report results? [Spec §US5]
- [ ] CHK040 - Does `vpa eval` command run appropriate evaluation harness? [Evaluation]
- [ ] CHK041 - Do all CLI commands provide helpful error messages and usage examples? [Usability]
- [ ] CHK042 - Do CLI commands support both JSON and human-readable output? [Usability]
- [ ] CHK043 - Are CLI outputs formatted nicely with tables and progress bars? [UX]
- [ ] CHK044 - Do CLI commands respect global config file settings? [Configuration]

## Testing Coverage - Unit Tests

- [ ] CHK045 - Are unit tests provided for all metrics with known examples? [Testing, T105]
- [ ] CHK046 - Are unit tests provided for Gate with synthetic adapter results? [Testing, T090]
- [ ] CHK047 - Are unit tests provided for utility functions (logging, seed, checkpointing)? [Testing, T022]
- [ ] CHK048 - Do all unit tests run in <1 second each? [Performance]
- [ ] CHK049 - Is unit test coverage >80% for vpa/eval/ and vpa/apply/gate.py? [Quality Gate]

## Testing Coverage - Integration Tests

- [ ] CHK050 - Are integration tests provided for Draft→Verify pipeline? [Testing, T128]
- [ ] CHK051 - Are integration tests provided for Apply→Gate pipeline? [Testing, T131]
- [ ] CHK052 - Are integration tests provided for full pipeline on 10 examples? [Testing, T132]
- [ ] CHK053 - Are integration tests provided for tool integration? [Testing, T133]
- [ ] CHK054 - Are integration tests provided for experiment tracking? [Testing, T135]
- [ ] CHK055 - Do integration tests run in <5 minutes total? [Performance]

## Testing Coverage - Contract Tests

- [ ] CHK056 - Are contract tests provided for Verifier interface? [Testing, T057]
- [ ] CHK057 - Are contract tests provided for Planner interface? [Testing, T068]
- [ ] CHK058 - Do contract tests validate all interface requirements? [Completeness]

## Performance Validation

- [ ] CHK059 - Does Gate complete evaluation in <5min on 200 examples? [Performance, Spec §SC-004]
- [ ] CHK060 - Do evaluation harnesses run efficiently without memory leaks? [Performance]
- [ ] CHK061 - Do CLI commands start up quickly (<2 seconds to first output)? [Performance]
- [ ] CHK062 - Are performance benchmarks included in test suite? [Testing]
- [ ] CHK063 - Is experiment tracking (WandB) lightweight and non-blocking? [Performance]

## Constitution Compliance

- [ ] CHK064 - Does Gate use frozen stability set per Principle III? [Constitution, Principle III - NON-NEGOTIABLE]
- [ ] CHK065 - Does Gate enforce acceptance criteria per Principle III? [Constitution, Principle III - NON-NEGOTIABLE]
- [ ] CHK066 - Does Gate quarantine failed adapters per Principle III? [Constitution, Principle III - NON-NEGOTIABLE]
- [ ] CHK067 - Are all experiments logged with full metadata per Principle IV? [Constitution, Principle IV]
- [ ] CHK068 - Do metrics match standard definitions per Principle VI? [Constitution, Principle VI]
- [ ] CHK069 - Are all datasets mapped to research questions per Principle VI? [Constitution, Principle VI]
- [ ] CHK070 - Is research on evaluation metrics documented in research.md? [Constitution, Principle I]

## Experiment Infrastructure

- [ ] CHK071 - Is ExperimentRun class implemented with all required metadata fields? [Spec §FR-013, T088]
- [ ] CHK072 - Is WandB or TensorBoard integration working correctly? [Experiment Tracking, T089]
- [ ] CHK073 - Are experiment configs properly versioned in configs/experiments/? [Organization]
- [ ] CHK074 - Can experiments be reproduced from saved configs and seeds? [Reproducibility]
- [ ] CHK075 - Are experiment results saved with timestamps and unique IDs? [Organization]
- [ ] CHK076 - Can multiple experiments run in parallel without conflicts? [Reliability]

## Scripts & Automation

- [ ] CHK077 - Does `scripts/setup_env.sh` correctly set up Python environment? [Setup]
- [ ] CHK078 - Does `scripts/download_models.sh` download required base models? [Setup]
- [ ] CHK079 - Does `scripts/download_datasets.sh` download all three datasets? [Setup]
- [ ] CHK080 - Does `scripts/run_mvp_pipeline.sh` demonstrate full pipeline? [Demo, T124]
- [ ] CHK081 - Does `scripts/train_adapter.sh` train single adapter correctly? [Utility, T125]
- [ ] CHK082 - Does `scripts/run_experiments.sh` run all baseline experiments? [Automation, T126]
- [ ] CHK083 - Do all scripts handle errors gracefully with informative messages? [Robustness]

## CI/CD & Automation

- [ ] CHK084 - Is GitHub Actions workflow for tests correctly configured? [CI, T013]
- [ ] CHK085 - Is GitHub Actions workflow for constitution check configured? [CI, T014]
- [ ] CHK086 - Do CI tests run on all PRs automatically? [Automation]
- [ ] CHK087 - Does CI catch test failures before merge? [Quality Gate]
- [ ] CHK088 - Is CI configured to run integration tests? [CI, T137]

## Documentation Requirements

- [ ] CHK089 - Are all public classes and methods documented with docstrings? [Documentation]
- [ ] CHK090 - Is architecture.md created explaining system design? [Documentation, T174]
- [ ] CHK091 - Is evaluation_guide.md created with metric definitions? [Documentation, T177]
- [ ] CHK092 - Is main README.md updated with installation and usage instructions? [Documentation, T178]
- [ ] CHK093 - Are CLI commands documented with examples in README? [Documentation]
- [ ] CHK094 - Are gate criteria and stability set construction documented? [Documentation]
- [ ] CHK095 - Is experiment tracking workflow documented? [Documentation]

## Results & Reproducibility

- [ ] CHK096 - Are baseline experiment results documented with metrics? [Results, T140-T142]
- [ ] CHK097 - Are VPA experiment results documented with improvements? [Results, T146-T154]
- [ ] CHK098 - Are ablation study results documented with comparisons? [Results, T162]
- [ ] CHK099 - Are all result tables generated with proper formatting? [Results, T172]
- [ ] CHK100 - Are all plots generated (Pareto curves, calibration plots)? [Results, T173]
- [ ] CHK101 - Are results reproducible with documented seeds and configs? [Reproducibility, T179]
- [ ] CHK102 - Is reproducibility checklist created and verified? [Reproducibility, T179]

## Integration Readiness

- [ ] CHK103 - Can Eval module be imported and used standalone for testing? [Integration]
- [ ] CHK104 - Can Gate module be imported and used standalone for testing? [Integration]
- [ ] CHK105 - Can CLI commands be invoked from shell successfully? [Integration]
- [ ] CHK106 - Are all modules integrated in test_pipeline.py? [Integration, T127-T132]
- [ ] CHK107 - Can full pipeline run end-to-end without manual intervention? [Integration]
- [ ] CHK108 - Can external researcher reproduce results using documentation? [Reproducibility]

## Paper & Publication Readiness

- [ ] CHK109 - Are all experiments run with 3 random seeds? [Publication, T170]
- [ ] CHK110 - Are mean and std computed for all metrics? [Publication, T171]
- [ ] CHK111 - Are final result tables publication-ready? [Publication, T172]
- [ ] CHK112 - Are all plots publication-quality (high resolution, labeled)? [Publication, T173]
- [ ] CHK113 - Are all configs and results archived for reproducibility? [Publication, T180]
- [ ] CHK114 - Is final constitution compliance check passed? [Quality Gate, T181]
- [ ] CHK115 - Is code polished with docstrings, type hints, comments? [Code Quality, T182]
- [ ] CHK116 - Is GitHub release created with reproducibility package? [Publication, T183]
