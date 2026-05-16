"""
M-TOOLS Phase 6: Dataset Validation
===================================
Validates the expanded dataset for:
1. JSON syntax & required keys
2. Tool existence
3. Parameter schema validation (using jsonschema)
4. Duplicate IDs / Queries
5. Empty fields
6. Canonical formatting
"""

import json
import sys
from pathlib import Path
from collections import Counter
from jsonschema import validate, exceptions

# Import schemas from tools.schemas
# We need to add the project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))
from tools.schemas import TOOL_SCHEMAS

DATASET_PATH = PROJECT_ROOT / "data" / "expanded_data.jsonl"
VALIDATED_OUTPUT = PROJECT_ROOT / "data" / "validated_data.jsonl"

def load_schemas():
    return {schema["name"]: schema for schema in TOOL_SCHEMAS}

def check_empty(val):
    if val is None:
        return False  # Null is allowed for some fields like 'difficulty'
    if isinstance(val, str) and not val.strip():
        return True
    if isinstance(val, (list, dict)) and not val:
        return True
    return False

def run_validation():
    if not DATASET_PATH.exists():
        print(f"Error: Dataset not found at {DATASET_PATH}")
        return

    schemas = load_schemas()
    
    valid_entries = []
    errors = {
        "syntax_error": 0,
        "missing_keys": 0,
        "invalid_tool": 0,
        "schema_error": 0,
        "empty_fields": 0,
        "duplicate_id": 0,
        "duplicate_query": 0,
    }

    seen_ids = set()
    seen_queries = set()

    required_keys = {
        "id", "original_id", "template_type", "user_query", 
        "tool", "category", "ground_truth", "language"
    }

    print(f"Starting validation of {DATASET_PATH.name}...\n")
    
    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()

    total_lines = len(lines)
    
    for line_idx, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            continue

        # 1. Syntax Validation
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            errors["syntax_error"] += 1
            print(f"[Line {line_idx}] Invalid JSON syntax.")
            continue

        # 2. Required Keys
        missing = required_keys - set(entry.keys())
        if missing:
            errors["missing_keys"] += 1
            print(f"[Line {line_idx}] Missing keys: {missing}")
            continue

        # 3. Duplicate Detection
        entry_id = entry.get("id")
        query = entry.get("user_query", "").strip()

        if entry_id in seen_ids:
            errors["duplicate_id"] += 1
            print(f"[Line {line_idx}] Duplicate ID: {entry_id}")
            continue
        seen_ids.add(entry_id)

        if query in seen_queries:
            errors["duplicate_query"] += 1
            # We don't drop duplicate queries if they are intended, but it's good to track.
            # Actually, let's treat exact query duplicates as a drop to ensure uniqueness.
            # print(f"[Line {line_idx}] Duplicate query string: {query}")
            continue
        seen_queries.add(query)

        # 4. Empty Fields Detection
        has_empty = False
        for k, v in entry.items():
            if k not in ["failure_type_injected", "difficulty", "requires_clarification", "conversation_context"]:
                if check_empty(v):
                    print(f"[Line {line_idx}] Empty field detected: '{k}'")
                    has_empty = True
                    break
        if has_empty:
            errors["empty_fields"] += 1
            continue

        # 5. Schema Validation
        tool_name = entry.get("tool")
        if tool_name not in schemas:
            errors["invalid_tool"] += 1
            print(f"[Line {line_idx}] Invalid tool: {tool_name}")
            continue

        tool_schema = schemas[tool_name]["parameters"]
        ground_truth = entry.get("ground_truth", {})
        
        # In seed dataset, ground_truth has {"tool_name": "...", "parameters": {...}}
        parameters = ground_truth.get("parameters", {})
        if "parameters" not in ground_truth:
            # fallback if it's formatted flat
            parameters = ground_truth

        try:
            # For this benchmark, many queries intentionally omit required parameters
            # (either for clarification tests or parameter localization tests).
            # We validate property types, but do not enforce the 'required' list.
            schema_to_use = tool_schema.copy()
            schema_to_use.pop("required", None)

            validate(instance=parameters, schema=schema_to_use)
        except exceptions.ValidationError as e:
            errors["schema_error"] += 1
            print(f"[Line {line_idx}] Schema error in '{tool_name}': {e.message}")
            continue

        valid_entries.append(entry)

    print("\n" + "="*50)
    print("VALIDATION SUMMARY")
    print("="*50)
    print(f"Total processed: {total_lines}")
    print(f"Valid entries:   {len(valid_entries)}")
    
    total_errors = sum(errors.values())
    print(f"Total errors:    {total_errors}")
    if total_errors > 0:
        print("\nError Breakdown:")
        for k, v in errors.items():
            if v > 0:
                print(f"  - {k}: {v}")

    # Write validated dataset
    with open(VALIDATED_OUTPUT, "w", encoding="utf-8") as f:
        for d in valid_entries:
            f.write(json.dumps(d, ensure_ascii=False) + "\n")
    print(f"\nValidated dataset exported to: {VALIDATED_OUTPUT.relative_to(PROJECT_ROOT)}")

if __name__ == "__main__":
    run_validation()
