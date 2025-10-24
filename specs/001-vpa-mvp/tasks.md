# VPA MVP Tasks

**Feature**: VPA (Verifier → Plan → Apply) Framework
**Branch**: `001-vpa-mvp`
**Team**: 3 people (Person 1: Draft/Verify, Person 2: Plan/Apply, Person 3: Eval/Gate/CLI)
**Timeline**: 8 weeks (MVP in 2 weeks, full system in 8 weeks)

## Task Organization by User Story

Tasks are organized by user story to enable independent implementation and testing. Each person has clear ownership of specific stories.

## Phase 1: Setup (All Team Members - Day 1)

**Goal**: Initialize project structure and environment

- [ ] T001 [P] Create project directory structure per implementation plan
- [ ] T002 [P] Create `requirements.txt` with core dependencies (PyTorch, Transformers, PEFT, Datasets)
- [ ] T003 [P] Create `pyproject.toml` with project metadata and dev dependencies
- [ ] T004 [P] Set up `.gitignore` for Python project (exclude data/, models/, __pycache__)
- [ ] T005 [P] Create `configs/base.yaml` with base model and LoRA default settings
- [ ] T006 [P] Create `configs/verifiers.yaml` with verifier ensemble configuration
- [ ] T007 [P] Create `configs/planner_grid.yaml` with planner action space
- [ ] T008 [P] Create `configs/datasets.yaml` with dataset paths and split ratios
- [ ] T009 Create `scripts/setup_env.sh` for environment initialization
- [ ] T010 Create `scripts/download_models.sh` for downloading base models from HuggingFace
- [ ] T011 Create `scripts/download_datasets.sh` for downloading datasets
- [ ] T012 [P] Set up pytest configuration in `pytest.ini` or `pyproject.toml`
- [ ] T013 [P] Create GitHub Actions workflow in `.github/workflows/tests.yml`
- [ ] T014 [P] Create GitHub Actions workflow in `.github/workflows/constitution_check.yml`
- [ ] T015 Initialize git repository and create feature branch `001-vpa-mvp`

## Phase 2: Foundational Infrastructure (Week 1, Days 2-3)

**Goal**: Build shared utilities and base classes that all modules depend on

- [ ] T016 [Person 3] Create `vpa/utils/logging.py` with structured logging setup
- [ ] T017 [Person 3] Create `vpa/utils/seed.py` with reproducible random seed utilities
- [ ] T018 [Person 2] Create `vpa/utils/checkpointing.py` with model checkpoint save/load utilities
- [ ] T019 [Person 1] Create `vpa/data/__init__.py` and base dataset interface
- [ ] T020 [Person 3] Create `vpa/eval/metrics.py` with metric computation utilities (EM, F1 helpers)
- [ ] T021 [Person 1] Create `vpa/verify/base.py` with abstract Verifier interface
- [ ] T022 [Person 3] Create `tests/unit/test_utils.py` for utility function tests

## Phase 3: User Story 1 - Draft Generation (Week 1-2, Person 1)

**Story Goal**: Generate k diverse candidate answers with optional tool support

**Independent Test**: Generate k=5 candidates for HotpotQA question in <10s with tools logged

