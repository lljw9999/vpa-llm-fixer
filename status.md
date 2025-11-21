# Project Status & Roadmap

Based on `GET_STARTED.md` and `Readme.md`, here is the checklist to track our progress towards the VPA (Verifier → Plan → Apply) framework.

## 🚀 Phase 1: Project Setup (Week 1)
- [ ] **Read Core Documents**
    - [ ] `Readme.md` (Project Overview)
    - [ ] `specs/001-vpa-mvp/README.md` (Feature Overview)
    - [ ] `.specify/memory/constitution.md` (Principles)
    - [ ] `specs/001-vpa-mvp/spec.md` (Requirements)
    - [ ] `specs/001-vpa-mvp/plan.md` (Architecture)
    - [ ] `specs/001-vpa-mvp/TEAM_ASSIGNMENTS.md` (Roles)
- [ ] **Environment Setup**
    - [ ] Clone repository & create branch `001-vpa-mvp`
    - [ ] Install Python 3.11 & create virtual environment
    - [ ] Install core dependencies (`torch`, `transformers`, `peft`, `datasets`, `pytest`)
- [ ] **Scaffold Project Structure**
    - [ ] Create directories: `vpa/{draft,verify,plan,apply,data,eval,cli,utils}`
    - [ ] Create directories: `tests`, `configs`, `scripts`, `docs`
    - [ ] Create `__init__.py` files
- [ ] **Initial Configuration**
    - [ ] Create `configs/datasets.yaml`
    - [ ] Create `configs/base.yaml` & `configs/planner_grid.yaml`
    - [ ] Create `configs/verifiers.yaml`

## 🛠 Phase 2: MVP Core Implementation (Week 2)
- [ ] **Core Modules**
    - [ ] Implement Draft generation (k-sampling + tools)
    - [ ] Implement Factual Verifier
    - [ ] Implement LoRA Trainer Skeleton
    - [ ] Implement Metrics & QA Harness
- [ ] **Integration & Demo**
    - [ ] Run end-to-end pipeline test
    - [ ] Demonstrate MVP (one example through full pipeline: Generate -> Verify -> Train -> Gate)

## 🧩 Phase 3: Full System (Weeks 3-5)
- [ ] **Advanced Features**
    - [ ] Wire up full datasets (HotpotQA, MBPP, GSM8K)
    - [ ] Add advanced verifiers (citation checker, contradiction model)
    - [ ] Implement Adapter Routing
    - [ ] Implement Anti-forgetting (Gate regression test)
- [ ] **Testing & Validation**
    - [ ] Full testing infrastructure
    - [ ] All 3 datasets working end-to-end

## 🔬 Phase 4: Experiments & Publication (Weeks 6-8)
- [ ] **Experiments**
    - [ ] Run baseline experiments (base model + best-of-N)
    - [ ] Run VPA experiments
    - [ ] Perform ablation studies (remove verifiers, random planner, etc.)
- [ ] **Publication**
    - [ ] Generate publication-ready results
    - [ ] Verify reproducibility (configs, seeds)
    - [ ] Finalize paper & submission
