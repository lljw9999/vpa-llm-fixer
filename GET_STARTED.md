# 🚀 VPA Project - Get Started Guide

Welcome to the VPA (Verifier → Plan → Apply) project! This guide will help your 3-person team get started quickly.

---

## ✨ What's Been Prepared for You

All planning and documentation is **complete**. You have:

### 📋 Project Setup (Ready)

✅ **Constitution** - Project principles and governance
- Location: `.specify/memory/constitution.md`
- 6 core principles (research-first, verification-centric, gated updates, reproducibility, minimal LoRA, dataset transparency)

✅ **Feature Specification** - Complete requirements
- Location: `specs/001-vpa-mvp/spec.md`
- 6 user stories with priorities and acceptance criteria
- 15 functional requirements
- 10 success criteria answering 4 research questions

✅ **Implementation Plan** - Full architecture and design
- Location: `specs/001-vpa-mvp/plan.md`
- Technical stack (Python 3.11, PyTorch, Transformers)
- Complete project structure
- Constitution compliance verification
- Team assignment strategy

✅ **Task Breakdown** - 183 tasks organized by person
- Location: `specs/001-vpa-mvp/tasks.md`
- 15 phases from setup to publication
- Clear ownership and dependencies
- Parallel execution opportunities marked

✅ **Team Assignments** - Clear responsibilities for 3 people
- Location: `specs/001-vpa-mvp/TEAM_ASSIGNMENTS.md`
- Person 1: Draft & Verify Lead (~50 tasks)
- Person 2: Plan & Apply Lead (~50 tasks)
- Person 3: Eval, Gate & CLI Lead (~60 tasks)

✅ **Quality Checklists** - 246 quality checks total
- Person 1: `specs/001-vpa-mvp/checklists/person1-draft-verify.md` (54 checks)
- Person 2: `specs/001-vpa-mvp/checklists/person2-plan-apply.md` (76 checks)
- Person 3: `specs/001-vpa-mvp/checklists/person3-eval-gate-cli.md` (116 checks)

---

## 🎯 Quick Start: Day 1 (All Team Members)

### Step 1: Read Core Documents (2 hours)

Read in this order:

1. **Project README**: `Readme.md` (10 mins)
   - Understand VPA concept and motivation

2. **Feature Overview**: `specs/001-vpa-mvp/README.md` (10 mins)
   - Get overview of all documents

3. **Constitution**: `.specify/memory/constitution.md` (20 mins)
   - Understand project principles and non-negotiables

4. **Feature Spec**: `specs/001-vpa-mvp/spec.md` (30 mins)
   - Understand user stories and requirements

5. **Implementation Plan**: `specs/001-vpa-mvp/plan.md` (30 mins)
   - Understand architecture and technical approach

6. **Team Assignments**: `specs/001-vpa-mvp/TEAM_ASSIGNMENTS.md` (20 mins)
   - Find your role and responsibilities

### Step 2: Review Your Personal Assignment (30 mins)

**Person 1 (Draft & Verify Lead)**:
- Read your section in `TEAM_ASSIGNMENTS.md`
- Review `specs/001-vpa-mvp/tasks.md` Phase 3-4 (your tasks)
- Check `specs/001-vpa-mvp/checklists/person1-draft-verify.md`
- **Your Focus**: Candidate generation and verification quality

**Person 2 (Plan & Apply Lead)**:
- Read your section in `TEAM_ASSIGNMENTS.md`
- Review `specs/001-vpa-mvp/tasks.md` Phase 5-6, 9 (your tasks)
- Check `specs/001-vpa-mvp/checklists/person2-plan-apply.md`
- **Your Focus**: Planner logic and LoRA adapter training

**Person 3 (Eval, Gate & CLI Lead)**:
- Read your section in `TEAM_ASSIGNMENTS.md`
- Review `specs/001-vpa-mvp/tasks.md` Phase 2, 7-8, 10-15 (your tasks)
- Check `specs/001-vpa-mvp/checklists/person3-eval-gate-cli.md`
- **Your Focus**: Quality control, metrics, and user experience

### Step 3: Set Up Development Environment (1 hour)

```bash
# Clone repository (if not already done)
git clone <repository-url>
cd vpa-llm-fixer

# Create feature branch
git checkout -b 001-vpa-mvp

# Install Python 3.11 (if not installed)
# On macOS with Homebrew:
brew install python@3.11

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install core dependencies (requirements.txt will be created in Phase 1)
pip install torch transformers peft datasets pytest pytest-cov
```

### Step 4: Complete Phase 1 Setup Tasks Together (2-3 hours)

All three people work through tasks T001-T015:

