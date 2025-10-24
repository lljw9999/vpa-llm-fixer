# Implementation Plan: VPA MVP

**Branch**: `001-vpa-mvp` | **Date**: 2025-10-24 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-vpa-mvp/spec.md`

## Summary

VPA (Verifier → Plan → Apply) is a lightweight framework that improves LLM precision through a verify-then-learn loop. The MVP will implement the core pipeline: (1) Draft generation with k-sampling and tool support, (2) Verifier ensemble with factual/formal/style channels, (3) Planner proposing self-edits, (4) LoRA adapter training on verified corrections, and (5) Regression gate preventing catastrophic forgetting. Initial evaluation on HotpotQA, MBPP, and GSM8K to validate RQ1-RQ4.

## Technical Context

**Language/Version**: Python 3.11
**Primary Dependencies**:
- PyTorch 2.1+ (model inference and training)
- Transformers 4.36+ (HuggingFace models and LoRA via PEFT)
- Datasets (HuggingFace datasets library)
- LangChain or LlamaIndex (tool integration: retrieval, code execution)
- OpenAI API (optional for baseline comparisons)
- WandB or TensorBoard (experiment tracking)

**Storage**:
- Local filesystem for model checkpoints and adapter weights
- SQLite or JSON for experiment logs and results
- HuggingFace Hub for dataset downloads

**Testing**:
- pytest (unit and integration tests)
- pytest-cov (coverage reporting)
- Contract tests for verifier interfaces

**Target Platform**: Linux server with GPU (CUDA 12.0+), tested on single A100/V100 40GB

**Project Type**: Single Python project with CLI interface

**Performance Goals**:
- Draft generation: 5 candidates in <10s on 7B-13B models
- Verification: <5s for ensemble scoring of 5 candidates
- LoRA training: convergence in <100 steps for rank ≤16
- Gate evaluation: <5min on 200 frozen examples

**Constraints**:
- Memory: Must fit 13B model + rank-16 adapter in 40GB GPU
- Latency: Interactive research workflow (no multi-hour waits per experiment)
- Cost: <1/10th compute vs. RL baselines (measured in GPU-hours)

**Scale/Scope**:
- Support 3 datasets (HotpotQA, MBPP, GSM8K) with ~1000 examples each for MVP
- Handle 10-50 adapter checkpoints per domain
- Log 100+ experiment runs for paper

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ I. Research-First Development
- **Status**: PASS
- **Evidence**: Phase 0 includes comprehensive research tasks for verifier approaches, LoRA best practices, evaluation metrics, and tool integration patterns

### ✅ II. Verification-Centric Architecture
- **Status**: PASS
- **Evidence**: Verifier ensemble is central to design. Each verifier channel (factual/formal/style) has clear interface, independent testing, and diagnostic output

### ✅ III. Gated Adapter Updates (NON-NEGOTIABLE)
- **Status**: PASS
- **Evidence**: Gate module explicitly included with frozen stability set, acceptance criteria (≥3 EM or ≥5 pass@1), and quarantine logic for failed adapters

### ✅ IV. Reproducibility & Experimentation Discipline
- **Status**: PASS
- **Evidence**: ExperimentRun entity tracks all metadata (seeds, configs, data hashes). WandB integration for logging. All configs in YAML.

### ✅ V. Minimal LoRA Footprint
- **Status**: PASS
- **Evidence**: Plan specifies rank ≤16 for initial experiments. Adapter routing by domain included. Interference monitoring in evaluation.

### ✅ VI. Dataset & Metric Transparency
- **Status**: PASS
- **Evidence**: Three datasets mapped to RQ1-RQ4. Standard metrics (EM/F1, pass@k, ECE, Brier). Data splits prevent leakage.

### Summary
All constitution principles are satisfied. No complexity violations. Proceeding to Phase 0 research.

## Project Structure

### Documentation (this feature)

```text
specs/001-vpa-mvp/
├── spec.md              # Feature specification (DONE)
├── plan.md              # This file (IN PROGRESS)
├── research.md          # Phase 0 output (TODO)
├── data-model.md        # Phase 1 output (TODO)
├── quickstart.md        # Phase 1 output (TODO)
├── contracts/           # Phase 1 output (TODO)
│   ├── verifier_api.yaml
│   └── planner_api.yaml
├── checklists/          # Phase 2 output (TODO)
│   ├── person1-draft-verify.md
│   ├── person2-plan-apply.md
│   └── person3-eval-gate.md
└── tasks.md             # Phase 2 output (TODO)
```

### Source Code (repository root)

```text
vpa/
├── draft/
│   ├── __init__.py
│   ├── generator.py          # k-sampling logic
│   ├── tools.py              # Retrieval, Python exec, calculator wrappers
│   └── config.py             # Draft generation config
│
├── verify/
│   ├── __init__.py
│   ├── base.py               # Abstract verifier interface
│   ├── factual.py            # Citation, contradiction, evidence checks
│   ├── formal.py             # Unit tests, schema validation, syntax
│   ├── style.py              # Formatting, safety, length checks
│   └── ensemble.py           # Composite scoring and diagnostics
│
├── plan/
│   ├── __init__.py
│   ├── planner.py            # Rejection sampling planner
│   ├── action_grid.py        # Search space definition (k, tools, LoRA params)
│   └── config.py             # Planner config
│
├── apply/
│   ├── __init__.py
│   ├── lora_trainer.py       # LoRA SFT/DPO training
│   ├── gate.py               # Regression gate logic
│   ├── router.py             # Adapter routing by domain
│   └── config.py             # Training and gate configs
│
├── data/
│   ├── __init__.py
│   ├── loaders.py            # HuggingFace dataset loaders
│   ├── builders.py           # Build (input, output, evidence) tuples
│   └── splits.py             # Train/val/test/stability splits
│
├── eval/
│   ├── __init__.py
│   ├── metrics.py            # EM, F1, pass@k, accuracy, Brier, ECE
│   ├── qa_eval.py            # QA evaluation harness
│   ├── code_eval.py          # Coding evaluation harness
│   ├── math_eval.py          # Math evaluation harness
│   └── experiment.py         # ExperimentRun tracker
│
├── cli/
│   ├── __init__.py
│   ├── main.py               # CLI entry point
│   ├── commands/
│   │   ├── draft.py          # Run draft generation
│   │   ├── verify.py         # Run verification
│   │   ├── plan.py           # Run planner
│   │   ├── train.py          # Train adapter
│   │   ├── gate.py           # Run gate
│   │   └── eval.py           # Run evaluation
│   └── config.py             # Global CLI config
│
└── utils/
    ├── __init__.py
    ├── logging.py            # Structured logging
    ├── checkpointing.py      # Model and adapter checkpoint utils
    └── seed.py               # Reproducible random seeds

