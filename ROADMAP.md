# VPA Project Roadmap - Honest Assessment

## ✅ What's Actually Done (Playground MVP)

### Core Functionality
- ✅ **Draft Generation**: k-sampling via Ollama with temperature variation
- ✅ **Basic Verifier**: Heuristic checks (length, completeness, coherence, format)
- ✅ **Tiny Eval**: 3-question QA set, 2-question code set with basic scoring
- ✅ **CLI**: Single question mode and eval mode
- ✅ **Scripts**: `run_mvp.sh` and `run_eval.sh` for easy execution
- ✅ **Ollama Client**: REST API wrapper with error handling and logging
- ✅ **Smoke Tests**: `test_ollama.py` validates client functionality

### Infrastructure
- ✅ **Error Handling**: Logging, empty response guards, timeout handling
- ✅ **Packaging**: `pyproject.toml`, `python -m vpa` support via `__main__.py`
- ✅ **CI**: GitHub Actions workflow (Python 3.11/3.12, import tests, syntax checks)
- ✅ **Documentation**: README and status.md aligned with actual code

### What This Means
You can:
- Generate multiple answers to questions using local Ollama
- Score them with simple heuristics
- Pick the best one
- Run tiny evaluations
- See it all work end-to-end locally

---

## ❌ What's NOT Done (Full VPA System)

### Missing Core Modules

#### 1. **Plan Module** (Not Started)
- [ ] Planner that proposes self-edit strategies
- [ ] Rejection sampling over action grid
- [ ] Adaptive k-selection based on verifier feedback
- [ ] Tool selection logic
- [ ] LoRA hyperparameter tuning

#### 2. **Apply Module** (Not Started)
- [ ] LoRA adapter training infrastructure
- [ ] SFT (Supervised Fine-Tuning) on verified corrections
- [ ] DPO (Direct Preference Optimization) option
- [ ] Adapter storage and versioning
- [ ] Training data construction from verifier feedback

#### 3. **Gate Module** (Not Started)
- [ ] Regression test suite (stability set)
- [ ] Performance delta tracking
- [ ] Adapter acceptance/rejection logic
- [ ] Anti-forgetting mechanisms (KL regularization, replay)
- [ ] Quarantine failed adapters

#### 4. **Routing Module** (Not Started)
- [ ] Domain-based adapter selection
- [ ] Adapter merging strategies
- [ ] Multi-adapter composition
- [ ] Performance tracking per domain

### Missing Verifiers

#### Advanced Verification (Not Implemented)
- [ ] **Factual Verifiers**:
  - [ ] Citation/evidence overlap checker
  - [ ] Contradiction detection model
  - [ ] Knowledge base consistency checks

- [ ] **Code Verifiers**:
  - [ ] Unit test execution (beyond basic heuristics)
  - [ ] Static analysis integration
  - [ ] Test case generation

- [ ] **Math Verifiers**:
  - [ ] Step-by-step validation
  - [ ] Symbolic math checking
  - [ ] Solution verification

- [ ] **Calibration**:
  - [ ] Confidence estimation
  - [ ] Abstention mechanisms
  - [ ] Brier score / ECE computation

### Missing Datasets & Configs

#### Real Datasets (Not Integrated)
- [ ] **Factual QA**: FEVER, HotpotQA, NQ-Open
- [ ] **Coding**: HumanEval, HumanEval+, MBPP
- [ ] **Math**: GSM8K, MATH subset
- [ ] Dataset loaders and processors
- [ ] Train/val/test splits

#### Configuration System (Not Built)
- [ ] `configs/base.yaml` - Model and LoRA hyperparameters
- [ ] `configs/datasets.yaml` - Dataset paths and preprocessing
- [ ] `configs/planner_grid.yaml` - Action space definition
- [ ] `configs/verifiers.yaml` - Verifier ensemble config

### Missing Experiments & Evaluation

#### Baselines (Not Run)
- [ ] Base model performance
- [ ] Best-of-N sampling
- [ ] Self-Refine comparison
- [ ] Inner-loop RL comparison

#### Ablation Studies (Not Done)
- [ ] Remove individual verifiers
- [ ] Random vs. learned planner
- [ ] No gate vs. with gate
- [ ] Adapter routing strategies

#### Metrics Collection (Minimal)
- [ ] Comprehensive accuracy tracking (EM, F1, pass@k)
- [ ] Hallucination rate measurement
- [ ] Cost analysis (tokens, time, compute)
- [ ] Calibration metrics (Brier, ECE)
- [ ] Forgetting metrics

### Missing Publication Materials
- [ ] Experiment tracking system
- [ ] Result visualization (plots, tables)
- [ ] Reproducibility configs (seeds, versions)
- [ ] Paper draft
- [ ] Benchmark comparison tables

---

## 🎯 Recommended Next Steps

