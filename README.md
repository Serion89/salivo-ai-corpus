# Salivo AI Corpus

> **A curated, 100% compiler-verified dataset of 30,000+ idiomatic Salivo code modules for training ultra-fast Small Language Models (SLMs) and IDE coding copilots.**

---

## Mission

General AI models frequently hallucinate when generating code in **Salivo** because it is absent from standard web-scale pre-training datasets. 

This repository solves that bottleneck by providing:
1. **Canonical Code Corpus**: 30,000+ high-quality, compiler-verified Salivo programs spanning fundamentals, collections, algorithms, systems programming, traits, networking, security, backend APIs, frontend templates, and memory management.
2. **Zero-Hallucination Guarantee**: Every single `.sal` file in this repository is strictly checked and validated by the official Salivo compiler driver (`sf check`).
3. **Training and Fine-Tuning Pipelines**: Ready-to-use dataset generators for:
   - **Pre-training / Continued Pre-training** (30,000+ raw verified code modules)
   - **Fill-In-The-Middle (FIM)** (90,000+ pairs for sub-10ms IDE ghost-text autocomplete)
   - **Instruction-Tuning (SFT)** (30,000+ prompt-response pairs for assistant models)

---

## Repository Structure

```
salivo-ai-corpus/
├── corpus/
│   ├── 01_language_basics/        # Core language fundamentals & stream imports
│   ├── 02_collections/            # Vec<T>, HashMap<K, V>, FIFO Queue, LIFO Stack
│   ├── 03_algorithms/             # Sorting, searching, graph traversal, math
│   ├── 04_traits_and_raii/        # Trait polymorphism, impl Drop deterministic cleanup
│   ├── 05_file_io/                # Path manipulation, filesystem inspection
│   ├── 06_networking/             # TCP socket address, client/server configuration
│   ├── 07_security_and_crypto/    # SHA-256, HMAC, constant-time validation, salted hashing
│   ├── 08_backend_and_api/        # HTTP statuses, REST routing, JSON building, pipelines
│   ├── 09_frontend_and_templates/ # HTML builders, UI Cards, tables, forms, pagination
│   ├── 10_system_and_concurrency/ # Benchmarking, direct memory allocation, safe RAII blocks
│   ├── gen_dsa_sorting/           # 3,000 verified sorting algorithm variations
│   ├── gen_dsa_searching/         # 2,000 verified binary & linear search variations
│   ├── gen_dsa_dp/                # 4,000 verified DP variations (Knapsack, LCS, Sieve, Fib)
│   ├── gen_dsa_math/              # 1,000 verified 2D matrix transformation modules
│   ├── gen_math_algebra/          # 2,000 verified GCD, LCM, and fast modular power modules
│   ├── gen_math_stats/            # 1,000 verified mean, min/max, and statistical modules
│   ├── gen_security_crypto/       # 3,000 verified SHA-256, HMAC, and token bucket modules
│   ├── gen_systems_mem/           # 1,000 verified raw memory buffer allocation modules
│   ├── gen_systems_raii/          # 1,000 verified RAII Drop destructor guard modules
│   ├── gen_backend_api/           # 7,000 verified REST routers, statuses, JSON, and auth modules
│   ├── gen_frontend_ui/           # 4,000 verified HTML, Card, Table, and CSS class modules
│   └── gen_fintech_biz/           # 1,000 verified financial math & ledger modules
├── scripts/
│   ├── verify_all.py              # Automated Stage-3 compiler verification runner
│   ├── build_dataset.py           # Exports pretraining, FIM, and SFT datasets (.jsonl)
│   └── build_30k_corpus.py        # High-throughput 30k parallel synthesis & verification engine
├── datasets/                      # Exported JSONL training data
├── .gitignore
└── README.md
```

---

## Verification and Tooling

### 1. Verify Samples with the Compiler
Run the parallel compiler verification script:
```bash
python scripts/verify_all.py
```

### 2. Generate Training Datasets
Export your corpus into training formats ready for Hugging Face, PyTorch, or Unsloth:
```bash
python scripts/build_dataset.py
```

---

## Key Salivo Syntax Rules

- **Stream Header Imports (`><`)**: Imports stream directly into modules (e.g. `><salivo.std.core::{outln};`).
- **The Zero-Underscore Type Law**: Types, structs, traits, and enums strictly use `PascalCase` with no underscores (`_` is never a datatype).
- **Explicit Dynamic Arrays**: Built-in generic vector methods (`vecNew<T>()`, `push<T>(v, val)`, `veclen<T>(v)`).
- **String Interpolation**: Template syntax using `$"..."` with postfix formatters (`{val:str}`, `{val:trim:upper}`).
- **Deterministic RAII**: Resource management with `impl Drop for StructName`.
