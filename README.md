# Salivo AI Corpus

> **A curated, 100% compiler-verified dataset of 30,080 idiomatic Salivo code modules for training ultra-fast Small Language Models (SLMs) and IDE coding copilots.**

---

## Mission

General AI models frequently hallucinate when generating code in **Salivo** because it is absent from standard web-scale pre-training datasets. 

This repository solves that bottleneck by providing:
1. **Two-Tier Architecture**:
   - **Smart AI Expert Code** (`corpus/smart_ai_expert_code/`): 80 hand-crafted, high-complexity canonical modules and 5 production-grade flagship projects designed for fine-tuning existing smart models (e.g. Claude, GPT-4, Llama, DeepSeek) that already know programming logic and only need deep Salivo systems idioms.
   - **Pre-Training from Scratch** (`corpus/to_train_llm_from_scratch/`): 30,000 compiler-verified modules designed for training new models from zero on tokenization, grammar rules, and IDE code completion.
2. **Zero-Hallucination Guarantee**: Every single `.sal` file in this repository is strictly checked and validated by the official Stage-3 Salivo compiler driver (`sf check`).
3. **Training and Fine-Tuning Pipelines**: Ready-to-use dataset generators for:
   - **Smart AI Expert SFT** (`datasets/smart_ai_expert_sft.jsonl`): Clean, zero-repetition instruction dataset for high-reasoning coding models (80 verified expert modules).
   - **Pre-training / Continued Pre-training** (`datasets/pretrain_corpus.jsonl`): 30,080 raw verified code modules.
   - **Fill-In-The-Middle (FIM)** (`datasets/fim_part1.jsonl`, `datasets/fim_part2.jsonl`): 90,240 autocomplete pairs.
   - **Instruction-Tuning (SFT)** (`datasets/instruct_sft.jsonl`): 30,080 prompt-response pairs.

---

## Repository Structure

