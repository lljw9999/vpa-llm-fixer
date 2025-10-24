# VPA MVP Team Assignments - 3 Person Team

**Project**: VPA (Verifier → Plan → Apply) Framework
**Timeline**: 8 weeks (MVP in 2 weeks, full system in 8 weeks)
**Date**: 2025-10-24

---

## Quick Start Guide

### Day 1: All Team Members

1. **Review project documents** (1-2 hours):
   - Read `Readme.md` in project root
   - Read `specs/001-vpa-mvp/spec.md` (feature specification)
   - Read `specs/001-vpa-mvp/plan.md` (implementation plan)
   - Review `.specify/memory/constitution.md` (project principles)

2. **Set up development environment** (1 hour):
   - Clone repository
   - Create feature branch: `git checkout -b 001-vpa-mvp`
   - Run `scripts/setup_env.sh` (to be created on Day 1)
   - Install Python 3.11, PyTorch, Transformers, PEFT

3. **Complete Phase 1 setup tasks** (2-3 hours):
   - Work through tasks T001-T015 in `tasks.md`
   - Create project structure, configs, and initial setup
   - Coordinate via shared document or meeting

4. **Review your personal assignment** (30 mins):
   - Person 1: Read "Person 1: Draft & Verify Lead" section below
   - Person 2: Read "Person 2: Plan & Apply Lead" section below
   - Person 3: Read "Person 3: Eval, Gate & CLI Lead" section below

### Week 1 Schedule

- **Days 1-2**: Setup + Phase 0 Research (all team members research their domains)
- **Days 3-5**: Phase 1 Design (create data models, contracts, quickstart docs)

### Week 2 Schedule

- **Days 1-3**: Core implementation (Draft/Verify, Plan/Apply, Eval/Gate)
- **Days 4-5**: Integration and MVP demo (run one example through full pipeline)

---

## Person 1: Draft & Verify Lead

### Your Mission

You own the **input side** of the VPA pipeline: generating diverse candidate answers and verifying their quality. Your modules are the foundation that everything else builds on.

### Your Modules

- `vpa/draft/` - Draft generation with k-sampling and tool support
- `vpa/verify/` - Verifier ensemble (factual, formal, style)
- `vpa/data/` - Dataset loading and preparation

### Your Responsibilities

#### Week 1: Research & Design

**Phase 0 Research** (Days 2-3):
- Research factual verification approaches (citation checking, contradiction detection)
- Survey libraries: FactScore, sentence-transformers, NLI models
- Document findings in `research.md` section "Verifier Approaches"
- Research tool integration safety (code execution sandboxing, timeout handling)
- Document findings in `research.md` section "Tool Integration"

**Phase 1 Design** (Days 3-5):
- Define Draft entity in `data-model.md` (candidate text, metadata, tool_calls)
- Define VerifierScore entity in `data-model.md` (per-channel scores, diagnostics)
- Define Dataset entity in `data-model.md` (questions, answers, evidence, splits)
- Create `contracts/verifier_api.yaml` (OpenAPI spec for verifier interface)
- Contribute to `quickstart.md` scenarios 1-2 (draft generation, verification)

#### Week 2: Core Implementation

**User Story 1 - Draft Generation** (Tasks T023-T040):
- Implement `Generator` class with k-sampling, temperature, top_p controls
- Implement tool wrappers: `RetrievalTool`, `PythonExecTool`, `CalculatorTool`
- Implement dataset loaders for HotpotQA, MBPP, GSM8K
- Write comprehensive unit tests for all components
- **Target**: Generate k=5 candidates in <10s with tools working

**User Story 2 - Verifier Ensemble** (Tasks T041-T057):
- Implement `FactualVerifier` with citation overlap, contradiction detection
- Implement `FormalVerifier` with unit test execution, schema validation
- Implement `StyleVerifier` with formatting and safety checks
- Implement `EnsembleVerifier` with composite scoring
- Write unit and contract tests
- **Target**: Verify 5 candidates in <5s with interpretable diagnostics

#### Weeks 3-4: Dataset Preparation & Integration