tests/
├── unit/
│   ├── test_draft.py
│   ├── test_verifiers.py
│   ├── test_planner.py
│   ├── test_lora_trainer.py
│   ├── test_gate.py
│   └── test_metrics.py
│
├── integration/
│   ├── test_pipeline.py      # End-to-end Draft→Verify→Plan→Apply
│   ├── test_tool_integration.py
│   └── test_adapter_routing.py
│
└── contract/
    ├── test_verifier_interface.py
    └── test_planner_interface.py

configs/
├── base.yaml                 # Base model, LoRA defaults
├── verifiers.yaml            # Verifier ensemble config
├── planner_grid.yaml         # Planner action space
├── datasets.yaml             # Dataset paths and splits
└── experiments/              # Experiment-specific configs
    ├── hotpotqa_baseline.yaml
    ├── mbpp_baseline.yaml
    └── gsm8k_baseline.yaml

scripts/
├── setup_env.sh              # Environment setup
├── download_models.sh        # Download base models
├── download_datasets.sh      # Download HF datasets
├── run_mvp_pipeline.sh       # Run full MVP demo
├── train_adapter.sh          # Train single adapter
└── run_experiments.sh        # Run all baseline experiments

docs/
├── architecture.md           # System architecture overview
├── verifier_guide.md         # How to add new verifiers
├── adapter_guide.md          # How to train and merge adapters
└── evaluation_guide.md       # How to run evaluations