### Option A: Complete the Playground (Short-term Polish)
**Goal**: Make the current Draft→Verify→Eval playground production-ready

1. **Better Test Coverage** (1-2 days)
   - [ ] Add unit tests for generator, verifier, scorer
   - [ ] Mock Ollama for CI testing
   - [ ] Integration tests for full pipeline
   - [ ] Add pytest configuration

2. **Enhanced Eval** (2-3 days)
   - [ ] Expand QA/code test sets (10-20 questions each)
   - [ ] Add metrics tracking (accuracy, avg score)
   - [ ] Results logging/export to JSON/CSV
   - [ ] Comparison mode (different models/k values)

3. **Documentation** (1 day)
   - [ ] API documentation (docstrings → Sphinx)
   - [ ] Usage examples beyond smoke tests
   - [ ] Troubleshooting guide
   - [ ] Architecture diagram

4. **Tool Integration** (2-3 days)
   - [ ] Add retrieval tool (simple web search/RAG)
   - [ ] Add calculator/Python REPL tool
   - [ ] Tool selection in draft generation

**Deliverable**: Solid playground for LLM answer generation and verification

---

### Option B: Build Toward Full VPA (Research Path)
**Goal**: Implement Plan→Apply→Gate loop for actual model improvement

#### Phase 1: Real Verifiers (1-2 weeks)
1. **Factual Verification**
   - [ ] Citation overlap checker
   - [ ] Simple contradiction detection
   - [ ] Integrate with small factual dataset (100 examples)

2. **Code Verification**
   - [ ] Unit test execution sandbox
   - [ ] Test on MBPP subset (50 problems)

3. **Composite Scoring**
   - [ ] Weighted verifier ensemble
   - [ ] Calibration scoring

#### Phase 2: Plan Module (1 week)
1. **Simple Planner**
   - [ ] Grid search over {k ∈ [1,5], temp ∈ [0.6, 0.9]}
   - [ ] Pick best based on verifier feedback
   - [ ] Log planner decisions

2. **Integration**
   - [ ] Wire planner into main loop
   - [ ] Show adaptive k-selection working

#### Phase 3: Apply Module (2 weeks)
1. **LoRA Training**
   - [ ] Install PEFT/transformers
   - [ ] Create training pairs from verifier feedback
   - [ ] Train small LoRA (rank 8-16)
   - [ ] Save/load adapters

2. **Basic Gate**
   - [ ] Define stability test set (50 examples)
   - [ ] Accept/reject based on delta threshold
   - [ ] Show one successful persistent improvement

#### Phase 4: Experiments (2-3 weeks)
1. **Baseline Runs**
   - [ ] Base model on HotpotQA/MBPP subsets
   - [ ] Best-of-N comparison
   - [ ] Collect metrics

2. **VPA Runs**
   - [ ] Full loop on same subsets
   - [ ] Track improvements per iteration
   - [ ] Measure forgetting

3. **Analysis**
   - [ ] Generate plots
   - [ ] Ablation studies
   - [ ] Cost analysis

**Deliverable**: Working VPA system demonstrating persistent improvement

---

### Option C: Hybrid Approach (Recommended)
**Goal**: Polish playground while building toward key research questions

**Week 1-2: Strengthen Foundation**
- Improve test coverage
- Expand eval sets
- Add one real verifier (code execution)

**Week 3-4: First VPA Loop**
- Implement simple planner
- Add basic LoRA training
- Show one sticky improvement

**Week 5-6: Scale Up**
- Add real dataset (MBPP subset)
- Implement gate
- Run baseline comparisons

**Week 7-8: Experiments & Polish**
- Ablations
- Documentation
- Results visualization

---

## 📊 Current vs. Target Scope

| Component | Current State | Full VPA Target | Gap |
|-----------|--------------|----------------|-----|
| Draft | ✅ k-sampling | ✅ + tools | Tool integration |
| Verify | ✅ Heuristics | ❌ Factual/Code/Math | Real verifiers |
| Plan | ❌ None | ❌ Adaptive planner | Full module |
| Apply | ❌ None | ❌ LoRA training | Full module |
| Gate | ❌ None | ❌ Regression tests | Full module |
| Eval | ✅ Tiny sets | ❌ Real benchmarks | Real datasets |
| Experiments | ❌ None | ❌ Baselines/ablations | All experiments |

**Current Progress**: ~20% of full VPA system
**Working Prototype**: ✅ Draft→Verify→Eval loop functional
**Research-ready**: ❌ Needs Plan→Apply→Gate

---

## 🚦 Decision Point

**Question for you**: Which path do you want to take?

A. **Polish the playground** - Make it a great tool for LLM answer generation/verification
B. **Build full VPA** - Research path toward the paper/publication
C. **Hybrid** - Strengthen playground while building core VPA components

Let me know and I'll create a detailed task breakdown for the next phase!