- [ ] T023 [US1] [Person 1] Create `vpa/draft/__init__.py` and draft module structure
- [ ] T024 [US1] [Person 1] Create `vpa/draft/config.py` with DraftConfig dataclass (k, temperature, top_p, tools)
- [ ] T025 [US1] [Person 1] Implement `vpa/draft/generator.py` with Generator class for k-sampling
- [ ] T026 [US1] [Person 1] Add temperature and top_p sampling controls to Generator
- [ ] T027 [US1] [Person 1] Add batched generation support for parallel candidate generation
- [ ] T028 [US1] [Person 1] Create `vpa/draft/tools.py` with Tool base class and registry
- [ ] T029 [US1] [Person 1] Implement RetrievalTool wrapper (using LangChain or LlamaIndex)
- [ ] T030 [US1] [Person 1] Implement PythonExecTool wrapper with sandbox (subprocess or Docker)
- [ ] T031 [US1] [Person 1] Implement CalculatorTool wrapper with safe eval
- [ ] T032 [US1] [Person 1] Add tool call logging and metadata tracking to Generator
- [ ] T033 [US1] [Person 1] Create `vpa/data/loaders.py` with HotpotQA dataset loader
- [ ] T034 [US1] [Person 1] Add MBPP dataset loader to `vpa/data/loaders.py`
- [ ] T035 [US1] [Person 1] Add GSM8K dataset loader to `vpa/data/loaders.py`
- [ ] T036 [US1] [Person 1] Create `vpa/data/builders.py` to build (input, output, evidence) tuples
- [ ] T037 [US1] [Person 1] Create `vpa/data/splits.py` for train/val/test/stability split logic
- [ ] T038 [US1] [Person 1] Write unit tests in `tests/unit/test_draft.py` for Generator
- [ ] T039 [US1] [Person 1] Write unit tests in `tests/unit/test_tools.py` for each tool
- [ ] T040 [US1] [Person 1] Write integration test in `tests/integration/test_tool_integration.py`

## Phase 4: User Story 2 - Verifier Ensemble (Week 2, Person 1)

**Story Goal**: Score candidates with factual/formal/style verifiers producing diagnostics

**Independent Test**: Verify 5 candidates in <5s with per-channel scores and diagnostics

- [ ] T041 [US2] [Person 1] Implement `vpa/verify/factual.py` with FactualVerifier class
- [ ] T042 [US2] [Person 1] Add citation overlap scoring to FactualVerifier (using sentence similarity)
- [ ] T043 [US2] [Person 1] Add contradiction detection to FactualVerifier (using NLI model)
- [ ] T044 [US2] [Person 1] Add evidence support scoring to FactualVerifier
- [ ] T045 [US2] [Person 1] Implement `vpa/verify/formal.py` with FormalVerifier class
- [ ] T046 [US2] [Person 1] Add unit test execution to FormalVerifier (for code candidates)
- [ ] T047 [US2] [Person 1] Add schema validation to FormalVerifier (using Pydantic or JSON Schema)
- [ ] T048 [US2] [Person 1] Add syntax checking to FormalVerifier (using ast.parse for Python)
- [ ] T049 [US2] [Person 1] Implement `vpa/verify/style.py` with StyleVerifier class
- [ ] T050 [US2] [Person 1] Add formatting checks to StyleVerifier (length, structure)
- [ ] T051 [US2] [Person 1] Add safety checks to StyleVerifier (toxicity detection, basic filtering)
- [ ] T052 [US2] [Person 1] Implement `vpa/verify/ensemble.py` with EnsembleVerifier class
- [ ] T053 [US2] [Person 1] Add composite scoring logic to EnsembleVerifier (weighted average)
- [ ] T054 [US2] [Person 1] Add diagnostic aggregation to EnsembleVerifier (collect all channel messages)
- [ ] T055 [US2] [Person 1] Add parallel verification support to EnsembleVerifier
- [ ] T056 [US2] [Person 1] Write unit tests in `tests/unit/test_verifiers.py` for each verifier
- [ ] T057 [US2] [Person 1] Write contract tests in `tests/contract/test_verifier_interface.py`

## Phase 5: User Story 3 - Planner (Week 2-3, Person 2)

**Story Goal**: Analyze verifier diagnostics and propose self-edit plans

**Independent Test**: Given low citation scores, planner suggests retrieval tool and k=7

