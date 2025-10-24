# Feature Specification: VPA (Verifier → Plan → Apply) MVP

**Feature Branch**: `001-vpa-mvp`
**Created**: 2025-10-24
**Status**: Draft
**Input**: VPA is a lightweight framework for improving the precision and reliability of large language models (LLMs) without resorting to unstable reinforcement learning. It wraps a base LLM with a Verifier → Plan → Apply loop.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Draft Generation with Tool Support (Priority: P1)

As a researcher, I want to generate multiple candidate answers from a base LLM using different sampling strategies and optional tools (retrieval, Python execution), so that I can explore the solution space and have diverse candidates for verification.

**Why this priority**: This is the foundation of the entire VPA pipeline. Without quality draft generation, there are no candidates to verify and improve.

**Independent Test**: Can generate k=5 candidates for a HotpotQA question in <10 seconds, with tool calls logged and candidates properly formatted.

**Acceptance Scenarios**:

1. **Given** a factual question from HotpotQA, **When** I request k=5 drafts with retrieval enabled, **Then** system returns 5 diverse candidate answers with retrieval context
2. **Given** a coding problem from MBPP, **When** I request k=3 drafts with Python execution enabled, **Then** system returns 3 candidate solutions with execution results
3. **Given** a math problem from GSM8K, **When** I request k=5 drafts with calculator tool, **Then** system returns 5 candidate solutions with calculation traces

---

### User Story 2 - Verifier Ensemble Scoring (Priority: P1)

As a researcher, I want to score all candidate answers using multiple verifier channels (factual, formal, style), so that I can identify high-quality candidates and diagnose specific failure modes.

**Why this priority**: Verification is the core innovation of VPA. Without reliable verifiers, the entire approach fails.

**Independent Test**: Can verify 5 candidates in <5 seconds, producing interpretable scores (0-1 range) for each verifier channel with diagnostic messages.

**Acceptance Scenarios**:

1. **Given** 5 candidate answers to a factual question, **When** I run the factual verifier, **Then** each candidate receives citation overlap score, contradiction score, and diagnostic message
2. **Given** 3 candidate code solutions, **When** I run the formal verifier, **Then** each candidate receives unit test pass rate, syntax validity, and diagnostic message
3. **Given** 5 candidate answers, **When** I run the style verifier, **Then** each candidate receives formatting score, safety score, and diagnostic message

---

### User Story 3 - Planner Proposing Self-Edits (Priority: P2)

As a researcher, I want the system to analyze verifier diagnostics and propose self-edit plans (adjust k, select tools, choose LoRA hyperparameters), so that the system can autonomously improve on identified weaknesses.

**Why this priority**: The planner enables autonomous improvement. It's lower priority than draft+verify because those must work first.

**Independent Test**: Given verifier scores showing factual errors, planner suggests increasing k or enabling retrieval tool.

**Acceptance Scenarios**:

1. **Given** verifier diagnostics showing low citation overlap, **When** planner analyzes results, **Then** planner proposes enabling retrieval tool and increasing k to 7
2. **Given** verifier diagnostics showing code syntax errors, **When** planner analyzes results, **Then** planner proposes adjusting temperature and enabling Python execution
3. **Given** verifier diagnostics showing acceptable quality, **When** planner analyzes results, **Then** planner proposes LoRA training parameters (rank, lr, epochs)

---

### User Story 4 - LoRA Adapter Training (Priority: P2)

As a researcher, I want to train small LoRA adapters on verified corrections, so that improvements persist across sessions without catastrophic forgetting.

**Why this priority**: This is the "Apply" step that makes improvements sticky. It depends on having quality verified corrections first.

**Independent Test**: Train a rank-8 LoRA adapter on 100 verified corrections, converges in <100 steps, checkpoint saved successfully.

**Acceptance Scenarios**:

1. **Given** 100 verified (input, best_answer) pairs from HotpotQA, **When** I train a LoRA adapter with rank=8, lr=1e-4, **Then** adapter converges in <100 steps and checkpoint is saved
2. **Given** 50 verified coding corrections from MBPP, **When** I train a LoRA adapter with rank=16, **Then** adapter shows improving loss curve and saves without errors
3. **Given** verified corrections across multiple domains, **When** I train domain-specific adapters, **Then** each adapter checkpoint is tagged with domain label

---

### User Story 5 - Regression Gate Validation (Priority: P1)

As a researcher, I want every trained adapter to pass through a regression gate with frozen stability tests, so that only improvements that don't cause regressions are merged.

**Why this priority**: This is NON-NEGOTIABLE per constitution. The gate prevents catastrophic forgetting and ensures quality control.

**Independent Test**: Load adapter, run gate suite on 200 frozen test examples, produce pass/fail decision with performance metrics in <5 minutes.

**Acceptance Scenarios**:

1. **Given** a newly trained adapter for HotpotQA, **When** I run the regression gate, **Then** gate evaluates on frozen stability set and reports EM/F1 delta
2. **Given** an adapter that improves EM by +5 points with no regressions, **When** gate evaluates it, **Then** gate marks adapter as PASS and allows merge
3. **Given** an adapter that improves one metric but regresses another by >3 points, **When** gate evaluates it, **Then** gate marks adapter as FAIL and quarantines it
4. **Given** gate results, **When** viewing output, **Then** I see detailed metrics: old performance, new performance, delta, pass/fail status

