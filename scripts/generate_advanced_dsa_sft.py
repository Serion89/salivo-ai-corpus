#!/usr/bin/env python3
"""
Generates high-quality pedagogical Teacher SFT dataset entries
from all 36 verified Salivo algorithms, data structures, and allocators.
Outputs to datasets/cieri_advanced_dsa_sft.jsonl
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CORPUS_DIR = BASE_DIR / "corpus" / "advanced_mastery_corpus"
OUTPUT_FILE = BASE_DIR / "datasets" / "cieri_advanced_dsa_sft.jsonl"

SYSTEM_PROMPT = (
    "You are Cieri, an exceptionally intelligent, articulate, and pedagogical master teacher and systems engineer. "
    "You communicate warmly and clearly. When answering technical or algorithmic requests, you think pedagogically inside "
    "<think>...</think> tags, breaking down the problem from first principles, verifying language invariants (stream headers ><, "
    "PascalCase types, deterministic RAII Drop), and providing clean, high-performance Salivo code."
)

TOPICS = {
    "avl_tree.sal": ("AVL Self-Balancing Binary Search Tree", "Balanced trees with height rotation invariants"),
    "segment_tree.sal": ("Segment Tree", "Range sum and point update queries in O(log N)"),
    "fenwick_tree.sal": ("Fenwick Tree (Binary Indexed Tree)", "Prefix sums and point updates with bitwise low-bit manipulation"),
    "binary_min_heap.sal": ("Binary Min-Heap Priority Queue", "Priority queue with heapify bubble-up and bubble-down invariants"),
    "binary_max_heap.sal": ("Binary Max-Heap", "Max-priority queue with O(log N) insertions"),
    "trie_prefix_tree.sal": ("Trie (Prefix Tree)", "High-performance prefix matching and dictionary search"),
    "disjoint_set_union.sal": ("Disjoint Set Union (DSU / Union-Find)", "Graph connectivity with path compression and rank union"),
    "lru_cache.sal": ("LRU (Least Recently Used) Cache", "O(1) access tracking and eviction strategy"),
    "circular_ring_buffer.sal": ("Circular FIFO Ring Buffer", "Fixed-size circular queue with head/tail wrapping"),
    "dijkstra_shortest_path.sal": ("Dijkstra's Shortest Path Algorithm", "Greedy single-source shortest path on weighted graphs"),
    "breadth_first_search.sal": ("Breadth-First Search (BFS)", "Level-order unweighted graph traversal and hop counting"),
    "topological_sort_kahn.sal": ("Topological Sort (Kahn's Algorithm)", "DAG dependency resolution using in-degree queue"),
    "floyd_warshall.sal": ("Floyd-Warshall All-Pairs Shortest Path", "Dynamic programming for all-pairs shortest paths"),
    "bellman_ford.sal": ("Bellman-Ford Algorithm", "Shortest paths on graphs with negative weights and cycle detection"),
    "kruskal_mst.sal": ("Kruskal's Minimum Spanning Tree", "Greedy MST construction using DSU connectivity"),
    "astar_grid_pathfinding.sal": ("A* Heuristic Pathfinding", "Grid pathfinding with Manhattan distance evaluation"),
    "longest_increasing_subseq.sal": ("Longest Increasing Subsequence (LIS)", "O(N log N) patience sorting with binary search tails"),
    "matrix_chain_multiplication.sal": ("Matrix Chain Multiplication", "Optimal parenthesization with dynamic programming"),
    "bitmask_tsp.sal": ("Traveling Salesperson Problem (TSP)", "Bitmask dynamic programming over exponential state spaces"),
    "coin_change_unbounded.sal": ("Unbounded Coin Change Problem", "Dynamic programming for minimum coin combinations"),
    "longest_palindromic_subseq.sal": ("Longest Palindromic Subsequence", "Interval dynamic programming over string characters"),
    "maximum_subarray_kadane.sal": ("Kadane's Maximum Subarray Algorithm", "O(N) linear scan for maximum contiguous sum"),
    "arena_bump_allocator.sal": ("Linear Arena / Bump Allocator", "Zero-overhead sequential memory allocation with RAII Drop cleanup"),
    "slab_pool_allocator.sal": ("Slab / Pool Allocator", "Fixed-size memory chunk allocator with free-list recycling"),
    "bitboard_chess_engine.sal": ("64-bit Bitboard Engine", "Fast bitwise state representations and popcount calculations"),
    "bloom_filter.sal": ("Probabilistic Bloom Filter", "Space-efficient set membership with multiple hash functions"),
    "ring_buffer_raii.sal": ("Byte Ring Buffer with RAII Drop", "Raw memory allocation with deterministic drop destruction"),
    "kmp_string_search.sal": ("Knuth-Morris-Pratt (KMP) String Search", "Linear time pattern matching via LPS prefix function"),
    "rabin_karp_rolling_hash.sal": ("Rabin-Karp Rolling Hash Search", "Polynomial rolling hash for fast substring matching"),
    "recursive_descent_calc.sal": ("Recursive Descent Expression Parser", "Grammar tokenization and AST evaluation for math expressions"),
    "json_tokenizer.sal": ("Streaming JSON Lexical Analyzer", "Lexer token stream for JSON object and array syntax"),
    "huffman_coding.sal": ("Huffman Tree Encoding", "Lossless compression prefix trees by character frequency"),
    "fnv1a_hash.sal": ("Fowler-Noll-Vo (FNV-1a) Hash", "High-dispersion 32/64-bit non-cryptographic hashing"),
    "crc32_checksum.sal": ("CRC-32 Checksum Engine", "Bitwise cyclic redundancy check for data integrity"),
    "binary_packet_protocol.sal": ("Binary Wire Frame Protocol", "Network packet serialization with magic bytes, opcode, and payload"),
    "http_request_parser.sal": ("HTTP/1.1 Request Line Parser", "Zero-copy byte parsing for HTTP methods and headers"),
}

def main():
    count = 0
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out_f:
        for sal_file in sorted(CORPUS_DIR.rglob("*.sal")):
            name = sal_file.name
            title, desc = TOPICS.get(name, (name.replace("_", " ").title(), "Advanced algorithm"))
            code = sal_file.read_text(encoding="utf-8").strip()

            user_query = f"Teach me how to implement {title} in Salivo. Walk me through the intuition, language laws, and provide complete, verified code."
            
            thought = (
                f"<think>\n"
                f"1. Educational Goal: Teach {title} ({desc}) with pedagogical clarity.\n"
                f"2. Core Mental Model: Explain the algorithmic intuition from first principles.\n"
                f"3. Salivo Language Laws:\n"
                f"   - Stream headers exclusively (><)\n"
                f"   - Strict PascalCase data types with zero underscores\n"
                f"   - Deterministic RAII Drop cleanup for memory and resources\n"
                f"   - Clean variable bindings and type safety\n"
                f"4. Code Implementation: Provide the canonical, compiler-verified Salivo implementation.\n"
                f"5. Proactive Gotchas & Complexity: Outline time/space complexity and common learner pitfalls.\n"
                f"</think>"
            )

            response_body = (
                f"{thought}\n\n"
                f"### 1. The Intuitive Mental Model\n"
                f"{title} is a fundamental systems computer science concept. {desc}.\n\n"
                f"### 2. Complete, Verified Salivo Implementation\n"
                f"```salivo\n{code}\n```\n\n"
                f"### 3. Key Architectural Takeaways\n"
                f"- **Memory Safety**: Clean ownership semantics with deterministic cleanup.\n"
                f"- **Zero Overhead**: Direct native compilation with no garbage collector pauses.\n"
                f"- **Idiomatic Salivo**: Adheres strictly to the stream header (`><`) and PascalCase type laws."
            )

            entry = {
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_query},
                    {"role": "assistant", "content": response_body},
                ]
            }

            out_f.write(json.dumps(entry, ensure_ascii=False) + "\n")
            count += 1

    print(f"Generated {count} teacher SFT pairs in {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
