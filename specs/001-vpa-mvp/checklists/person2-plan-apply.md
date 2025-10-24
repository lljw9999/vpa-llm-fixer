# Person 2: Plan & Apply Lead - Quality Checklist

**Purpose**: Quality checklist for Planner, LoRA Training, and Adapter Routing implementation
**Created**: 2025-10-24
**Focus Areas**: Requirements completeness, adapter quality, training stability, routing accuracy

## Requirement Completeness

- [ ] CHK001 - Are planner action grid requirements (k values, tool selections, LoRA params) clearly specified? [Completeness, Spec §FR-007]
- [ ] CHK002 - Are planner diagnostic analysis requirements explicitly defined? [Clarity, Spec §US3]
- [ ] CHK003 - Are LoRA training requirements (SFT, rank, learning rate, epochs) fully documented? [Completeness, Spec §FR-008]
- [ ] CHK004 - Are adapter checkpointing requirements (metadata, versioning, domain tags) specified? [Completeness, Spec §US4]
- [ ] CHK005 - Are adapter routing requirements (similarity metrics, confidence thresholds) clearly defined? [Clarity, Spec §US6]
- [ ] CHK006 - Is the adapter composition/merging strategy documented? [Gap, Spec §US6]
- [ ] CHK007 - Are LoRA training convergence criteria (steps, loss threshold) measurable? [Measurability, Spec §SC-003]
- [ ] CHK008 - Are edge cases for planner documented (all scores low, conflicting diagnostics)? [Coverage, Edge Cases]
- [ ] CHK009 - Are edge cases for training documented (divergence, NaN losses, OOM errors)? [Coverage, Edge Cases]
- [ ] CHK010 - Are edge cases for routing documented (multi-domain queries, no matching adapter)? [Coverage, Edge Cases]

## Implementation Quality - Planner

- [ ] CHK011 - Does Planner correctly parse verifier diagnostics from all three channels? [Spec §US3]
- [ ] CHK012 - Does rejection sampling implementation explore action grid efficiently? [Spec §FR-007]
- [ ] CHK013 - Are k adjustment proposals sensible (increase k when quality low)? [Logic Correctness]
- [ ] CHK014 - Are tool selection proposals aligned with diagnostic types (retrieval for factual errors)? [Logic Correctness]
- [ ] CHK015 - Are LoRA hyperparameter proposals reasonable (rank, lr, epochs)? [Domain Knowledge]
- [ ] CHK016 - Does Planner handle cases where no action improves quality? [Edge Case]
- [ ] CHK017 - Is planner action grid configurable via configs/planner_grid.yaml? [Configuration]

## Implementation Quality - LoRA Training

- [ ] CHK018 - Does LoRATrainer correctly integrate with HuggingFace PEFT library? [Spec §FR-008]
- [ ] CHK019 - Are training data properly formatted as (input, output) pairs? [Data Preparation]
- [ ] CHK020 - Does training loop implement proper gradient accumulation for small batches? [Training Quality]
- [ ] CHK021 - Is early stopping implemented to prevent overfitting? [Training Quality]
- [ ] CHK022 - Are loss curves logged for debugging and analysis? [Observability]
- [ ] CHK023 - Does checkpoint saving include all required metadata (rank, domain, data hash, seed)? [Spec §FR-013]
- [ ] CHK024 - Can adapters be loaded and used for inference without errors? [Functionality]
- [ ] CHK025 - Is adapter versioning implemented with domain tags (e.g., "math-v1.2")? [Versioning]
- [ ] CHK026 - Are LoRA hyperparameters (rank ≤16) enforced per constitution? [Constitution, Principle V]

## Implementation Quality - Adapter Routing

- [ ] CHK027 - Does AdapterRouter correctly classify domain from query text? [Spec §US6]
- [ ] CHK028 - Does embedding similarity routing produce reasonable confidence scores? [Spec §US6]
- [ ] CHK029 - Does router fall back to base model when no adapter matches? [Spec §FR-012]
- [ ] CHK030 - Is adapter composition/merging implemented correctly (if applicable)? [Advanced Feature]
- [ ] CHK031 - Does router handle multi-domain queries appropriately? [Edge Case]
- [ ] CHK032 - Are routing decisions logged for debugging and analysis? [Observability]

## Training Stability & Quality

