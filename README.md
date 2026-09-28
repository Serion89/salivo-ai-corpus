# Salivo AI Corpus

> **A curated, 100% compiler-verified dataset of idiomatic Salivo code for training ultra-fast Small Language Models (SLMs) and IDE coding copilots.**

---

## Mission

General AI models frequently hallucinate when generating code in **Salivo** because it is absent from standard web-scale pre-training datasets. 

This repository solves that bottleneck by providing:
1. **Canonical Code Corpus**: High-quality, idiomatic Salivo programs spanning fundamentals, collections, algorithms, systems programming, traits, networking, security, backend APIs, frontend templates, and memory management.
2. **Zero-Hallucination Guarantee**: Every single `.sal` file in this repository is strictly compiled and executed natively by the official Salivo Stage 3 Self-Hosted Compiler (`sf run --compiler stage3`).
3. **Training and Fine-Tuning Pipelines**: Ready-to-use dataset generators for:
   - **Pre-training / Continued Pre-training** (raw verified code)
   - **Fill-In-The-Middle (FIM)** (for sub-10ms IDE ghost-text autocomplete)
   - **Instruction-Tuning (SFT)** (prompt-response pairs for assistant models)

---

## Repository Structure

```
salivo-ai-corpus/
├── corpus/
│   ├── 01_language_basics/        # Stream headers (><), types, control flow, interpolation
│   ├── 02_collections/            # Vec<T>, Map<K, V>, FIFO Queue, LIFO Stack
│   ├── 03_algorithms/             # Bubble sort, Selection sort, Insertion sort, Binary search, Sieve, Fast power
│   ├── 04_traits_and_raii/        # Trait polymorphism, impl Drop deterministic cleanup
│   ├── 05_file_io/                # Path manipulation, filesystem inspection
│   ├── 06_networking/             # TCP socket address, client/server configuration
│   ├── 07_security_and_crypto/    # SHA-256 digests, HMAC authentication, constant-time verification, salted hashing
│   ├── 08_backend_and_api/        # HTTP status taxonomy, REST routing, JSON building, middleware pipelines
│   ├── 09_frontend_and_templates/ # HTML builders, UI Card components, table rendering, CSS class utilities
│   └── 10_system_and_concurrency/ # Benchmarking, direct memory allocation (allocate/deallocate), safe RAII memory blocks
├── scripts/
│   ├── verify_all.py              # Automated Stage-3 compiler verification runner (sf run --compiler stage3)
│   └── build_dataset.py           # Exports pretraining, FIM, and SFT datasets (.jsonl)
├── datasets/                      # Exported JSONL training data
├── .gitignore
└── README.md
```

---

## Verification and Tooling

### 1. Verify All Samples with the Stage 3 Compiler
Run the automated verification script to ensure every file compiles and runs under the Stage 3 self-hosted compiler with zero fallback:
```bash
python scripts/verify_all.py
```

### 2. Run an Individual Sample
```bash
sf run --compiler stage3 corpus/01_language_basics/01_hello.sal
```

### 3. Generate Training Datasets
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
