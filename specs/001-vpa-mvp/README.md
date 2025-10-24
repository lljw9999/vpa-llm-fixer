# VPA MVP Feature Documentation

**Feature Branch**: `001-vpa-mvp`
**Created**: 2025-10-24
**Status**: Planning Complete, Ready for Implementation

---

## 📚 Document Index

This directory contains all planning documents for the VPA (Verifier → Plan → Apply) MVP implementation.

### Core Documents (Read in Order)

1. **[spec.md](./spec.md)** - Feature Specification
   - 6 user stories with priorities (P1-P3)
   - Acceptance criteria and test scenarios
   - Functional requirements (FR-001 to FR-015)
   - Success criteria (SC-001 to SC-010)
   - Research questions (RQ1-RQ4)

2. **[plan.md](./plan.md)** - Implementation Plan
   - Technical context (Python 3.11, PyTorch, Transformers)
   - Constitution compliance check
   - Complete project structure
   - Phase 0-1 detailed workflow
   - 3-person team assignment strategy

3. **[tasks.md](./tasks.md)** - Task Breakdown
   - 183 tasks organized by user story and phase
   - Clear task ownership per person
   - Parallel execution opportunities marked with [P]
   - Tasks organized across 15 phases (setup → paper prep)
   - Timeline: 8 weeks total (MVP in 2 weeks)

4. **[TEAM_ASSIGNMENTS.md](./TEAM_ASSIGNMENTS.md)** - Team Guide
   - Detailed responsibilities for each person
   - Day 1 quick start guide
   - Weekly schedules and milestones
   - Communication protocols
   - Success criteria per person

### Checklists (Quality Assurance)

5. **[checklists/person1-draft-verify.md](./checklists/person1-draft-verify.md)**
   - 54 quality checks for Draft & Verify modules
   - Requirements completeness, implementation quality, testing coverage
   - Constitution compliance, documentation, integration readiness

6. **[checklists/person2-plan-apply.md](./checklists/person2-plan-apply.md)**
   - 76 quality checks for Plan & Apply modules
   - Planner logic, LoRA training stability, adapter routing
   - Training quality, testing coverage, experiment preparation

7. **[checklists/person3-eval-gate-cli.md](./checklists/person3-eval-gate-cli.md)**
   - 116 quality checks for Eval, Gate, CLI modules
   - Metric correctness, gate reliability, CLI usability
   - Testing infrastructure, CI/CD, reproducibility

### Supporting Documents (To Be Created)

8. **research.md** (Phase 0 output)
   - Verifier approaches research
   - LoRA best practices research
   - Evaluation metrics research
   - Tool integration patterns
   - Gate design research

9. **data-model.md** (Phase 1 output)
   - Draft, VerifierScore, Plan entities
   - LoRAAdapter, GateResult entities
   - Dataset, ExperimentRun entities