```
salivo-ai-corpus/
├── corpus/
│   ├── smart_ai_expert_code/           # For fine-tuning existing smart LLMs (Claude, GPT, Llama)
│   │   ├── 01_language_basics/         # Core language fundamentals & stream imports
│   │   ├── 02_collections/             # Vec<T>, HashMap<K, V>, FIFO Queue, LIFO Stack
│   │   ├── 03_algorithms/              # Sorting, searching, graph traversal, math
│   │   ├── 04_traits_and_raii/         # Trait polymorphism, impl Drop deterministic cleanup
│   │   ├── 05_file_io/                 # Path manipulation, filesystem inspection
│   │   ├── 06_networking/              # TCP socket address, client/server configuration
│   │   ├── 07_security_and_crypto/     # SHA-256, HMAC, constant-time validation, salted hashing
│   │   ├── 08_backend_and_api/         # HTTP statuses, REST routing, JSON building, pipelines
│   │   ├── 09_frontend_and_templates/  # HTML builders, UI Cards, tables, forms, pagination
│   │   ├── 10_system_and_concurrency/  # Benchmarking, direct memory allocation, safe RAII blocks
│   │   ├── 11_project_markdown_engine/ # Full Markdown lexer, AST parser, HTML emitter, pipeline
│   │   ├── 12_project_minidb_engine/   # In-memory SQL/KV table storage, query filter, WAL transactions
│   │   ├── 13_project_http_web_framework/ # HTTP parser, route table, middleware stack, REST controller
│   │   ├── 14_project_chess_game_engine/  # 8x8 Board state, ray move generator, material evaluator, game runner
│   │   ├── 15_project_crypto_wire_protocol/ # Frame codec, CRC16 checksum, HMAC auth, secure session state
│   │   ├── 16_advanced_trees_and_heaps/   # AVL, Segment Tree, Fenwick Tree, Min/Max-Heap, Trie, DSU, LRU, Ring Buffer
│   │   ├── 17_graph_algorithms/           # Dijkstra, BFS, Kahn Toposort, Floyd-Warshall, Bellman-Ford, Kruskal, A*
│   │   ├── 18_dynamic_programming/        # LIS O(N log N), Matrix Chain Mult, Bitmask TSP, Coin Change, LPS, Kadane
│   │   ├── 19_systems_allocators/         # Linear Arena/Bump, Slab/Pool Allocators, RAII Drop buffers, Bitboard, Bloom
│   │   ├── 20_parsers_and_strings/        # KMP, Rabin-Karp, Recursive Descent AST Parser, JSON Tokenizer, Huffman
│   │   └── 21_wire_protocols_and_crypto/  # FNV-1a, CRC32 Checksum, Binary Packet Frame Serializer, HTTP Parser
│   │
│   └── to_train_llm_from_scratch/      # 30,000+ files for vocabulary & syntax pre-training
│       ├── gen_dsa_sorting/            # 3,000 verified sorting algorithm variations
│       ├── gen_dsa_searching/          # 2,000 verified binary & linear search variations
│       ├── gen_dsa_dp/                 # 4,000 verified DP variations (Knapsack, LCS, Sieve, Fib)
│       ├── gen_dsa_trees_heaps/        # Verified AVL, Segment Tree, Fenwick, Heaps, Trie, DSU, LRU
│       ├── gen_dsa_graphs_networks/    # Verified Dijkstra, BFS, Toposort, Floyd-Warshall, Bellman-Ford, Kruskal, A*
│       ├── gen_dsa_advanced_dp/        # Verified LIS, Matrix Chain, Bitmask TSP, Coin Change, LPS, Kadane
│       ├── gen_systems_allocators/     # Verified Arena Allocator, Slab Allocator, RAII Buffers, Bitboard, Bloom
│       ├── gen_strings_parsers/        # Verified KMP, Rabin-Karp, Recursive Descent AST, JSON Tokenizer, Huffman
│       ├── gen_crypto_wire/            # Verified FNV-1a, CRC32, Packet Serializer, HTTP Request Parser
│       ├── gen_dsa_math/               # 1,000 verified 2D matrix transformation modules
│       ├── gen_math_algebra/           # 2,000 verified GCD, LCM, and fast modular power modules
│       ├── gen_math_stats/             # 1,000 verified mean, min/max, and statistical modules
│       ├── gen_security_crypto/        # 3,000 verified SHA-256, HMAC, and token bucket modules
│       ├── gen_systems_mem/            # 1,000 verified raw memory buffer allocation modules
│       ├── gen_systems_raii/           # 1,000 verified RAII Drop destructor guard modules
│       ├── gen_backend_api/            # 7,000 verified REST routers, statuses, JSON, and auth modules
│       ├── gen_frontend_ui/            # 4,000 verified HTML, Card, Table, and CSS class modules
│       └── gen_fintech_biz/            # 1,000 verified financial math & ledger modules
│
├── scripts/
│   ├── verify_all.py                   # Automated Stage-3 compiler verification runner
│   ├── build_dataset.py                # Exports pretraining, FIM, and SFT datasets (.jsonl)
│   ├── build_30k_corpus.py             # High-throughput 30k parallel synthesis & verification engine
│   ├── build_advanced_mastery_corpus.py # Advanced DSA & Systems compiler verification suite
│   └── generate_advanced_dsa_sft.py    # Teacher-level SFT dataset synthesis engine
│
├── datasets/                           # Exported JSONL training data
│   ├── cieri_advanced_dsa_sft.jsonl    # Teacher-level CoT SFT pairs for DSA, systems & allocators
│   ├── smart_ai_expert_sft.jsonl       # High-entropy dataset for fine-tuning existing smart models
│   ├── pretrain_corpus.jsonl           # 30,060+ raw files for pre-training from scratch
│   ├── fim_part1.jsonl                 # IDE ghost-text code completion (Part 1)
│   ├── fim_part2.jsonl                 # IDE ghost-text code completion (Part 2)
│   └── instruct_sft.jsonl              # Full instruction-tuning dataset
│
├── .gitignore
└── README.md
```

---

## Verification and Tooling

### 1. Verify Samples with the Compiler
Run the parallel Stage-3 compiler verification script:
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