- [ ] T058 [US3] [Person 2] Create `vpa/plan/__init__.py` and plan module structure
- [ ] T059 [US3] [Person 2] Create `vpa/plan/config.py` with PlanConfig dataclass
- [ ] T060 [US3] [Person 2] Create `vpa/plan/action_grid.py` defining action space (k values, tools, LoRA params)
- [ ] T061 [US3] [Person 2] Implement `vpa/plan/planner.py` with Planner class
- [ ] T062 [US3] [Person 2] Add diagnostic analysis logic to Planner (parse verifier messages)
- [ ] T063 [US3] [Person 2] Implement rejection sampling over action grid in Planner
- [ ] T064 [US3] [Person 2] Add k adjustment proposal logic (if quality low, increase k)
- [ ] T065 [US3] [Person 2] Add tool selection proposal logic (if factual errors, enable retrieval)
- [ ] T066 [US3] [Person 2] Add LoRA hyperparameter proposal logic (if quality acceptable, suggest training)
- [ ] T067 [US3] [Person 2] Write unit tests in `tests/unit/test_planner.py`
- [ ] T068 [US3] [Person 2] Write contract tests in `tests/contract/test_planner_interface.py`

## Phase 6: User Story 4 - LoRA Training (Week 3, Person 2)

**Story Goal**: Train small LoRA adapters on verified corrections

**Independent Test**: Train rank-8 adapter on 100 examples, converges in <100 steps

- [ ] T069 [US4] [Person 2] Create `vpa/apply/__init__.py` and apply module structure
- [ ] T070 [US4] [Person 2] Create `vpa/apply/config.py` with LoRAConfig and TrainingConfig
- [ ] T071 [US4] [Person 2] Implement `vpa/apply/lora_trainer.py` with LoRATrainer class
- [ ] T072 [US4] [Person 2] Add PEFT LoRA setup to LoRATrainer (using HuggingFace PEFT)
- [ ] T073 [US4] [Person 2] Implement SFT training loop in LoRATrainer
- [ ] T074 [US4] [Person 2] Add training data preparation (convert verified corrections to prompts)
- [ ] T075 [US4] [Person 2] Add loss tracking and early stopping to LoRATrainer
- [ ] T076 [US4] [Person 2] Add checkpoint saving with metadata (rank, domain, data hash) to LoRATrainer
- [ ] T077 [US4] [Person 2] Add adapter loading and inference to LoRATrainer
- [ ] T078 [US4] [Person 2] Implement adapter versioning (domain tags, version numbers)
- [ ] T079 [US4] [Person 2] Write unit tests in `tests/unit/test_lora_trainer.py`
- [ ] T080 [US4] [Person 2] Create experiment config templates in `configs/experiments/`

## Phase 7: User Story 5 - Regression Gate (Week 3-4, Person 3)

**Story Goal**: Validate adapters against frozen stability set with pass/fail decision

**Independent Test**: Load adapter, run gate on 200 examples in <5min, output metrics

- [ ] T081 [US5] [Person 3] Implement `vpa/apply/gate.py` with Gate class
- [ ] T082 [US5] [Person 3] Add stability set construction logic to Gate (frozen 20% of training data)
- [ ] T083 [US5] [Person 3] Implement adapter evaluation on stability set in Gate
- [ ] T084 [US5] [Person 3] Add acceptance criteria checking (≥3 EM or ≥5 pass@1 improvement)
- [ ] T085 [US5] [Person 3] Add regression detection logic (>3 point drop on any metric)
- [ ] T086 [US5] [Person 3] Implement pass/fail decision and logging in Gate
- [ ] T087 [US5] [Person 3] Add quarantine logic for failed adapters (move to quarantine directory)
- [ ] T088 [US5] [Person 3] Create `vpa/eval/experiment.py` with ExperimentRun tracking class
- [ ] T089 [US5] [Person 3] Add WandB or TensorBoard integration to ExperimentRun
- [ ] T090 [US5] [Person 3] Write unit tests in `tests/unit/test_gate.py`

## Phase 8: Evaluation Infrastructure (Week 4, Person 3)

**Story Goal**: Implement all metrics and evaluation harnesses for QA/code/math

**Independent Test**: Evaluate model on HotpotQA with EM/F1, MBPP with pass@k

