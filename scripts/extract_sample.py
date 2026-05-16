"""
M-TOOLS Phase 6: Human Verification Sampling
============================================
Extracts a 10% stratified random sample of the validated dataset 
for manual review. Outputs to a CSV file for easy importing 
into Google Sheets/Excel.
"""

import json
import csv
import random
from pathlib import Path
from collections import defaultdict

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASET_PATH = PROJECT_ROOT / "data" / "validated_data.jsonl"
OUTPUT_CSV = PROJECT_ROOT / "data" / "human_review_sample.csv"

def extract_sample(sample_fraction=0.10):
    if not DATASET_PATH.exists():
        print(f"Error: {DATASET_PATH} not found.")
        return

    # Load all data
    data = []
    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                data.append(json.loads(line.strip()))

    # Stratify by language/template_type
    strata = defaultdict(list)
    for d in data:
        # Use template_type as the primary strata (or language)
        # Seeds have 'English Baseline' or similar in category, so fallback to language
        strat_key = d.get("template_type") or d.get("language", "unknown")
        strata[strat_key].append(d)

    sampled_data = []
    
    print(f"Loaded {len(data)} total entries. Extracting {sample_fraction*100:.0f}% sample...\n")
    
    # Sample 10% from each strata
    for key, items in strata.items():
        sample_size = max(1, int(len(items) * sample_fraction))
        sample = random.sample(items, sample_size)
        sampled_data.extend(sample)
        print(f" - {key}: Sampled {sample_size} out of {len(items)}")

    # Shuffle the final sample so it's randomized for the reviewer
    random.shuffle(sampled_data)

    print(f"\nTotal sampled: {len(sampled_data)}")

    # Write to CSV
    headers = [
        "id", "template_type", "tool", "user_query", 
        "requires_clarification", "ground_truth", 
        "Review_Status (OK/Fix/Drop)", "Reviewer_Notes"
    ]

    with open(OUTPUT_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        for d in sampled_data:
            # Format ground truth nicely
            gt = d.get("ground_truth", {})
            gt_str = json.dumps(gt, ensure_ascii=False)
            
            row = [
                d.get("id", ""),
                d.get("template_type") or d.get("language", ""),
                d.get("tool", ""),
                d.get("user_query", ""),
                "Yes" if d.get("requires_clarification") else "No",
                gt_str,
                "",  # Empty column for reviewer
                ""   # Empty column for reviewer
            ]
            writer.writerow(row)

    print(f"\nSample exported successfully to: {OUTPUT_CSV.relative_to(PROJECT_ROOT)}")
    print("Tip: You can import this CSV into Google Sheets for collaborative review.")

if __name__ == "__main__":
    # Fixed seed for reproducibility (so rerunning gives the same sample if needed)
    random.seed(42)
    extract_sample(0.10)
