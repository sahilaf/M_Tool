# M-TOOLS: Multilingual Tool Calling Benchmark

Benchmarking Robust Multilingual Tool Calling Under Code-Switching and Parameter Localization.

## Dataset Summary

| Metric | Value |
|---|---|
| **Seed examples** | 415 (manually curated) |
| **Expanded examples** | 6,427 (Gemini-generated) |
| **Total** | **6,842** |
| **Languages** | English, Bangla, Bangla-English code-switched, Transliteration |
| **Tools covered** | 7 (weather, ride, food, email, calendar, flights, currency) |

### Language Distribution

| Language | Count |
|---|---|
| Bangla-English code-switch | 2,151 |
| Pure Bangla | 2,196 |
| Transliteration (Banglish) | 2,080 |
| English (seeds) | 415 |

## Repository Structure

```
M_Tool/
├── data/
│   ├── raw/
│   │   └── seed_dataset.jsonl       # 415 curated seed examples
│   └── expanded_data.jsonl          # 6,427 expanded examples
├── generation/
│   ├── expand_dataset.py            # Parallel Gemini generation pipeline
│   ├── dataset_generation_phase5.ipynb  # Colab notebook version
│   └── checkpoint.jsonl             # Generation checkpoint (resume support)
├── tools/                           # Tool schemas and mock execution
├── evaluation/                      # Evaluation pipeline and metrics
├── experiments/                     # Experiment configs and outputs
├── results/                         # Final results and failure analysis
├── paper/                           # EMNLP paper materials
├── checklist.md                     # Project progress tracker
├── dataset_creation.md              # Dataset creation methodology
├── manual_review_guidelines.md      # Review guidelines for annotators
└── plan.md                          # Full project plan
```

## Generation Pipeline

The dataset expansion uses **Gemini 3.1 Flash Lite API** with:
- **3 templates**: Code-switch, Pure Bangla, Transliteration
- **Two-pass filtering**: Semantic fidelity check + naturalness scoring (≥4/5)
- **Parallel execution**: 5 API keys with thread-safe round-robin rotation
- **92% approval rate** across 6,427 generated examples

## Quality Metrics

| Naturalness Score | Count | % |
|---|---|---|
| 5 (very natural) | 4,759 | 74% |
| 4 (natural) | 1,668 | 26% |

## Phases

- ✅ Phase 1–4: Seed creation, schema design, tool implementation
- ✅ Phase 5: Dataset generation (6,427 examples)
- ⬜ Phase 6: Validation & cleanup
- ⬜ Phase 7: Evaluation pipeline
- ⬜ Phase 8: Experiments & paper writing