- [ ] T091 [Person 3] Implement exact match (EM) metric in `vpa/eval/metrics.py`
- [ ] T092 [Person 3] Implement F1 score metric in `vpa/eval/metrics.py`
- [ ] T093 [Person 3] Implement pass@k metric with code execution in `vpa/eval/metrics.py`
- [ ] T094 [Person 3] Implement accuracy metric in `vpa/eval/metrics.py`
- [ ] T095 [Person 3] Implement Brier score metric in `vpa/eval/metrics.py`
- [ ] T096 [Person 3] Implement ECE (Expected Calibration Error) in `vpa/eval/metrics.py`
- [ ] T097 [Person 3] Implement hallucination rate metric in `vpa/eval/metrics.py`
- [ ] T098 [Person 3] Create `vpa/eval/qa_eval.py` with QA evaluation harness
- [ ] T099 [Person 3] Add EM/F1 evaluation for HotpotQA to qa_eval.py
- [ ] T100 [Person 3] Create `vpa/eval/code_eval.py` with code evaluation harness
- [ ] T101 [Person 3] Add pass@k evaluation for MBPP to code_eval.py
- [ ] T102 [Person 3] Add pass@k evaluation for HumanEval to code_eval.py
- [ ] T103 [Person 3] Create `vpa/eval/math_eval.py` with math evaluation harness
- [ ] T104 [Person 3] Add accuracy evaluation for GSM8K to math_eval.py
- [ ] T105 [Person 3] Write unit tests in `tests/unit/test_metrics.py`

## Phase 9: User Story 6 - Adapter Routing (Week 4, Person 2)

**Story Goal**: Route queries to domain-specific adapters using similarity metrics

**Independent Test**: Given coding query, router selects "code" adapter with >0.8 confidence

- [ ] T106 [US6] [Person 2] Implement `vpa/apply/router.py` with AdapterRouter class
- [ ] T107 [US6] [Person 2] Add domain classification logic to AdapterRouter (using keyword matching or classifier)
- [ ] T108 [US6] [Person 2] Add embedding similarity logic to AdapterRouter (using sentence-transformers)
- [ ] T109 [US6] [Person 2] Add confidence scoring to AdapterRouter
- [ ] T110 [US6] [Person 2] Add fallback logic to AdapterRouter (use base model if no match)
- [ ] T111 [US6] [Person 2] Add adapter composition logic (optional: merge multiple adapters)
- [ ] T112 [US6] [Person 2] Write unit tests in `tests/unit/test_router.py`
- [ ] T113 [US6] [Person 2] Write integration tests in `tests/integration/test_adapter_routing.py`

## Phase 10: CLI Interface (Week 4-5, Person 3)

**Story Goal**: Provide command-line interface for all pipeline stages

**Independent Test**: Run `vpa draft --dataset hotpotqa --k 5` and get 5 candidates

- [ ] T114 [Person 3] Create `vpa/cli/__init__.py` and CLI module structure
- [ ] T115 [Person 3] Create `vpa/cli/main.py` with Click or argparse CLI entry point
- [ ] T116 [Person 3] Create `vpa/cli/config.py` with global CLI configuration
- [ ] T117 [Person 3] Implement `vpa/cli/commands/draft.py` for draft generation command
- [ ] T118 [Person 3] Implement `vpa/cli/commands/verify.py` for verification command
- [ ] T119 [Person 3] Implement `vpa/cli/commands/plan.py` for planner command
- [ ] T120 [Person 3] Implement `vpa/cli/commands/train.py` for adapter training command
- [ ] T121 [Person 3] Implement `vpa/cli/commands/gate.py` for gate evaluation command
- [ ] T122 [Person 3] Implement `vpa/cli/commands/eval.py` for evaluation command
- [ ] T123 [Person 3] Add rich output formatting to CLI commands (tables, progress bars)
- [ ] T124 [Person 3] Create `scripts/run_mvp_pipeline.sh` demonstrating full pipeline
- [ ] T125 [Person 3] Create `scripts/train_adapter.sh` for training single adapter
- [ ] T126 [Person 3] Create `scripts/run_experiments.sh` for running all experiments

