#!/usr/bin/env python3
"""
Dataset export pipeline for Salivo AI Corpus.
Generates:
1. pretrain_corpus.jsonl   - Raw text for continuous pre-training
2. fim_autocomplete.jsonl  - Fill-in-the-middle for instant IDE autocomplete
3. instruct_sft.jsonl      - Supervised fine-tuning instruction pairs
"""

import os
import sys
import json
import random
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

SYSTEM_PROMPT = (
    "You are an expert Salivo systems programming assistant. Write clean, "
    "idiomatic Salivo code using stream header imports (><), the zero-underscore type law, "
    "and proper error handling."
)

def create_fim_samples(code_text, filename, num_samples=3):
    """Generates Fill-In-The-Middle (FIM) training samples."""
    lines = code_text.splitlines()
    if len(lines) < 6:
        return []

    samples = []
    for _ in range(num_samples):
        # Pick cut points
        start_cut = random.randint(2, len(lines) - 3)
        cut_len = random.randint(1, min(4, len(lines) - start_cut - 1))
        end_cut = start_cut + cut_len

        prefix = "\n".join(lines[:start_cut]) + "\n"
        middle = "\n".join(lines[start_cut:end_cut]) + "\n"
        suffix = "\n".join(lines[end_cut:])

        # Standard StarCoder/CodeLlama FIM format
        fim_text = f"<fim_prefix>{prefix}<fim_suffix>{suffix}<fim_middle>{middle}"
        samples.append({
            "source_file": filename,
            "prefix": prefix,
            "suffix": suffix,
            "middle": middle,
            "prompt": f"<fim_prefix>{prefix}<fim_suffix>{suffix}<fim_middle>",
            "completion": middle,
            "full_fim": fim_text
        })
    return samples

def main():
    root_dir = Path(__file__).resolve().parent.parent
    corpus_dir = root_dir / "corpus"
    output_dir = root_dir / "datasets"
    output_dir.mkdir(parents=True, exist_ok=True)

    sal_files = sorted(list(corpus_dir.rglob("*.sal")))
    print(f">> Processing {len(sal_files)} Salivo files for training datasets...")

    pretrain_file = output_dir / "pretrain_corpus.jsonl"
    fim_file = output_dir / "fim_autocomplete.jsonl"
    sft_file = output_dir / "instruct_sft.jsonl"

    pretrain_count = 0
    fim_count = 0
    sft_count = 0

    with open(pretrain_file, "w", encoding="utf-8") as f_pre, \
         open(fim_file, "w", encoding="utf-8") as f_fim, \
         open(sft_file, "w", encoding="utf-8") as f_sft:

        for file_path in sal_files:
            rel_path = str(file_path.relative_to(root_dir)).replace("\\", "/")
            code_text = file_path.read_text(encoding="utf-8")

            # 1. Pretraining entry
            f_pre.write(json.dumps({
                "id": rel_path,
                "text": code_text
            }) + "\n")
            pretrain_count += 1

            # 2. FIM Autocomplete entries
            fim_samples = create_fim_samples(code_text, rel_path, num_samples=3)
            for sample in fim_samples:
                f_fim.write(json.dumps(sample) + "\n")
                fim_count += 1

            # 3. SFT / Instruct entry
            # Extract header description if present or construct from module/path
            title = Path(rel_path).stem.replace("_", " ").title()
            instruction = f"Write an idiomatic Salivo module implementing {title} with standard imports and verification."
            
            f_sft.write(json.dumps({
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": instruction},
                    {"role": "assistant", "content": f"```salivo\n{code_text}\n```"}
                ]
            }) + "\n")
            sft_count += 1

    print("\n==========================================")
    print("Dataset Generation Complete:")
    print(f"  Pretrain samples: {pretrain_count} -> {pretrain_file.name}")
    print(f"  FIM samples:      {fim_count} -> {fim_file.name}")
    print(f"  SFT chat samples: {sft_count} -> {sft_file.name}")
    print("==========================================")

if __name__ == "__main__":
    main()
