# M-TOOLS

## Benchmarking Robust Multilingual Tool Calling Under Code-Switching and Parameter Localization

Author: Sahil Al Farib
Target Venue:

- EMNLP 2026 Main / Findings
- EMNLP Workshop (fallback)

---

# 1. Core Research Idea

Large Language Models can call tools/APIs reliably in English,
but fail in realistic multilingual settings involving:

- code-switching
- transliteration
- localized parameter values
- noisy multilingual prompts
- tool execution failures

This project creates:

1. A realistic multilingual tool-calling benchmark focusing on the language-tool boundary
2. An executable evaluation environment with mock APIs and execution traces
3. A robustness evaluation framework testing failure recovery and retry behavior
4. A failure taxonomy for parameter canonicalization and multilingual agent systems

---

# 2. Main Research Questions

## RQ1

How robust are modern LLMs at multilingual tool calling?

## RQ2

How badly does performance degrade under:

- code-switching
- transliteration
- localized parameter grounding
- multi-turn interaction
- tool failures

## RQ3

Can models recover from execution failures automatically?

## RQ4

What are the most common multilingual tool-calling failure patterns?

---

# 3. Novel Contributions

## Contribution 1

A multilingual benchmark for realistic tool use.

## Contribution 2

Evaluation of code-switched tool calling.

## Contribution 3

Localized parameter grounding benchmark.

Example:
User:
"আগামীকাল ঢাকার weather কেমন?"

Correct API parameter:
{
"city": "Dhaka"
}

NOT:
{
"city": "ঢাকা"
}

## Contribution 4

Tool failure recovery evaluation.

## Contribution 5

Failure taxonomy for multilingual agent systems.

---

# 4. Scope

DO NOT over-expand the project.

Focus on:

- quality
- realism
- evaluation rigor

NOT:

- giant scale
- training giant models
- many languages

---

# 5. Languages

## Primary Languages

- English
- Bangla

## Secondary

- Bangla-English code-switching
- Transliteration variants

Examples:

- "Kal Dhaka er weather bolo"
- "amar jonno ride book koro"

---

# 6. Tool Categories

Keep total tools between 5–10.

## Planned Tools

### Weather

get_weather

### Calendar

create_calendar_event

### Ride Booking

book_ride

### Food Ordering

order_food

### Email

send_email

### Flight Search

search_flights

### Currency Conversion

currency_convert

---

# 7. Benchmark Categories

## Category A — English Baseline

Simple clean English prompts.

## Category B — Pure Multilingual

Pure Bangla prompts.

## Category C — Code-Switching

Mixed-language prompts.

## Category D — Transliteration

Romanized local languages.

## Category E — Parameter Localization

Localized entities.

## Category F — Multi-turn Tool Use

Conversation memory.

## Category G — Tool Failure Recovery

API failures injected intentionally.

## Category H — Ambiguous Requests

Model must clarify missing information.

---

# 8. Dataset Design

## Dataset Size Goal

Target:

- 6,000–7,000 examples (Original target: 3,000–5,000)

NOT 100k examples.

Quality > Quantity.

---

# 9. Dataset Schema

Each example should contain:

{
"id": "",
"language": "",
"category": "",
"tool": "",
"user_query": "",
"ground_truth": {},
"difficulty": "",
"requires_clarification": false
}

---

# 10. Example Entry

{
"id": 1001,
"language": "bangla-english",
"category": "parameter_localization",
"tool": "get_weather",
"user_query": "আগামীকাল ঢাকার weather কেমন?",
"ground_truth": {
"city": "Dhaka",
"date": "tomorrow"
},
"difficulty": "medium",
"requires_clarification": false,
"failure_type_injected": null
}

---

# 11. Data Generation Pipeline

## Phase 1 — Manual Seeds

Handcraft:

- 50–100 examples per tool

Goal:
high realism.

---

## Phase 2 — LLM Expansion (Gemini API)

Use **Gemini 3.1 Flash Lite API** (Replaced Qwen2.5-32B due to hallucination issues) to generate:
- **Persona-based variations**: WhatsApp style, code-switched.
- **Pure Bangla**: Varied sentence structures.
- **Transliteration Tiers**: Full, Mixed, and Heavy Shorthand generated via prompt.
- **Two-Pass Filter**: Semantic fidelity check + naturalness scoring (score >= 4).

## Phase 3 — Rule-Based Augmentation

Programmatically generate:
- **Transliteration Tiers**: Full, Mixed, and Heavy Shorthand (e.g., "amr", "kmn").
- **Slot-Based Switching**: Constrained code-switching (e.g., switch nouns/verbs, never connectives).
- **Spelling Noise**: Typos and phonetic variations.

---

## Phase 4 — Automatic Validation

Validate:
- JSON syntax & Schema adherence
- Canonical parameter forms (e.g., ঢাকা → Dhaka)
- Robust extraction (Regex/Retry layers for LLM output)