## Phase 11: Integration Testing (Week 5, All Team)

**Story Goal**: Test end-to-end pipeline and ensure all components work together

**Independent Test**: Run full Draft→Verify→Plan→Apply→Gate pipeline on 10 examples

- [ ] T127 Create `tests/integration/test_pipeline.py` with end-to-end tests
- [ ] T128 [Person 1] Add test for Draft→Verify integration
- [ ] T129 [Person 2] Add test for Verify→Plan integration
- [ ] T130 [Person 2] Add test for Plan→Apply integration
- [ ] T131 [Person 3] Add test for Apply→Gate integration
- [ ] T132 [Person 3] Add test for full pipeline on small synthetic dataset (10 examples)
- [ ] T133 [Person 1] Add test for tool integration (retrieval + code execution)
- [ ] T134 [Person 2] Add test for adapter merging and composition
- [ ] T135 [Person 3] Add test for experiment tracking and logging
- [ ] T136 Run integration tests and fix any failures
- [ ] T137 [Person 3] Set up CI to run integration tests on PRs

## Phase 12: Baseline Experiments (Week 6, All Team)

**Story Goal**: Run baseline experiments and initial VPA experiments

**Independent Test**: Baseline results on HotpotQA, MBPP, GSM8K with standard metrics

- [ ] T138 [Person 1] Prepare datasets with proper splits (train/val/test/stability)
- [ ] T139 [Person 3] Create experiment configs for baseline (base model + best-of-N)
- [ ] T140 [Person 3] Run baseline experiment on HotpotQA (100 examples)
- [ ] T141 [Person 3] Run baseline experiment on MBPP (100 examples)
- [ ] T142 [Person 3] Run baseline experiment on GSM8K (100 examples)
- [ ] T143 [Person 1] Generate 500 training examples with Draft+Verify for HotpotQA
- [ ] T144 [Person 2] Train HotpotQA adapter (rank=8, 100 steps)
- [ ] T145 [Person 3] Run gate evaluation on HotpotQA adapter
- [ ] T146 [Person 3] Evaluate HotpotQA adapter on test set (EM/F1)
- [ ] T147 [Person 1] Generate 500 training examples for MBPP
- [ ] T148 [Person 2] Train MBPP adapter (rank=16, 100 steps)
- [ ] T149 [Person 3] Run gate evaluation on MBPP adapter
- [ ] T150 [Person 3] Evaluate MBPP adapter on test set (pass@1, pass@5)
- [ ] T151 [Person 1] Generate 500 training examples for GSM8K
- [ ] T152 [Person 2] Train GSM8K adapter (rank=8, 100 steps)
- [ ] T153 [Person 3] Run gate evaluation on GSM8K adapter
- [ ] T154 [Person 3] Evaluate GSM8K adapter on test set (accuracy)
- [ ] T155 [Person 3] Generate initial result tables comparing baseline vs VPA

## Phase 13: Ablation Studies (Week 7, All Team)

**Story Goal**: Run ablation studies to answer RQ4 (which verifier signals matter most)

**Independent Test**: Compare VPA with/without each verifier channel

- [ ] T156 [Person 3] Create experiment configs for ablations
- [ ] T157 [Person 1] Run VPA without factual verifier on HotpotQA (keep formal+style)
- [ ] T158 [Person 1] Run VPA without formal verifier on MBPP (keep factual+style)
- [ ] T159 [Person 1] Run VPA without style verifier on all datasets (keep factual+formal)
- [ ] T160 [Person 2] Run VPA with random planner (no diagnostics) on all datasets
- [ ] T161 [Person 3] Run VPA without gate (merge all adapters) on all datasets
- [ ] T162 [Person 3] Collect and compare ablation results
- [ ] T163 [Person 3] Generate plots showing impact of each component

