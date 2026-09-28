# Salivo AI Corpus ⚡

> **A curated, 100% compiler-verified dataset of idiomatic Salivo code for training ultra-fast Small Language Models (SLMs) and IDE coding copilots.**

---

## 🎯 Mission

General AI models frequently hallucinate when generating code in **Salivo** because it is absent from standard web-scale pre-training datasets. 

This repository solves that bottleneck by providing:
1. **Canonical Code Corpus**: High-quality, idiomatic Salivo programs spanning fundamentals, data structures, algorithms, systems programming, and networking.
2. **Zero-Hallucination Guarantee**: Every single `.sal` file in this repository is strictly checked and validated by the official Salivo compiler (`sf check` / `sf run`).
3. **Training & Fine-Tuning Pipelines**: Ready-to-use dataset generators for:
   - **Pre-training / Continued Pre-training** (raw verified code)
   - **Fill-In-The-Middle (FIM)** (for sub-10ms IDE ghost-text autocomplete)
   - **Instruction-Tuning (SFT)** (prompt-response pairs for assistant models)

---

## 📁 Repository Structure

```
salivo-ai-corpus/
├── corpus/
│   ├── 01_language_basics/        # Stream headers (><), types, control flow, interpolation
│   ├── 02_collections/            # Vec<T>, Map<K, V>, Heap<T>, BTree<K, V>
│   ├── 03_algorithms/             # Sorting, searching, graph traversal, math
│   ├── 04_traits_and_raii/        # Trait polymorphism, impl Drop deterministic cleanup
│   ├── 05_file_io/                # Path manipulation, filesystem read/write
│   └── 06_networking/             # TCP socket server, client streams
├── scripts/
│   ├── verify_all.py              # Automated compiler verification runner (sf check)
│   └── build_dataset.py           # Exports pretraining, FIM, and SFT datasets (.jsonl)
├── datasets/                      # Exported JSONL training data
├── .gitignore
└── README.md
```

---

## 🛠️ Verification & Tooling

### 1. Verify All Samples with the Compiler
Run the automated verification script to ensure every file passes the Salivo compiler:
```bash
python scripts/verify_all.py
```

### 2. Run an Individual Sample
```bash
sf run corpus/01_language_basics/01_hello.sal
```

### 3. Generate Training Datasets
Export your corpus into training formats ready for Hugging Face, PyTorch, or Unsloth:
```bash
python scripts/build_dataset.py
```

---

## 📜 Key Salivo Syntax Rules

- **Stream Header Imports (`><`)**: Imports stream directly into modules (e.g. `><salivo.std.core::{outln};`).
- **The Zero-Underscore Type Law**: Types, structs, traits, and enums strictly use `PascalCase` with no underscores (`_` is never a datatype).
- **Explicit Dynamic Arrays**: Built-in generic vector methods (`vecNew<T>()`, `push<T>(v, val)`, `veclen<T>(v)`).
- **String Interpolation**: Template syntax using `$"..."` with postfix formatters (`{val:str}`, `{val:trim:upper}`).
- **Deterministic RAII**: Resource management with `impl Drop for StructName`.