- Prepare datasets with proper train/val/test/stability splits (T138)
- Generate 500 training examples for each dataset using Draft+Verify (T143, T147, T151)
- Integrate with Person 2's planner and Person 3's evaluators
- Test Draft→Verify integration (T128)

#### Weeks 5-8: Experiments & Refinement

- Run verifier ablation studies (T157-T159)
- Support baseline and VPA experiments
- Polish verifier diagnostics based on experiment feedback
- Write `docs/verifier_guide.md` (T175)

### Your Key Files

**To Create**:
- `vpa/draft/generator.py`
- `vpa/draft/tools.py`
- `vpa/draft/config.py`
- `vpa/verify/factual.py`
- `vpa/verify/formal.py`
- `vpa/verify/style.py`
- `vpa/verify/ensemble.py`
- `vpa/data/loaders.py`
- `vpa/data/builders.py`
- `vpa/data/splits.py`
- `tests/unit/test_draft.py`
- `tests/unit/test_tools.py`
- `tests/unit/test_verifiers.py`
- `tests/contract/test_verifier_interface.py`

**Your Checklist**: `specs/001-vpa-mvp/checklists/person1-draft-verify.md`

### Success Criteria

- [ ] Draft generation works on all 3 datasets (HotpotQA, MBPP, GSM8K)
- [ ] All 3 tool types work (retrieval, Python exec, calculator)
- [ ] All 3 verifier channels produce reliable scores (factual, formal, style)
- [ ] Verifier ensemble composites scores correctly
- [ ] Performance targets met (<10s draft, <5s verify)
- [ ] Test coverage >80% for your modules
- [ ] 500 verified training examples generated per dataset

### Daily Check-ins

Share updates on:
- Verifier reliability (do scores make sense?)
- Tool integration issues (sandboxing, timeouts)
- Dataset loading challenges
- Performance bottlenecks

---

## Person 2: Plan & Apply Lead

### Your Mission

You own the **learning side** of the VPA pipeline: analyzing verifier results to propose improvements and training LoRA adapters that make those improvements stick.

### Your Modules

- `vpa/plan/` - Planner with rejection sampling over action grid
- `vpa/apply/` - LoRA training, adapter routing, checkpointing

### Your Responsibilities

#### Week 1: Research & Design

**Phase 0 Research** (Days 2-3):
- Research LoRA best practices (rank selection, learning rates, convergence)
- Survey papers: QLoRA, LoRA+, AdaLoRA
- Check HuggingFace PEFT examples and documentation
- Document findings in `research.md` section "LoRA Best Practices"
- Research adapter composition and routing strategies
- Document findings in `research.md` section "Adapter Routing"

**Phase 1 Design** (Days 3-5):
- Define Plan entity in `data-model.md` (k_adjustment, tool_selections, lora_params)
- Define LoRAAdapter entity in `data-model.md` (checkpoint_path, rank, domain, metadata)
- Create `contracts/planner_api.yaml` (OpenAPI spec for planner interface)
- Contribute to `quickstart.md` scenario 3 (train small adapter)

#### Week 2-3: Core Implementation

**User Story 3 - Planner** (Tasks T058-T068):
- Implement `Planner` class with diagnostic analysis
- Create action grid with k values, tool selections, LoRA hyperparameters
- Implement rejection sampling over action grid
- Write unit and contract tests
- **Target**: Planner proposes sensible actions based on verifier diagnostics

**User Story 4 - LoRA Training** (Tasks T069-T080):
- Implement `LoRATrainer` class with PEFT integration
- Implement SFT training loop with loss tracking and early stopping
- Implement checkpoint saving with metadata (rank, domain, data hash, seed)
- Implement adapter loading and inference
- Create experiment config templates
- Write unit tests
- **Target**: Train rank-8 adapter on 100 examples in <100 steps

#### Week 4: Adapter Routing

**User Story 6 - Adapter Routing** (Tasks T106-T113):
- Implement `AdapterRouter` class with domain classification
- Add embedding similarity routing with confidence scores
- Add fallback logic (use base model if no match)
- Optional: Implement adapter composition/merging
- Write unit and integration tests
- **Target**: Router selects correct adapter with >0.8 confidence