## Phase 14: Advanced Experiments (Week 7, Person 2 & 3)

**Story Goal**: Run advanced experiments (multi-adapter, calibration analysis)

**Independent Test**: Evaluate calibration (Brier, ECE) and multi-adapter routing

- [ ] T164 [Person 2] Experiment with adapter composition (merge HotpotQA + GSM8K adapters)
- [ ] T165 [Person 2] Experiment with LoRA hyperparameter sweep (ranks 4/8/16, lr 1e-4/1e-5)
- [ ] T166 [Person 3] Compute calibration metrics (Brier score, ECE) for all experiments
- [ ] T167 [Person 3] Generate calibration plots (reliability diagrams)
- [ ] T168 [Person 3] Measure GPU-hours for VPA vs RL baseline (hypothetical comparison)
- [ ] T169 [Person 3] Generate Pareto curves (performance vs cost)

## Phase 15: Paper Prep & Reproducibility (Week 8, All Team)

**Story Goal**: Finalize experiments, generate plots, ensure reproducibility

**Independent Test**: External researcher can reproduce results using docs and configs

- [ ] T170 [Person 3] Re-run all experiments with 3 different random seeds
- [ ] T171 [Person 3] Compute mean and standard deviation for all metrics
- [ ] T172 [Person 3] Generate final result tables for paper (baseline, VPA, ablations)
- [ ] T173 [Person 3] Generate all plots: Pareto curves, calibration plots, ablation comparisons
- [ ] T174 Create `docs/architecture.md` documenting system design
- [ ] T175 Create `docs/verifier_guide.md` explaining how to add new verifiers
- [ ] T176 Create `docs/adapter_guide.md` explaining adapter training workflow
- [ ] T177 Create `docs/evaluation_guide.md` explaining evaluation procedures
- [ ] T178 Update main `README.md` with installation, usage, and reproduction instructions
- [ ] T179 Create reproducibility checklist (configs, seeds, data splits, model versions)
- [ ] T180 Archive all experiment configs, results, and plots
- [ ] T181 Run final constitution compliance check on all code
- [ ] T182 Polish code: add docstrings, type hints, comments
- [ ] T183 Create release tag and GitHub release with reproducibility package

## Summary Statistics

**Total Tasks**: 183
**Tasks per Person**:
- Person 1 (Draft/Verify): ~50 tasks (T023-T057, T138-T159)
- Person 2 (Plan/Apply): ~50 tasks (T058-T080, T106-T113, T144-T165)
- Person 3 (Eval/Gate/CLI): ~60 tasks (T081-T105, T114-T137, T140-T183)
- Shared/All: ~23 tasks (T001-T022, T127-T137, T170-T183)

**Parallel Opportunities**:
- Phase 1 (Setup): All 15 tasks can run in parallel with coordination
- Phase 2 (Foundation): 7 tasks can run in parallel across 3 people
- Phases 3-6 (User Stories): ~130 tasks can run largely in parallel by person
- Phase 11 (Integration): Some parallelism, requires coordination
- Phases 12-15 (Experiments): High parallelism, each person runs different experiments

**Timeline**:
- Weeks 1-2: MVP (Phases 1-7, ~100 tasks)
- Weeks 3-5: Full System (Phases 8-11, ~50 tasks)
- Weeks 6-8: Experiments & Paper (Phases 12-15, ~33 tasks)

## Implementation Strategy

**MVP First** (Weeks 1-2): Focus on getting one working example through the full pipeline:
- Draft 5 candidates for one HotpotQA question
- Verify with all three verifiers
- Train tiny adapter on 50 examples
- Run gate evaluation
- This validates the architecture end-to-end

**Incremental Delivery** (Weeks 3-5): Add datasets, polish, comprehensive testing

**Evaluation Focus** (Weeks 6-8): Run all experiments, generate plots, ensure reproducibility