10. **contracts/** (Phase 1 output)
    - `verifier_api.yaml` - Verifier interface spec
    - `planner_api.yaml` - Planner interface spec

11. **quickstart.md** (Phase 1 output)
    - 5 quickstart scenarios
    - Demo commands and expected outputs

---

## 🚀 Quick Start for Team

### For Everyone (Day 1)

1. Read the **Core Documents** above in order (1-4)
2. Read **your checklist** (#5, #6, or #7 depending on your role)
3. Set up development environment
4. Complete Phase 1 setup tasks (T001-T015) together

### For Person 1: Draft & Verify Lead

**Your Mission**: Own candidate generation and verification quality

**Read**:
- spec.md User Stories 1-2 (Draft & Verify)
- plan.md "Person 1" section
- tasks.md Phase 3-4 (your tasks)
- checklists/person1-draft-verify.md

**Week 1 Focus**: Research verifier approaches, implement draft generation
**Week 2 Focus**: Implement verifier ensemble, generate training data

### For Person 2: Plan & Apply Lead

**Your Mission**: Own planner and LoRA adapter training

**Read**:
- spec.md User Stories 3-4, 6 (Plan, Apply, Routing)
- plan.md "Person 2" section
- tasks.md Phase 5-6, 9 (your tasks)
- checklists/person2-plan-apply.md

**Week 1 Focus**: Research LoRA best practices, design planner
**Week 2-3 Focus**: Implement planner and LoRA training

### For Person 3: Eval, Gate & CLI Lead

**Your Mission**: Own quality control, metrics, and user experience

**Read**:
- spec.md User Story 5 (Gate) and all Success Criteria
- plan.md "Person 3" section
- tasks.md Phase 2, 7-8, 10-15 (your tasks)
- checklists/person3-eval-gate-cli.md

**Week 1 Focus**: Research metrics and gate design, set up infrastructure
**Week 2-4 Focus**: Implement evaluation, gate, and CLI
**Week 5-8 Focus**: Run all experiments, generate results

---

## 📊 Project Statistics

### Scope

- **User Stories**: 6 (3 P1, 2 P2, 1 P3)
- **Functional Requirements**: 15
- **Success Criteria**: 10
- **Research Questions**: 4
- **Total Tasks**: 183
- **Total Quality Checks**: 246 (54 + 76 + 116)

### Team Distribution

- **Person 1 (Draft/Verify)**: ~50 tasks, 54 quality checks
- **Person 2 (Plan/Apply)**: ~50 tasks, 76 quality checks
- **Person 3 (Eval/Gate/CLI)**: ~60 tasks, 116 quality checks
- **Shared Tasks**: ~23 tasks

### Timeline

- **Week 1-2**: MVP (Phases 1-7, ~100 tasks)
  - Can run one example through full pipeline
  - Draft → Verify → Plan → Train → Gate works

- **Week 3-5**: Full System (Phases 8-11, ~50 tasks)
  - All 3 datasets working
  - Complete testing infrastructure
  - Integration complete

- **Week 6-8**: Experiments & Paper (Phases 12-15, ~33 tasks)
  - Baseline and VPA experiments
  - Ablation studies
  - Publication-ready results

### Milestones

- ✅ **Week 2**: MVP Demo (one example end-to-end)
- ✅ **Week 5**: Full System (all datasets, all features)
- ✅ **Week 6**: Baseline Results (initial experiments complete)
- ✅ **Week 8**: Publication Ready (reproducible, polished)

---

## 🎯 Success Criteria Summary

### Technical Success (MVP - Week 2)

- [ ] Draft generation: 5 candidates in <10s ✓
- [ ] Verification: ensemble scores in <5s ✓
- [ ] LoRA training: converges in <100 steps ✓
- [ ] Gate: evaluates in <5min ✓
- [ ] Full pipeline works on 10 examples ✓

### Research Success (Week 6-8)

- [ ] VPA improves EM on HotpotQA by ≥5 points vs baseline
- [ ] VPA improves pass@1 on MBPP by ≥8 points vs baseline
- [ ] VPA reduces hallucination rate by ≥15% on FEVER
- [ ] Adapter improvements persist (no forgetting after 3 merges)
- [ ] VPA uses <1/10th compute vs RL baseline

### Publication Success (Week 8)

- [ ] All experiments reproducible with documented seeds
- [ ] All 4 research questions answered (RQ1-RQ4)
- [ ] Publication-quality plots generated
- [ ] External researcher can reproduce results
- [ ] GitHub release with reproducibility package

---

## 🔍 Constitution Alignment

This feature implementation fully aligns with the VPA constitution:

### ✅ Principle I: Research-First Development
- Phase 0 includes comprehensive research on all technical unknowns
- All decisions documented in research.md with rationale

### ✅ Principle II: Verification-Centric Architecture
- Verifier ensemble is core component (Person 1's primary focus)
- All verifiers independently testable with interpretable diagnostics

### ✅ Principle III: Gated Adapter Updates (NON-NEGOTIABLE)
- Gate module explicitly designed and owned by Person 3
- Frozen stability set, acceptance criteria, quarantine logic all specified

### ✅ Principle IV: Reproducibility & Experimentation Discipline
- All experiments tracked with full metadata (ExperimentRun entity)
- Multiple seeds, versioned configs, documented hyperparameters

### ✅ Principle V: Minimal LoRA Footprint
- Rank ≤16 enforced in plan and tests
- Domain-specific adapters with routing

### ✅ Principle VI: Dataset & Metric Transparency
- 3 datasets mapped to RQ1-RQ4
- Standard metrics (EM/F1, pass@k, ECE, Brier)

---

## 📞 Need Help?

### Unclear About Requirements?
→ Read `spec.md` for user stories and acceptance criteria

### Unclear About Technical Approach?
→ Read `plan.md` for architecture and design decisions

### Unclear About Your Tasks?
→ Read `tasks.md` for step-by-step breakdown

### Unclear About Quality Standards?
→ Read your checklist in `checklists/`

### Unclear About Team Coordination?
→ Read `TEAM_ASSIGNMENTS.md` for communication protocols

### Unclear About Project Principles?
→ Read `.specify/memory/constitution.md` in project root

---

## 🎉 Ready to Start!

All planning is complete. The team has:

✅ Clear specification with 6 user stories
✅ Detailed implementation plan with full architecture
✅ 183 tasks organized by person and phase
✅ 246 quality checks across 3 checklists
✅ Team assignments with clear responsibilities
✅ 8-week timeline with milestones

**Next Step**: Create feature branch and start Phase 1 setup tasks (T001-T015)

```bash
git checkout -b 001-vpa-mvp
# Begin implementation following tasks.md
```

Good luck building VPA! 🚀