- [ ] CHK033 - Do LoRA adapters converge consistently within 100 steps for rank ≤16? [Performance, Spec §SC-003]
- [ ] CHK034 - Are training losses decreasing monotonically (no divergence)? [Training Quality]
- [ ] CHK035 - Are NaN losses detected and handled gracefully? [Robustness]
- [ ] CHK036 - Do trained adapters produce coherent outputs on validation set? [Quality]
- [ ] CHK037 - Are adapters tested on held-out examples before gate submission? [Quality Control]
- [ ] CHK038 - Do adapters improve on targeted domain without catastrophic forgetting? [Core Objective]
- [ ] CHK039 - Are multiple training runs with different seeds consistent? [Reproducibility]

## Testing Coverage

- [ ] CHK040 - Are unit tests provided for Planner with various diagnostic inputs? [Testing, T067]
- [ ] CHK041 - Are contract tests provided for Planner interface compliance? [Testing, T068]
- [ ] CHK042 - Are unit tests provided for LoRATrainer with small synthetic dataset? [Testing, T079]
- [ ] CHK043 - Are unit tests provided for AdapterRouter with test queries? [Testing, T112]
- [ ] CHK044 - Are integration tests provided for adapter routing with multiple adapters? [Testing, T113]
- [ ] CHK045 - Are integration tests provided for Verify→Plan workflow? [Testing, T129]
- [ ] CHK046 - Are integration tests provided for Plan→Apply workflow? [Testing, T130]
- [ ] CHK047 - Do tests include edge cases (training divergence, router conflicts, bad diagnostics)? [Coverage]
- [ ] CHK048 - Is test coverage >80% for all modules in vpa/plan/ and vpa/apply/? [Quality Gate]

## Performance Validation

- [ ] CHK049 - Does LoRA training converge in <100 steps per requirement? [Performance, Spec §SC-003]
- [ ] CHK050 - Is training memory footprint within 40GB GPU limit for 13B model? [Resource Constraint]
- [ ] CHK051 - Does planner complete diagnostic analysis in <1 second? [Performance]
- [ ] CHK052 - Does adapter routing complete in <100ms per query? [Performance]
- [ ] CHK053 - Are performance benchmarks included in test suite? [Testing]

## Constitution Compliance

- [ ] CHK054 - Are LoRA ranks ≤16 for initial experiments per Principle V? [Constitution, Principle V]
- [ ] CHK055 - Does each adapter target specific domain per Principle V? [Constitution, Principle V]
- [ ] CHK056 - Is adapter routing using similarity metrics per Principle V? [Constitution, Principle V]
- [ ] CHK057 - Are all LoRA training configs logged with seeds per Principle IV? [Constitution, Principle IV]
- [ ] CHK058 - Is research on LoRA best practices documented in research.md? [Constitution, Principle I]
- [ ] CHK059 - Are adapter checkpoints versioned with metadata per Principle IV? [Constitution, Principle IV]

## Documentation Requirements

- [ ] CHK060 - Are all public classes and methods documented with docstrings? [Documentation]
- [ ] CHK061 - Are planner action grid configurations documented? [Documentation]
- [ ] CHK062 - Are LoRA training procedures documented with hyperparameter guidance? [Documentation]
- [ ] CHK063 - Is adapter_guide.md created with training workflow instructions? [Documentation, T176]
- [ ] CHK064 - Are adapter routing strategies explained in documentation? [Documentation]
- [ ] CHK065 - Are training failure modes and debugging tips documented? [Documentation]

## Integration Readiness

- [ ] CHK066 - Can Plan module be imported and used standalone for testing? [Integration]
- [ ] CHK067 - Can Apply module be imported and used standalone for testing? [Integration]
- [ ] CHK068 - Are Verify→Plan→Apply modules integrated in test_pipeline.py? [Integration, T129-T130]
- [ ] CHK069 - Are all required configs present in configs/ directory (base.yaml, planner_grid.yaml)? [Configuration]
- [ ] CHK070 - Can adapters be trained successfully for all three datasets? [Integration, T144-T154]
- [ ] CHK071 - Can trained adapters be loaded and routed correctly? [Integration]

## Experiment Preparation

- [ ] CHK072 - Are experiment configs created for all three datasets in configs/experiments/? [Configuration, T080]
- [ ] CHK073 - Can 100-example training runs complete without errors? [Reliability]
- [ ] CHK074 - Are adapter checkpoints saved with proper naming convention? [Organization]
- [ ] CHK075 - Can multi-adapter routing experiments be set up easily? [Extensibility, T164]
- [ ] CHK076 - Are hyperparameter sweep configs prepared for ablations? [Experiment Planning, T165]