```bash
# Create project structure (T001)
mkdir -p vpa/{draft,verify,plan,apply,data,eval,cli,utils}
mkdir -p vpa/cli/commands
mkdir -p tests/{unit,integration,contract}
mkdir -p configs/experiments
mkdir -p scripts
mkdir -p docs
mkdir -p data/{models,datasets,adapters,stability_sets,experiments}
mkdir -p .github/workflows

# Create __init__.py files
find vpa -type d -exec touch {}/__init__.py \;
find tests -type d -exec touch {}/__init__.py \;

# Create configs (T005-T008) - coordinate who creates which
# Person 1: configs/datasets.yaml
# Person 2: configs/base.yaml, configs/planner_grid.yaml
# Person 3: configs/verifiers.yaml

# Continue with remaining setup tasks...
```

Coordinate on Slack/Teams/Discord during this phase.

---

## 📅 Timeline Overview

### Week 1: Research & Design
- **Days 1-2**: Setup + Phase 0 Research
  - Person 1: Research verifier approaches
  - Person 2: Research LoRA best practices
  - Person 3: Research evaluation metrics
  - All: Document findings in `research.md`

- **Days 3-5**: Phase 1 Design
  - All: Create `data-model.md`, `contracts/`, `quickstart.md`
  - Person 3: Update agent context

### Week 2: MVP Core Implementation
- **Days 1-3**: Core modules
  - Person 1: Draft generation + Factual verifier
  - Person 2: LoRA trainer skeleton
  - Person 3: Metrics + QA harness

- **Days 4-5**: Integration & Demo
  - All: End-to-end pipeline test
  - All: MVP demo (one example through full pipeline)

### Weeks 3-5: Full System
- Complete all verifiers, planner, gate, CLI
- Full testing infrastructure
- All 3 datasets working

### Weeks 6-8: Experiments & Publication
- Run all baseline and VPA experiments
- Ablation studies
- Generate publication-ready results

---

## 🎯 Success Milestones

### ✅ Week 2 Milestone: MVP Demo
- Generate 5 candidates for one HotpotQA question
- Verify with ensemble scoring
- Train tiny adapter on 50 examples
- Run gate evaluation
- Full pipeline works!

### ✅ Week 5 Milestone: Full System
- All 3 datasets working end-to-end
- All features implemented
- Test suite passing on CI

### ✅ Week 6 Milestone: Baseline Results
- Baseline and initial VPA experiments complete
- At least one adapter passes gate

### ✅ Week 8 Milestone: Publication Ready
- All experiments with 3 seeds
- Publication-quality results
- Reproducibility verified

---

## 📞 Need Help?

### Where to Find Information

| Question | Document |
|----------|----------|
| What are the requirements? | `specs/001-vpa-mvp/spec.md` |
| How should we build it? | `specs/001-vpa-mvp/plan.md` |
| What tasks do I have? | `specs/001-vpa-mvp/tasks.md` |
| What's my role? | `specs/001-vpa-mvp/TEAM_ASSIGNMENTS.md` |
| What quality checks? | `specs/001-vpa-mvp/checklists/person*.md` |
| What are the principles? | `.specify/memory/constitution.md` |

### Communication

**Daily Standups** (15 minutes):
- What I completed yesterday
- What I'm working on today
- Any blockers

**Weekly Sync** (1 hour):
- Demo working features
- Discuss integration challenges
- Plan next week

---

## 📊 By the Numbers

- **Timeline**: 8 weeks total (MVP in 2 weeks)
- **Team Size**: 3 people
- **Total Tasks**: 183
- **Quality Checks**: 246
- **User Stories**: 6 (prioritized P1-P3)
- **Functional Requirements**: 15
- **Success Criteria**: 10
- **Research Questions**: 4

---

## 🎉 You're Ready!

Everything is planned and documented. You have:

✅ Clear requirements and acceptance criteria
✅ Complete architecture and technical design
✅ Detailed task breakdown with ownership
✅ Quality checklists for validation
✅ 8-week timeline with milestones
✅ Team coordination strategy

**Next Action**: Each person reads their assignment, then start Day 1 together!

```bash
# Create the feature branch
git checkout -b 001-vpa-mvp

# Start with Phase 1 setup tasks (T001-T015)
# Work together, coordinate on communication channel
```

---

## 📚 Document Map

```
vpa-llm-fixer/
├── GET_STARTED.md                           ← YOU ARE HERE
├── Readme.md                                ← Project overview
├── .specify/memory/constitution.md          ← Project principles
└── specs/001-vpa-mvp/
    ├── README.md                            ← Feature doc index
    ├── spec.md                              ← Requirements (6 user stories)
    ├── plan.md                              ← Architecture & design
    ├── tasks.md                             ← 183 tasks breakdown
    ├── TEAM_ASSIGNMENTS.md                  ← 3-person team guide
    └── checklists/
        ├── person1-draft-verify.md          ← 54 quality checks
        ├── person2-plan-apply.md            ← 76 quality checks
        └── person3-eval-gate-cli.md         ← 116 quality checks
```

**Good luck building VPA! 🚀**

Let's improve LLM precision without unstable RL!
