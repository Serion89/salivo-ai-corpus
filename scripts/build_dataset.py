#!/usr/bin/env python3
"""
Dataset export pipeline for Salivo AI Corpus.
Splits datasets into chunked parts to stay well under GitHub's 100MB single-file limit.
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
    lines = code_text.splitlines()
    if len(lines) < 6:
        return []
    samples = []
    for _ in range(num_samples):
        start_cut = random.randint(2, len(lines) - 3)
        cut_len = random.randint(1, min(4, len(lines) - start_cut - 1))
        end_cut = start_cut + cut_len
        prefix = "\n".join(lines[:start_cut]) + "\n"
        middle = "\n".join(lines[start_cut:end_cut]) + "\n"
        suffix = "\n".join(lines[end_cut:])
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

    # Clean old files
    for old_f in output_dir.glob("*.jsonl"):
        old_f.unlink()

    sal_files = sorted(list(corpus_dir.rglob("*.sal")))
    print(f">> Processing {len(sal_files)} Salivo files for training datasets...")

    pretrain_file = output_dir / "pretrain_corpus.jsonl"
    sft_file = output_dir / "instruct_sft.jsonl"

    pretrain_count = 0
    sft_count = 0
    fim_count = 0

    fim_part1 = output_dir / "fim_part1.jsonl"
    fim_part2 = output_dir / "fim_part2.jsonl"

    f_fim1 = open(fim_part1, "w", encoding="utf-8")
    f_fim2 = open(fim_part2, "w", encoding="utf-8")

    with open(pretrain_file, "w", encoding="utf-8") as f_pre, \
         open(sft_file, "w", encoding="utf-8") as f_sft:

        for file_path in sal_files:
            rel_path = str(file_path.relative_to(root_dir)).replace("\\", "/")
            code_text = file_path.read_text(encoding="utf-8")

            # 1. Pretraining entry
            f_pre.write(json.dumps({"id": rel_path, "text": code_text}) + "\n")
            pretrain_count += 1

            # 2. FIM Autocomplete entries (split between part 1 and part 2)
            fim_samples = create_fim_samples(code_text, rel_path, num_samples=3)
            for sample in fim_samples:
                if fim_count % 2 == 0:
                    f_fim1.write(json.dumps(sample) + "\n")
                else:
                    f_fim2.write(json.dumps(sample) + "\n")
                fim_count += 1

            # 3. SFT / Instruct entry
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

    f_fim1.close()
    f_fim2.close()

    print("\n==========================================")
    print("Dataset Generation Complete (GitHub-Safe Chunking):")
    print(f"  Pretrain samples: {pretrain_count} -> {pretrain_file.name}")
    print(f"  FIM Part 1:       {fim_count // 2} -> {fim_part1.name}")
    print(f"  FIM Part 2:       {fim_count - (fim_count // 2)} -> {fim_part2.name}")
    print(f"  SFT chat samples: {sft_count} -> {sft_file.name}")
    print("==========================================")

if __name__ == "__main__":
    main()