---

## Phase 5 — Human Verification

Stratified manual inspection:
- **Hand-crafted (S2)**: 100%
- **LLM Expansion (S3)**: 20–30%
- **Rule-based (S4)**: 40–60% (High noise risk)

Fix robotic phrasing, incorrect labels, and unnatural code-switching.

---

# 12. Canonicalization System

One of the key contributions.

Map:

- localized city names
- transliterated names
- spelling variants

to canonical API-compatible forms.

Examples:
ঢাকা → Dhaka
চট্টগ্রাম → Chittagong

---

# 13. Evaluation Metrics

## Tool Selection Accuracy

Correct tool chosen?

## Parameter Accuracy

Correct arguments extracted?

## Canonicalization Accuracy

Localized values normalized correctly?

## Execution Success Rate

Would API execute successfully?

## Recovery Success Rate

Can model recover after failure?

## Clarification Accuracy

Does model ask clarification when needed (especially for FT0)?

## Difficulty Calibration

Does model performance correlate with the **Mechanical Difficulty Rubric** (+1 per factor)?

---

# 14. Models To Evaluate

## Free / Open Models

### Gemini

- Gemini Flash
- Gemini Pro (if available)

### Open Models

- Qwen2.5
- Llama 3
- Gemma
- DeepSeek

---

# 15. Infrastructure

## Local Inference

- vLLM
- Ollama
- Transformers

## Evaluation

- Python
- JSONSchema
- Pydantic

## Dataset

- JSONL

## Experiment Tracking

- Weights & Biases (optional)

---

# 16. Experiment Design

## Experiment 1

English baseline.

## Experiment 2

Pure multilingual evaluation.

## Experiment 3

Code-switching robustness.

## Experiment 4

Transliteration robustness.

## Experiment 5

Parameter localization.

## Experiment 6

Tool recovery evaluation.

---

## FT0 — Ambiguous Entity Resolution
Pre-execution ambiguity (Geographic, Temporal, or Underspecification).

## FT1 — Tool Selection Failure
Wrong tool selected.

## FT2 — Parameter Grounding Failure
Correct tool but localized or wrong parameters.

## FT3 — Localization Leakage
API parameter contains local script (e.g., "ঢাকা").

## FT4 — Missing Required Parameter
Missing info not caught by clarification logic.

## FT5 — Failure Recovery Collapse
Model fails to handle system error (Timeout/503).

## FT6 — Multi-turn Memory Inconsistency
Context lost across conversation turns.

---

# 18. Main Expected Findings

Possible findings:

- Models perform well in English but degrade heavily under code-switching.
- Parameter localization is a major hidden failure source.
- Transliteration significantly reduces execution success.
- Models often understand intent but fail at API-compatible grounding.

---

# 19. Timeline

## Month 1

Literature review.
Finalize benchmark design.

## Month 2

Create tools and schemas.
Write seed examples.

## Month 3

Dataset generation pipeline.

## Month 4

Validation and cleanup.

## Month 5

Evaluation framework.

## Month 6

Run experiments.

## Month 7

Analyze failures.

## Month 8

Write paper.

## Month 9

Paper polishing.
Open-source release.

---

# 20. Repository Structure

project/
│
├── data/
├── tools/
├── evaluation/
├── generation/
├── scripts/
├── experiments/
├── results/
├── paper/
└── [README.md](http://readme.md/)

---

# 21. Open-Source Goals

Release:

- benchmark
- evaluation scripts
- tool schemas
- multilingual examples
- leaderboard scripts

---

# 22. Risks

## Risk 1

Synthetic-looking prompts.

Mitigation:
Human verification.

---

## Risk 2

Too many languages.

Mitigation:
Keep scope small.

---

## Risk 3

Weak novelty.

Mitigation:
Focus on:

- code-switching
- localization
- recovery robustness

---

# 23. Publication Strategy

## Primary

EMNLP 2026 Findings/Main

## Backup

EMNLP Workshop

## Secondary

ACL Rolling Review

---

# 24. Paper Structure

## 1. Introduction

Problem motivation.

## 2. Related Work

Existing multilingual tool benchmarks.

## 3. Benchmark Design

Dataset and tools.

## 4. Evaluation Framework

Metrics and execution system.

## 5. Experiments

Results.

## 6. Failure Analysis

Key contribution section.

## 7. Limitations

## 8. Conclusion

---

# 25. Success Criteria

The project succeeds if:

- benchmark is realistic
- evaluation is rigorous
- failure analysis is insightful
- multilingual robustness gaps are clearly demonstrated

Even without frontier APIs.

---

# 26. Most Important Rule

DO NOT try to build:

- the largest benchmark
- the most languages
- the most tools

Instead build:

- the most realistic multilingual tool-calling benchmark.