---

### User Story 6 - Adapter Routing by Domain (Priority: P3)

As a researcher, I want adapters to be routed based on domain similarity (law, math, code), so that the most relevant improvements are applied to each query.

**Why this priority**: This is an optimization that can come after basic adapter training works. Nice to have but not MVP-critical.

**Independent Test**: Given a coding query, router selects "code" adapter with >0.8 confidence based on similarity metrics.

**Acceptance Scenarios**:

1. **Given** a query about legal documents, **When** router evaluates available adapters, **Then** router selects "law" adapter with confidence score
2. **Given** a math word problem, **When** router evaluates available adapters, **Then** router selects "math" adapter over "code" adapter
3. **Given** a query not matching any domain, **When** router evaluates, **Then** router falls back to base model without adapter

---

### Edge Cases

- What happens when draft generation produces k<requested candidates (e.g., model refuses to answer)?
- How does system handle verifier failures (e.g., retrieval service down, unit test timeout)?
- What happens when all k candidates score below threshold (no good answer)?
- How does gate handle adapters that slightly improve one domain but slightly hurt another?
- What happens when LoRA training diverges or produces NaN losses?
- How does router handle queries that span multiple domains (e.g., "write code to solve this math problem")?
- What happens when gate stability set becomes stale or no longer representative?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST generate k candidate answers (1 ≤ k ≤ 10) from base LLM with configurable temperature and top_p
- **FR-002**: System MUST support optional tool usage: retrieval (RAG), Python execution (code interpreter), calculator
- **FR-003**: System MUST implement factual verifier checking citation overlap, contradiction detection, and evidence support
- **FR-004**: System MUST implement formal verifier checking unit tests (code), schema validation (structured output), and syntax
- **FR-005**: System MUST implement style verifier checking formatting, safety, and output length constraints
- **FR-006**: System MUST composite verifier scores into single quality score with interpretable diagnostics
- **FR-007**: System MUST implement planner using rejection sampling over action grid (k values, tool selections, LoRA hyperparams)
- **FR-008**: System MUST train LoRA adapters using supervised fine-tuning (SFT) or DPO on verified corrections
- **FR-009**: System MUST implement regression gate evaluating adapters on frozen stability set
- **FR-010**: Gate MUST accept adapters with ≥3 EM points improvement on QA OR ≥5 pass@1 points on coding benchmarks
- **FR-011**: Gate MUST reject and quarantine adapters that cause regressions >3 points on any metric
- **FR-012**: System MUST implement adapter router using domain classification or embedding similarity
- **FR-013**: System MUST log all experiments with: model checkpoint, LoRA config, verifier config, training data hash, random seed
- **FR-014**: System MUST support multiple datasets: FEVER, HotpotQA, NQ-Open (QA), HumanEval/MBPP (code), GSM8K (math)
- **FR-015**: System MUST compute standard metrics: EM/F1 (QA), pass@k (code), accuracy (math), Brier score (calibration), ECE

### Key Entities

- **Draft**: Generated candidate answer with metadata (temperature, tool usage, tokens)
- **VerifierScore**: Multi-channel score (factual, formal, style) with diagnostic message for each channel
- **Plan**: Self-edit proposal containing k adjustment, tool selections, and LoRA hyperparameters
- **LoRAAdapter**: Fine-tuned adapter with metadata (rank, domain, training data, checkpoint path)
- **GateResult**: Pass/fail decision with performance metrics (old/new/delta) and timestamp
- **Dataset**: Question-answer pairs with metadata (domain, difficulty, gold answer, evidence)
- **ExperimentRun**: Complete run metadata linking dataset, model, adapters, verifier configs, and results

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Draft generation produces k=5 candidates in <10 seconds on 7B-13B models (tested on HotpotQA, MBPP, GSM8K)
- **SC-002**: Verifier ensemble scores 5 candidates in <5 seconds with all three channels (factual, formal, style)
- **SC-003**: LoRA training converges in <100 steps for rank ≤ 16 on <500 training examples
- **SC-004**: Regression gate evaluates adapter on 200 frozen examples in <5 minutes
- **SC-005**: VPA improves EM on HotpotQA by ≥5 points vs. baseline (base model + best-of-N sampling)
- **SC-006**: VPA improves pass@1 on MBPP by ≥8 points vs. baseline
- **SC-007**: VPA reduces hallucination rate by ≥15% on FEVER (measured by contradiction detection)
- **SC-008**: Adapter improvements persist after gate merge (no forgetting on stability set after 3 adapter merges)
- **SC-009**: System achieves better Brier score and ECE than baseline (improved calibration)
- **SC-010**: VPA uses <1/10th the compute of comparable RL fine-tuning baseline (measured in GPU-hours)

### Research Questions Validated

- **RQ1**: Does VPA improve precision (EM, F1, pass@k, hallucination↓) vs. best-of-N and Self-Refine?
- **RQ2**: Can we persist fixes (no context) without forgetting across multiple adapter merges?
- **RQ3**: What's the cost–performance frontier compared with inner-loop RL (PPO/DPO)?
- **RQ4**: Which verifier signals matter most (factual vs. formal vs. style) via ablation study?