#### Weeks 5-8: Training & Experiments

- Train adapters for all 3 datasets (HotpotQA, MBPP, GSM8K) - Tasks T144, T148, T152
- Work with Person 3 on gate evaluation
- Support adapter ablation studies
- Experiment with multi-adapter routing (T164)
- Run LoRA hyperparameter sweeps (T165)
- Write `docs/adapter_guide.md` (T176)

### Your Key Files

**To Create**:
- `vpa/plan/planner.py`
- `vpa/plan/action_grid.py`
- `vpa/plan/config.py`
- `vpa/apply/lora_trainer.py`
- `vpa/apply/router.py`
- `vpa/apply/config.py`
- `vpa/utils/checkpointing.py`
- `configs/planner_grid.yaml`
- `configs/experiments/hotpotqa_baseline.yaml`
- `configs/experiments/mbpp_baseline.yaml`
- `configs/experiments/gsm8k_baseline.yaml`
- `tests/unit/test_planner.py`
- `tests/unit/test_lora_trainer.py`
- `tests/unit/test_router.py`
- `tests/contract/test_planner_interface.py`

**Your Checklist**: `specs/001-vpa-mvp/checklists/person2-plan-apply.md`

### Success Criteria

- [ ] Planner produces sensible action proposals from verifier diagnostics
- [ ] LoRA training converges consistently in <100 steps for rank ≤16
- [ ] Adapters improve on target domain (validated by Person 3's gate)
- [ ] Adapter routing works correctly for different query types
- [ ] All 3 dataset adapters trained successfully and pass gate
- [ ] Test coverage >80% for your modules
- [ ] Adapter versioning and metadata tracking works

### Daily Check-ins

Share updates on:
- Planner action quality (do proposals make sense?)
- Training stability (convergence, loss curves, NaN issues)
- Adapter quality (do they improve model outputs?)
- Routing accuracy (does router pick right adapter?)

---

## Person 3: Eval, Gate & CLI Lead

### Your Mission

You own **quality control and user experience**: ensuring adapters actually improve performance without regressions, providing a great CLI, and running all experiments to validate VPA.

### Your Modules

- `vpa/eval/` - Metrics and evaluation harnesses
- `vpa/apply/gate.py` - Regression gate (NON-NEGOTIABLE per constitution)
- `vpa/cli/` - Command-line interface for all pipeline stages
- `tests/` - All testing infrastructure

### Your Responsibilities

#### Week 1: Research & Design

**Phase 0 Research** (Days 2-3):
- Research evaluation metrics (pass@k, ECE, Brier score implementations)
- Survey libraries: EleutherAI lm-evaluation-harness, HuggingFace evaluate
- Document findings in `research.md` section "Evaluation Metrics"
- Research gate design and stability set construction
- Survey continual learning papers (EWC, PackNet)
- Document findings in `research.md` section "Gate Design"

**Phase 1 Design** (Days 3-5):
- Define GateResult entity in `data-model.md` (pass/fail, metrics, timestamp)
- Define ExperimentRun entity in `data-model.md` (all metadata fields)
- Contribute to `quickstart.md` scenarios 4-5 (gate evaluation, full pipeline)
- Design stability set construction strategy

#### Week 2: Foundational Infrastructure

**Phase 2 - Utilities** (Tasks T016-T022):
- Create `vpa/utils/logging.py` with structured logging
- Create `vpa/utils/seed.py` with reproducible random seeds
- Create `vpa/eval/metrics.py` with basic metric helpers (EM, F1)
- Write unit tests for utilities

#### Week 3-4: Evaluation & Gate

**User Story 5 - Regression Gate** (Tasks T081-T090):
- Implement `Gate` class with stability set construction (frozen 20% of data)
- Implement adapter evaluation with acceptance criteria (≥3 EM or ≥5 pass@1)
- Implement regression detection (>3 point drop on any metric)
- Implement quarantine logic for failed adapters
- Create `ExperimentRun` tracker with WandB/TensorBoard integration
- Write unit tests
- **Target**: Gate evaluates adapter in <5min with pass/fail decision

**Evaluation Infrastructure** (Tasks T091-T105):
- Implement all metrics: EM, F1, pass@k, accuracy, Brier, ECE, hallucination rate
- Create QA evaluation harness (HotpotQA with EM/F1)
- Create code evaluation harness (MBPP/HumanEval with pass@k)
- Create math evaluation harness (GSM8K with accuracy)
- Write comprehensive unit tests for all metrics
- **Target**: All metrics work correctly on test examples

#### Week 4-5: CLI & Integration

**CLI Interface** (Tasks T114-T126):
- Create CLI entry point with subcommands (draft, verify, plan, train, gate, eval)
- Implement each CLI command with proper argument parsing
- Add rich output formatting (tables, progress bars)
- Create helper scripts (run_mvp_pipeline.sh, train_adapter.sh, run_experiments.sh)
- **Target**: CLI is user-friendly and well-documented

**Integration Testing** (Tasks T127-T137):
- Write end-to-end pipeline tests (Draft→Verify→Plan→Apply→Gate)
- Test all module integrations
- Set up CI to run tests on PRs
- **Target**: Full pipeline works on 10 examples

#### Weeks 5-6: Baseline Experiments

**Run All Baselines** (Tasks T138-T155):
- Prepare datasets with proper splits
- Run baseline experiments (base model + best-of-N) on all 3 datasets
- Work with Person 2 to evaluate trained adapters through gate
- Evaluate adapters on test sets
- Generate initial result tables
- **Target**: Baseline and initial VPA results documented

#### Week 7: Ablation Studies

**Ablations & Analysis** (Tasks T156-T169):
- Run verifier ablations (remove each channel)
- Run planner ablations (random planner)
- Run gate ablations (no gate)
- Compute calibration metrics (Brier, ECE)
- Generate all analysis plots
- **Target**: Answer RQ4 (which verifier signals matter most?)

#### Week 8: Paper Prep & Reproducibility

**Finalize Everything** (Tasks T170-T183):
- Re-run all experiments with 3 seeds
- Compute mean and std for all metrics
- Generate publication-ready tables and plots
- Write architecture and evaluation guides
- Update README with full instructions
- Create reproducibility checklist
- Archive all configs and results
- Polish code and run final constitution check
- Create GitHub release
- **Target**: External researcher can reproduce all results

### Your Key Files

**To Create**:
- `vpa/eval/metrics.py`
- `vpa/eval/qa_eval.py`
- `vpa/eval/code_eval.py`
- `vpa/eval/math_eval.py`
- `vpa/eval/experiment.py`
- `vpa/apply/gate.py`
- `vpa/cli/main.py`
- `vpa/cli/commands/*.py` (draft, verify, plan, train, gate, eval)
- `vpa/utils/logging.py`
- `vpa/utils/seed.py`
- `scripts/setup_env.sh`
- `scripts/download_models.sh`
- `scripts/download_datasets.sh`
- `scripts/run_mvp_pipeline.sh`
- `scripts/train_adapter.sh`
- `scripts/run_experiments.sh`
- `tests/unit/test_metrics.py`
- `tests/unit/test_gate.py`
- `tests/unit/test_utils.py`
- `tests/integration/test_pipeline.py`
- `.github/workflows/tests.yml`
- `.github/workflows/constitution_check.yml`
- `docs/architecture.md`
- `docs/evaluation_guide.md`

**Your Checklist**: `specs/001-vpa-mvp/checklists/person3-eval-gate-cli.md`

### Success Criteria

- [ ] All metrics implemented correctly and tested
- [ ] Gate works reliably and enforces constitution principles (NON-NEGOTIABLE)
- [ ] CLI is user-friendly with good documentation
- [ ] All tests pass (unit, integration, contract) with >80% coverage
- [ ] CI/CD pipeline runs automatically on PRs
- [ ] All baseline and VPA experiments completed
- [ ] All ablation studies completed
- [ ] Publication-ready results (tables, plots, reproducibility docs)
- [ ] External researcher can reproduce results

### Daily Check-ins

Share updates on:
- Gate reliability (are pass/fail decisions correct?)
- Metric correctness (do results match expectations?)
- CLI usability issues
- Test failures or coverage gaps
- Experiment progress and results

---

## Communication & Coordination

### Daily Standups (15 minutes)

Each person shares:
1. What I completed yesterday
2. What I'm working on today
3. Any blockers or questions

### Weekly Sync (1 hour)

Review progress against timeline:
- Demo working features
- Discuss integration challenges
- Adjust priorities if needed
- Plan next week's tasks

### Integration Points

**Week 2 (MVP Integration)**:
- Person 1 provides draft and verify modules → Person 2 uses for training data
- Person 2 provides trained adapters → Person 3 runs through gate
- Person 3 provides CLI → All use for testing

**Week 5 (Full Pipeline Integration)**:
- All team: Run end-to-end tests together
- All team: Debug integration issues as a group
- All team: Demo MVP to stakeholders

**Week 6+ (Experiments)**:
- Person 1 focuses on verifier ablations
- Person 2 focuses on adapter experiments
- Person 3 orchestrates all experiments and collects results

### Shared Documents

- **Progress Tracker**: Shared spreadsheet with task completion status
- **Blockers Log**: Document any issues blocking progress
- **Decisions Log**: Record important technical decisions
- **Results Sheet**: Collect all experiment results

### Git Workflow

1. All work on feature branch `001-vpa-mvp`
2. Create sub-branches for major features: `001-vpa-mvp-draft`, `001-vpa-mvp-gate`, etc.
3. Pull requests for code review before merging to feature branch
4. Person 3 runs CI checks on all PRs

---

## Success Milestones

### Week 2 (MVP Checkpoint)

- [ ] Can generate 5 candidates for one HotpotQA question
- [ ] Can verify 5 candidates with ensemble scoring
- [ ] Can train tiny adapter on 50 examples
- [ ] Can run gate evaluation on adapter
- [ ] CLI works for basic commands
- [ ] All team members have working dev environment

### Week 5 (Full System Checkpoint)

- [ ] All 3 datasets work end-to-end
- [ ] All tool integrations work (retrieval, code exec, calculator)
- [ ] Adapter routing works
- [ ] Gate passes/fails adapters correctly
- [ ] Full test suite runs on CI
- [ ] Integration tests pass

### Week 6 (Baseline Results Checkpoint)

- [ ] Baseline experiments complete on all datasets
- [ ] Initial VPA experiments complete on all datasets
- [ ] At least one adapter passes gate
- [ ] Initial result tables generated

### Week 8 (Publication Readiness Checkpoint)

- [ ] All experiments run with 3 seeds
- [ ] All ablations complete
- [ ] All plots generated (publication quality)
- [ ] All documentation complete
- [ ] Reproducibility verified
- [ ] GitHub release created

---

## Quick Reference

### Your Tasks File
See `specs/001-vpa-mvp/tasks.md` for detailed task breakdown (183 tasks total)

### Your Checklist
- Person 1: `specs/001-vpa-mvp/checklists/person1-draft-verify.md` (54 checks)
- Person 2: `specs/001-vpa-mvp/checklists/person2-plan-apply.md` (76 checks)
- Person 3: `specs/001-vpa-mvp/checklists/person3-eval-gate-cli.md` (116 checks)

### Your Modules
- Person 1: `vpa/draft/`, `vpa/verify/`, `vpa/data/`
- Person 2: `vpa/plan/`, `vpa/apply/` (minus gate.py)
- Person 3: `vpa/eval/`, `vpa/apply/gate.py`, `vpa/cli/`, `tests/`, `scripts/`

### Key Documents
- Project README: `Readme.md`
- Feature Spec: `specs/001-vpa-mvp/spec.md`
- Implementation Plan: `specs/001-vpa-mvp/plan.md`
- Constitution: `.specify/memory/constitution.md`

---

## Questions?

If unclear about:
- **Your responsibilities**: Review your section above and your checklist
- **Task details**: Check `tasks.md` for specific task descriptions
- **Technical approach**: Check `plan.md` for architecture and decisions
- **Requirements**: Check `spec.md` for user stories and acceptance criteria
- **Project principles**: Check `.specify/memory/constitution.md`

**Let's build VPA! 🚀**