data/                         # Git-ignored, created at runtime
├── models/                   # Downloaded model checkpoints
├── datasets/                 # Downloaded datasets
├── adapters/                 # Trained adapter checkpoints
│   ├── hotpotqa/
│   ├── mbpp/
│   └── gsm8k/
├── stability_sets/           # Frozen regression test data
└── experiments/              # Experiment outputs
    ├── run_001/
    ├── run_002/
    └── ...

.github/
└── workflows/
    ├── tests.yml             # CI: run pytest on PRs
    └── constitution_check.yml # CI: verify constitution compliance
```

**Structure Decision**: Single Python project structure chosen because VPA is a unified framework with tight coupling between components. All modules need access to shared configs and models. CLI provides entry points for each pipeline stage. Monorepo simplifies reproducibility (single environment, single requirements.txt).

## Complexity Tracking

No violations. All requirements align with constitution principles. No additional complexity beyond core VPA architecture.

## Phase 0: Research Tasks (Week 1, Days 1-2)

**Goal**: Resolve all technical unknowns and establish best practices before implementation.

### Research Tasks

1. **Verifier Approaches Research**
   - **Question**: What are best practices for factual verification (citation checking, contradiction detection)?
   - **Action**: Survey papers (FactScore, SAFE, FActScore, Citation Recall), evaluate existing libraries (NLTK, spaCy, sentence-transformers)
   - **Output**: `research.md` section documenting chosen approaches with rationale

2. **Formal Verifier Research**
   - **Question**: How to implement robust unit test execution and schema validation for code/structured output?
   - **Action**: Evaluate execution sandboxes (Docker, subprocess isolation), schema validators (Pydantic, JSON Schema), unit test frameworks
   - **Output**: `research.md` section documenting chosen tools and safety measures

3. **LoRA Best Practices Research**
   - **Question**: What rank, learning rate, and epoch settings work best for 7B-13B models on small datasets (<500 examples)?
   - **Action**: Survey LoRA papers (QLoRA, LoRA+, AdaLoRA), check HuggingFace PEFT examples, review recent fine-tuning results
   - **Output**: `research.md` section with recommended hyperparameter ranges

4. **Tool Integration Patterns Research**
   - **Question**: Should we use LangChain, LlamaIndex, or custom implementations for retrieval and code execution?
   - **Action**: Benchmark latency, evaluate API stability, check documentation quality
   - **Output**: `research.md` section with tool integration architecture decision

5. **Evaluation Metrics Research**
   - **Question**: What are standard implementations for pass@k, ECE, Brier score, and hallucination rate?
   - **Action**: Survey evaluation libraries (EleutherAI lm-evaluation-harness, HuggingFace evaluate), check metric definitions
   - **Output**: `research.md` section documenting metric implementations

6. **Gate Design Research**
   - **Question**: How should we implement the regression gate to prevent overfitting to stability set?
   - **Action**: Survey continual learning papers (EWC, PackNet, adapter merging), review test set construction
   - **Output**: `research.md` section with gate architecture and stability set construction

**Deliverable**: Complete `research.md` with all decisions documented and rationale provided.

## Phase 1: Design & Contracts (Week 1, Days 3-5)

**Prerequisites**: `research.md` complete

### Design Tasks

1. **Data Model Design** (`data-model.md`)
   - Draft entity (candidate text, metadata, tool_calls)
   - VerifierScore entity (per-channel scores, diagnostics)
   - Plan entity (k_adjustment, tool_selections, lora_params)
   - LoRAAdapter entity (checkpoint_path, rank, domain, training_metadata)
   - GateResult entity (pass/fail, metrics, timestamp)
   - Dataset entity (questions, answers, evidence, splits)
   - ExperimentRun entity (all config hashes, results)

2. **API Contracts Design** (`contracts/`)
   - `verifier_api.yaml`: Abstract verifier interface (input: list of candidates, output: list of scores with diagnostics)
   - `planner_api.yaml`: Planner interface (input: verifier scores, output: action plan)
   - Both in OpenAPI 3.0 format for potential future service decomposition

3. **Quickstart Scenarios** (`quickstart.md`)
   - Scenario 1: Run draft generation for single HotpotQA question
   - Scenario 2: Verify candidates with full ensemble
   - Scenario 3: Train small LoRA adapter on 50 examples
   - Scenario 4: Run gate evaluation on trained adapter
   - Scenario 5: Full pipeline on 10 questions (draft → verify → train → gate)

4. **Agent Context Update**
   - Run `.specify/scripts/bash/update-agent-context.sh codex` to add Python, PyTorch, Transformers to agent context

**Deliverable**: Complete `data-model.md`, `contracts/`, `quickstart.md`, updated agent context file.

## Team Assignment Strategy (3 People)

### Person 1: Draft & Verify Lead
**Modules**: `vpa/draft/`, `vpa/verify/`, `vpa/data/`
**Focus**: Candidate generation, verifier ensemble, dataset loading
**Key Responsibilities**:
- Implement k-sampling with temperature/top_p controls
- Integrate tools (retrieval, Python exec, calculator)
- Implement all three verifier channels (factual, formal, style)
- Build verifier ensemble with composite scoring
- Create dataset loaders for HotpotQA, MBPP, GSM8K

### Person 2: Plan & Apply Lead
**Modules**: `vpa/plan/`, `vpa/apply/`
**Focus**: Planner, LoRA training, adapter routing
**Key Responsibilities**:
- Implement rejection sampling planner with action grid
- Build LoRA training pipeline (SFT, optional DPO)
- Implement adapter checkpointing and versioning
- Build adapter router using domain classification
- Handle LoRA merging and composition

### Person 3: Eval & Gate Lead
**Modules**: `vpa/eval/`, `vpa/apply/gate.py`, `vpa/cli/`, `tests/`
**Focus**: Evaluation harness, regression gate, CLI, testing
**Key Responsibilities**:
- Implement all metrics (EM/F1, pass@k, accuracy, Brier, ECE)
- Build evaluation harnesses for QA, code, math
- Implement regression gate with frozen stability set
- Build CLI commands for all pipeline stages
- Write unit, integration, and contract tests
- Set up experiment tracking (WandB/TensorBoard)

## Implementation Phases (Weeks 2-8)

### Week 2: MVP Core Components
- Person 1: Draft generation + factual verifier
- Person 2: LoRA trainer skeleton + config system
- Person 3: Evaluation metrics + QA harness

### Week 3: Verifier Ensemble & Gate
- Person 1: Formal + style verifiers + ensemble
- Person 2: Planner with simple action grid
- Person 3: Regression gate + stability set construction

### Week 4: Tool Integration & Routing
- Person 1: Integrate retrieval and code execution tools
- Person 2: Adapter routing by domain
- Person 3: Code and math evaluation harnesses

### Week 5: End-to-End Pipeline & Testing
- All: Integration testing of full pipeline
- Person 3: Comprehensive unit and contract tests
- All: Run MVP demo on small dataset slices

### Week 6: Baseline Experiments
- All: Run baseline experiments (base model + best-of-N)
- All: Run VPA with single domain adapter
- Person 3: Generate initial plots and result tables

### Week 7: Ablation Studies & Advanced Experiments
- All: Verifier ablations (remove each channel)
- All: LoRA hyperparameter sweeps
- Person 2: Multi-adapter routing experiments
- Person 3: Calibration analysis (Brier, ECE)

### Week 8: Paper Prep & Reproducibility
- All: Finalize experiments with multiple seeds
- Person 3: Generate all plots for paper (Pareto curves, calibration plots)
- All: Document reproducibility (configs, seeds, instructions)
- All: Polish code, update README, prepare for release

## Next Steps

1. Review and approve this plan
2. Create branch `001-vpa-mvp`
3. Run Phase 0 research (Person 1: verifiers, Person 2: LoRA, Person 3: metrics)
4. Complete Phase 1 design documents
5. Generate `tasks.md` with detailed task breakdown per person
6. Begin Week 2 implementation

## Open Questions

1. Should we implement DPO in MVP or defer to post-MVP? (Current plan: SFT only for MVP)
2. What base model should we use for initial experiments? (Suggested: Llama-2-7B or Mistral-7B)
3. Should we implement adapter composition/merging in MVP? (Current plan: yes, simple averaging)
4. How large should frozen stability set be? (Current plan: 200 examples, 20% of training data)
