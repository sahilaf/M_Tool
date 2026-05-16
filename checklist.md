## M-TOOLS — Multilingual Tool Calling Benchmark

---

# PHASE 0 — PROJECT INITIALIZATION

## Goal

Set up project structure, scope, and workflow.

### Tasks

- [ ]  Finalize paper title
- [ ]  Create GitHub repository
- [ ]  Create folder structure
- [ ]  Setup Python environment
- [ ]  Setup GPU inference environment
- [ ]  Create [README.md](http://readme.md/)
- [ ]  Create project Kanban / task tracker
- [ ]  Decide benchmark scope
- [ ]  Decide language coverage
- [ ]  Decide tool categories

### Deliverables

- Clean repository
- Working environment
- Finalized scope

### Exit Criteria

- Repository runs successfully
- All folders created
- Scope frozen

---

# PHASE 1 — LITERATURE REVIEW

## Goal

Understand existing multilingual tool-calling research.

### Papers To Read

- [x]  MASSIVE-Agents
- [x]  ToolBench
- [x]  BFCL
- [x]  NESTFUL
- [x]  FunctionChat-Bench
- [x]  Lost in Execution
- [x]  Gorilla
- [x]  APIBench
- [x]  AgentBench

### Tasks

- [x]  Create related work notes
- [x]  Identify gaps
- [x]  Identify missing benchmark categories
- [x]  Create comparison table
- [x]  Collect evaluation metrics used by prior work
- [x]  Analyze weaknesses of current datasets

### Deliverables

- Literature summary document
- Gap analysis table
- Benchmark positioning statement

### Exit Criteria

- Clear novelty statement exists
- Contributions finalized

---

# PHASE 2 — BENCHMARK DESIGN

## Goal

Design benchmark structure and evaluation tasks.

### Tasks

- [x]  Define benchmark categories
- [x]  Define task taxonomy
- [x]  Define failure taxonomy
- [x]  Define mechanical difficulty rubric (Checklist-based)
- [x]  Define annotation schema
- [x]  Define canonicalization rules
- [x]  Define execution environment behavior
- [x]  Define evaluation metrics

### Benchmark Categories

- [x]  English baseline
- [x]  Pure multilingual
- [x]  Code-switching
- [x]  Transliteration
- [x]  Multi-turn
- [x]  Failure recovery
- [x]  Ambiguous requests
- [x]  Parameter localization

### Deliverables

- Benchmark specification document

### Exit Criteria

- Benchmark structure frozen

---

# PHASE 3 — TOOL & SCHEMA DESIGN

## Goal

Build realistic tool schemas.

### Tools

- [x]  get_weather
- [x]  create_calendar_event
- [x]  send_email
- [x]  order_food
- [x]  book_ride
- [x]  search_flights
- [x]  currency_convert

### Tasks

- [x]  Create JSON schemas
- [x]  Create parameter definitions
- [x]  Define required/optional fields
- [x]  Create mock tool execution layer
- [x]  Create API response simulator
- [x]  Create failure injection system

### Failure Types

- [x]  FT0: Ambiguous Entity Resolution
- [x]  FT1: Wrong Localization
- [x]  FT2: Missing Parameter
- [x]  FT3: Tool Error (Recovery)
- [x]  FT4: Multi-turn Memory Failure
- [x]  Timeout simulation

### Deliverables

- Tool schema library
- Mock execution environment

### Exit Criteria

- All tools executable locally

---

# PHASE 4 — SEED DATA CREATION

## Goal

Create high-quality manual examples.

### Tasks

- [x]  Write English examples
- [x]  Write Bangla examples
- [x]  Write code-switched examples
- [x]  Write transliterated examples
- [x]  Write ambiguous examples
- [x]  Write recovery examples
- [x]  Write multi-turn examples

### Target

- [x]  50–100 examples per tool (Seed file generated, automated expansion prepared for Phase 5)

### Important Checks

- [x]  Natural phrasing
- [x]  Realistic requests
- [x]  Correct tool mapping
- [x]  Correct parameter grounding

### Deliverables

- [x]  Seed dataset

### Exit Criteria

- [x]  Seeds reviewed manually

---

# PHASE 5 — DATASET GENERATION PIPELINE ✅

## Goal

Scale benchmark from 415 seeds to 4,000–5,000 examples using automated generation.

### LLM Generation (Gemini 3.1 Flash Lite API)

> **Note:** Originally planned for local Qwen2.5-32B on A100. Switched to Gemini API
> after Qwen produced poor Bangla-English code-switching quality (hallucinated words,
> semantic drift). Gemini achieved 92% approval rate with excellent naturalness.

- [x]  ~~Configure Qwen2.5-32B-Instruct~~ → Switched to Gemini 3.1 Flash Lite API
- [x]  Implement parallel inference (5 API keys, 5 threads, ~48 calls/min)
- [x]  Create Persona-based (Code-switch) templates
- [x]  Create Pure Bangla templates
- [x]  Create Transliteration shorthand templates (with mobile shorthand tiers)
- [x]  Build JSON extraction + retry logic
- [x]  Implement two-pass filtering (semantic fidelity + naturalness score ≥ 4)
- [x]  Set up checkpoint/resume system (`generation/checkpoint.jsonl`)

### Rule-Based Augmentation

> Skipped — LLM generation exceeded volume targets without needing rule-based augmentation.

- [x]  ~~Build transliteration scripts~~ → Covered by transliteration template
- [x]  ~~Build spelling noise generator~~ → Covered by shorthand tiers in prompts
- [ ]  Build parameter variation scripts (deferred — not needed for target)
- [ ]  Build mixed-language generator (deferred — not needed for target)

### Generation Quality Validation

- [x]  Semantic fidelity check (batched, per-variation)
- [x]  Naturalness scoring (1–5 scale, threshold ≥ 4)
- [x]  Approval rate: **92%** (6,427 approved / ~6,984 generated)

### Dataset Expansion Results

| Category | Target | Achieved |
|---|---|---|
| Code-switched (bangla-english) | 1,000 | **2,151** |
| Pure Bangla | 700 | **2,196** |
| Transliteration | 600 | **2,080** |
| **Total expanded** | **4,000–5,000** | **6,427** ✅ |

**By tool coverage:**
| Tool | Count |
|---|---|
| create_calendar_event | 1,517 |
| order_food | 1,395 |
| get_weather | 1,181 |
| book_ride | 759 |
| send_email | 601 |
| search_flights | 567 |
| currency_convert | 407 |

### Deliverables

- [x]  Raw expanded dataset (`data/expanded_data.jsonl` — 6,427 examples)
- [x]  Generation script (`generation/expand_dataset.py`)
- [x]  Checkpoint file (`generation/checkpoint.jsonl`)

### Exit Criteria

- [x]  Dataset exceeds target size (6,427 > 5,000)

---

# PHASE 6 — VALIDATION & CLEANUP

## Goal

Ensure benchmark quality.

### Automatic Validation

- [x]  JSON syntax validation
- [x]  Schema validation
- [x]  Parameter validation
- [x]  Duplicate detection
- [x]  Empty field detection

### Canonicalization Validation

- [x]  City normalization (Verified: All cities are properly capitalized English)
- [x]  Date normalization (Verified: Dates use canonical English e.g., 'today', 'tomorrow')
- [x]  Time normalization (Verified: Times use 24-hour HH:MM format)

### Human Verification

- [x]  Stratified Review (Generated 10% sample: `data/human_review_sample.csv`)
- [ ]  Remove unnatural prompts
- [ ]  Fix mislabeled examples
- [ ]  Improve edge cases

### Deliverables

- Final validated dataset

### Exit Criteria

- Benchmark quality acceptable

---

# PHASE 7 — EVALUATION FRAMEWORK

## Goal

Build model evaluation system.

### Tasks

- [ ]  Create inference pipeline
- [ ]  Create tool execution evaluator (with execution traces)
- [ ]  Create JSON parser
- [ ]  Create schema checker
- [ ]  Create recovery evaluator (retry behavior analysis)
- [ ]  Create multi-turn evaluator

### Metrics

- [ ]  Tool selection accuracy
- [ ]  Parameter accuracy
- [ ]  Canonicalization accuracy
- [ ]  Execution success
- [ ]  Recovery & retry success
- [ ]  Clarification accuracy
- [ ]  Localization accuracy

### Deliverables

- Full evaluation pipeline

### Exit Criteria

- End-to-end evaluation works

---

# PHASE 8 — MODEL EVALUATION

## Goal

Run experiments across models.

### Models

- [ ]  Gemini Flash
- [ ]  Gemini Pro
- [ ]  Qwen2.5
- [ ]  Llama 3
- [ ]  Gemma
- [ ]  DeepSeek

### Experiments

- [ ]  English baseline
- [ ]  Pure multilingual
- [ ]  Code-switching
- [ ]  Transliteration
- [ ]  Failure recovery
- [ ]  Multi-turn evaluation

### Deliverables

- Raw experiment outputs
- Benchmark scores

### Exit Criteria

- All experiments completed

---

# PHASE 9 — FAILURE ANALYSIS

## Goal

Extract research insights.

### Tasks

- [ ]  Categorize failures
- [ ]  Build failure taxonomy
- [ ]  Analyze localization failures
- [ ]  Analyze code-switch degradation
- [ ]  Analyze recovery collapse
- [ ]  Analyze model-specific weaknesses

### Visualizations

- [ ]  Accuracy tables
- [ ]  Error distributions
- [ ]  Failure heatmaps
- [ ]  Language degradation charts

### Deliverables

- Analysis report
- Final insights

### Exit Criteria

- Strong research narrative exists

---

# PHASE 10 — PAPER WRITING

## Goal

Write EMNLP paper.

### Sections

- [ ]  Abstract
- [ ]  Introduction
- [ ]  Related Work
- [ ]  Benchmark Design
- [ ]  Experimental Setup
- [ ]  Results
- [ ]  Failure Analysis
- [ ]  Limitations
- [ ]  Conclusion

### Tasks

- [ ]  Create figures
- [ ]  Create tables
- [ ]  Create benchmark examples
- [ ]  Write appendix
- [ ]  Add citations
- [ ]  Format for ACL template

### Deliverables

- Full paper draft

### Exit Criteria

- Internal review ready

---

# PHASE 11 — PAPER POLISHING

## Goal

Improve submission quality.

### Tasks

- [ ]  Proofreading
- [ ]  Grammar cleanup
- [ ]  Improve clarity
- [ ]  Improve figures
- [ ]  Tighten contributions
- [ ]  Reduce unnecessary content
- [ ]  Improve abstract
- [ ]  Improve title

### External Feedback

- [ ]  Ask peers for review
- [ ]  Ask researchers for feedback
- [ ]  Revise based on comments

### Deliverables

- Final submission draft

### Exit Criteria

- Submission-ready paper

---

# PHASE 12 — OPEN SOURCE RELEASE

## Goal

Release benchmark publicly.

### Tasks

- [ ]  Upload dataset
- [ ]  Upload evaluation scripts
- [ ]  Upload schemas
- [ ]  Upload inference scripts
- [ ]  Write documentation
- [ ]  Create leaderboard format
- [ ]  Add example notebooks

### Deliverables

- Public GitHub release

### Exit Criteria

- Reproducibility achieved

---

# PHASE 13 — SUBMISSION

## Goal

Submit to EMNLP.

### Tasks

- [ ]  Verify formatting
- [ ]  Verify anonymity rules
- [ ]  Final PDF generation
- [ ]  Upload supplementary material
- [ ]  Upload code repository
- [ ]  Submit before deadline

### Deliverables

- Submitted paper

### Exit Criteria

- Submission confirmed

---

# PHASE 14 — POST-SUBMISSION

## Goal

Maximize impact.

### Tasks

- [ ]  Create project website
- [ ]  Share benchmark online
- [ ]  Post on Twitter/X
- [ ]  Post on LinkedIn
- [ ]  Submit to PapersWithCode
- [ ]  Create demo videos
- [ ]  Prepare camera-ready version

### Stretch Goals

- [ ]  Workshop presentation
- [ ]  Benchmark leaderboard
- [ ]  Shared task proposal

### Deliverables

- Public research visibility

### Exit Criteria

- Research publicly discoverable

---

# FINAL SUCCESS CHECKLIST

## Research

- [ ]  Strong novelty
- [ ]  Realistic benchmark
- [ ]  Clear contributions
- [ ]  Strong experiments
- [ ]  Insightful failure analysis

## Engineering

- [ ]  Reproducible code
- [ ]  Clean dataset
- [ ]  Public benchmark
- [ ]  Evaluation framework

## Publication

- [ ]  EMNLP submission
- [ ]  Open-source release
- [ ]  Public documentation