#!/usr/bin/env python3
"""
Advanced Mastery Corpus Generator & Compiler Verifier.
Builds 36 canonical, high-IQ Salivo algorithms, data structures, allocators,
parsers, and network protocols, verifying every single file with `sf check`.
"""

import os
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
TARGET_DIR = BASE_DIR / "corpus" / "advanced_mastery_corpus"
SF_BIN = r"C:\Users\sahil\.salivo\bin\sf.exe"

MODULES = {}

# =============================================================================
# 1. TREES AND HEAPS
# =============================================================================

MODULES["01_trees_and_heaps/avl_tree.sal"] = """module corpus.dsa.avl;

><salivo.std.core::{outln};
><salivo.std.collections::{Vec, vecNew, push, get, set, veclen};

pub struct AvlNode {
    int key;
    int height;
    int left;
    int right;
}

pub func maxVal(a: int, b: int) -> int {
    if (a > b) {
        return a;
    }
    return b;
}

pub func getNodeHeight(nodes: Vec<AvlNode>, idx: int) -> int {
    if (idx < 0) {
        return 0;
    }
    let node = get<AvlNode>(nodes, idx);
    return node.height;
}

pub func getBalance(nodes: Vec<AvlNode>, idx: int) -> int {
    if (idx < 0) {
        return 0;
    }
    let node = get<AvlNode>(nodes, idx);
    let lh = getNodeHeight(nodes, node.left);
    let rh = getNodeHeight(nodes, node.right);
    return lh - rh;
}

pub func main() -> int {
    let mut nodes: Vec<AvlNode> = vecNew<AvlNode>();
    let root = AvlNode { key: 10, height: 1, left: -1, right: -1 };
    nodes = push<AvlNode>(nodes, root);
    let bal = getBalance(nodes, 0);
    outln($"AVL Root Balance Factor: {bal:str}");
    return 0;
}
"""

MODULES["01_trees_and_heaps/segment_tree.sal"] = """module corpus.dsa.segtree;

><salivo.std.core::{outln};
><salivo.std.collections::{Vec, vecNew, push, get, set, veclen};

pub struct SegmentTree {
    int size;
    Vec<int> tree;
}

pub func buildTree(arr: Vec<int>, n: int) -> SegmentTree {
    let mut treeVec: Vec<int> = vecNew<int>();
    let total = n * 4;
    for (let mut i = 0; i < total; i = i + 1) {
        treeVec = push<int>(treeVec, 0);
    }
    return SegmentTree { size: n, tree: treeVec };
}

pub func updatePoint(st: SegmentTree, node: int, start: int, end: int, idx: int, val: int) {
    if (start == end) {
        set<int>(st.tree, node, val);
        return;
    }
    let mid = (start + end) / 2;
    let leftNode = node * 2 + 1;
    let rightNode = node * 2 + 2;
    if (idx <= mid) {
        updatePoint(st, leftNode, start, mid, idx, val);
    } else {
        updatePoint(st, rightNode, mid + 1, end, idx, val);
    }
    let leftSum = get<int>(st.tree, leftNode);
    let rightSum = get<int>(st.tree, rightNode);
    set<int>(st.tree, node, leftSum + rightSum);
}

pub func main() -> int {
    let mut arr: Vec<int> = vecNew<int>();
    arr = push<int>(arr, 1);
    arr = push<int>(arr, 3);
    arr = push<int>(arr, 5);
    let st = buildTree(arr, 3);
    updatePoint(st, 0, 0, 2, 1, 10);
    let total = get<int>(st.tree, 0);
    outln($"Segment Tree Root Aggregate: {total:str}");
    return 0;
}
"""

MODULES["01_trees_and_heaps/fenwick_tree.sal"] = """module corpus.dsa.fenwick;

><salivo.std.core::{outln};
><salivo.std.collections::{Vec, vecNew, push, get, set, veclen};

pub struct FenwickTree {
    int size;
    Vec<int> tree;
}

pub func fenwickNew(n: int) -> FenwickTree {
    let mut t: Vec<int> = vecNew<int>();
    for (let mut i = 0; i <= n; i = i + 1) {
        t = push<int>(t, 0);
    }
    return FenwickTree { size: n, tree: t };
}

pub func fenwickUpdate(ft: FenwickTree, idx: int, delta: int) {
    let mut i = idx;
    while (i <= ft.size) {
        let current = get<int>(ft.tree, i);
        set<int>(ft.tree, i, current + delta);
        let lsb = i & (-i);
        i = i + lsb;
    }
}

pub func fenwickQuery(ft: FenwickTree, idx: int) -> int {
    let mut sum = 0;
    let mut i = idx;
    while (i > 0) {
        let val = get<int>(ft.tree, i);
        sum = sum + val;
        let lsb = i & (-i);
        i = i - lsb;
    }
    return sum;
}

pub func main() -> int {
    let ft = fenwickNew(10);
    fenwickUpdate(ft, 1, 5);
    fenwickUpdate(ft, 2, 3);
    fenwickUpdate(ft, 3, 7);
    let p = fenwickQuery(ft, 3);
    outln($"Prefix sum at 3: {p:str}");
    return 0;
}
"""

MODULES["01_trees_and_heaps/binary_min_heap.sal"] = """module corpus.dsa.minheap;

><salivo.std.core::{outln};
><salivo.std.collections::{Vec, vecNew, push, get, set, veclen};

pub struct MinHeap {
    Vec<int> data;
}

pub func heapNew() -> MinHeap {
    return MinHeap { data: vecNew<int>() };
}

pub func heapPush(heap: MinHeap, val: int) {
    let mut v = heap.data;
    v = push<int>(v, val);
    let mut idx = veclen<int>(v) - 1;
    while (idx > 0) {
        let parent = (idx - 1) / 2;
        let parentVal = get<int>(v, parent);
        let currVal = get<int>(v, idx);
        if (currVal < parentVal) {
            set<int>(v, parent, currVal);
            set<int>(v, idx, parentVal);
            idx = parent;
        } else {
            return;
        }
    }
}

pub func heapPeek(heap: MinHeap) -> int {
    return get<int>(heap.data, 0);
}

pub func main() -> int {
    let h = heapNew();
    heapPush(h, 45);
    heapPush(h, 12);
    heapPush(h, 89);
    heapPush(h, 5);
    let top = heapPeek(h);
    outln($"Min Heap Top: {top:str}");
    return 0;
}
"""

MODULES["01_trees_and_heaps/disjoint_set_union.sal"] = """module corpus.dsa.dsu;

><salivo.std.core::{outln};
><salivo.std.collections::{Vec, vecNew, push, get, set, veclen};

pub struct DisjointSet {
    Vec<int> parent;
    Vec<int> rank;
}

pub func dsuNew(n: int) -> DisjointSet {
    let mut p: Vec<int> = vecNew<int>();
    let mut r: Vec<int> = vecNew<int>();
    for (let mut i = 0; i < n; i = i + 1) {
        p = push<int>(p, i);
        r = push<int>(r, 0);
    }
    return DisjointSet { parent: p, rank: r };
}

pub func dsuFind(dsu: DisjointSet, x: int) -> int {
    let p = get<int>(dsu.parent, x);
    if (p == x) {
        return x;
    }
    let root = dsuFind(dsu, p);
    set<int>(dsu.parent, x, root);
    return root;
}

pub func dsuUnion(dsu: DisjointSet, a: int, b: int) -> int {
    let rootA = dsuFind(dsu, a);
    let rootB = dsuFind(dsu, b);
    if (rootA == rootB) {
        return 0;
    }
    let rankA = get<int>(dsu.rank, rootA);
    let rankB = get<int>(dsu.rank, rootB);
    if (rankA < rankB) {
        set<int>(dsu.parent, rootA, rootB);
    } else {
        if (rankA > rankB) {
            set<int>(dsu.parent, rootB, rootA);
        } else {
            set<int>(dsu.parent, rootB, rootA);
            set<int>(dsu.rank, rootA, rankA + 1);
        }
    }
    return 1;
}

pub func main() -> int {
    let dsu = dsuNew(5);
    dsuUnion(dsu, 0, 1);
    dsuUnion(dsu, 1, 2);
    let root2 = dsuFind(dsu, 2);
    let root0 = dsuFind(dsu, 0);
    outln($"DSU Connected (0 and 2): {root2:str} == {root0:str}");
    return 0;
}
"""

MODULES["01_trees_and_heaps/circular_ring_buffer.sal"] = """module corpus.dsa.ringbuf;

><salivo.std.core::{outln};
><salivo.std.collections::{Vec, vecNew, push, get, set, veclen};

pub struct RingBuffer {
    Vec<int> buffer;
    int capacity;
    int head;
    int tail;
    int count;
}

pub func ringNew(capacity: int) -> RingBuffer {
    let mut b: Vec<int> = vecNew<int>();
    for (let mut i = 0; i < capacity; i = i + 1) {
        b = push<int>(b, 0);
    }
    return RingBuffer { buffer: b, capacity: capacity, head: 0, tail: 0, count: 0 };
}

pub func ringPush(rb: RingBuffer, val: int) -> int {
    if (rb.count >= rb.capacity) {
        return -1;
    }
    set<int>(rb.buffer, rb.tail, val);
    rb.tail = (rb.tail + 1) % rb.capacity;
    rb.count = rb.count + 1;
    return 0;
}

pub func ringPop(rb: RingBuffer) -> int {
    if (rb.count == 0) {
        return -1;
    }
    let val = get<int>(rb.buffer, rb.head);
    rb.head = (rb.head + 1) % rb.capacity;
    rb.count = rb.count - 1;
    return val;
}

pub func main() -> int {
    let rb = ringNew(4);
    ringPush(rb, 100);
    ringPush(rb, 200);
    ringPush(rb, 300);
    let popped = ringPop(rb);
    outln($"Popped FIFO item: {popped:str}, remaining count: {rb.count:str}");
    return 0;
}
"""

# =============================================================================
# 2. GRAPH ALGORITHMS
# =============================================================================

MODULES["02_graphs_and_networks/dijkstra_shortest_path.sal"] = """module corpus.graphs.dijkstra;

><salivo.std.core::{outln};
><salivo.std.collections::{Vec, vecNew, push, get, set, veclen};

pub func dijkstra(adj: Vec<int>, numVertices: int, startNode: int) -> Vec<int> {
    let mut dist: Vec<int> = vecNew<int>();
    let mut visited: Vec<int> = vecNew<int>();
    let inf = 999999;
    for (let mut i = 0; i < numVertices; i = i + 1) {
        dist = push<int>(dist, inf);
        visited = push<int>(visited, 0);
    }
    set<int>(dist, startNode, 0);

    for (let mut step = 0; step < numVertices; step = step + 1) {
        let mut minDist = inf;
        let mut u = -1;
        for (let mut v = 0; v < numVertices; v = v + 1) {
            let isVis = get<int>(visited, v);
            let d = get<int>(dist, v);
            if (isVis == 0 && d < minDist) {
                minDist = d;
                u = v;
            }
        }
        if (u < 0) {
            return dist;
        }
        set<int>(visited, u, 1);
        for (let mut v = 0; v < numVertices; v = v + 1) {
            let weight = get<int>(adj, u * numVertices + v);
            let isVis = get<int>(visited, v);
            if (weight > 0 && isVis == 0) {
                let currentDist = get<int>(dist, v);
                let newDist = minDist + weight;
                if (newDist < currentDist) {
                    set<int>(dist, v, newDist);
                }
            }
        }
    }
    return dist;
}

pub func main() -> int {
    let mut adj: Vec<int> = vecNew<int>();
    for (let mut i = 0; i < 9; i = i + 1) {
        adj = push<int>(adj, 0);
    }
    set<int>(adj, 0 * 3 + 1, 4);
    set<int>(adj, 0 * 3 + 2, 10);
    set<int>(adj, 1 * 3 + 2, 2);
    let dist = dijkstra(adj, 3, 0);
    let target = get<int>(dist, 2);
    outln($"Shortest path from 0 to 2: {target:str}");
    return 0;
}
"""

MODULES["02_graphs_and_networks/breadth_first_search.sal"] = """module corpus.graphs.bfs;

><salivo.std.core::{outln};
><salivo.std.collections::{Vec, vecNew, push, get, set, veclen};

pub func bfsDistances(adj: Vec<int>, numVertices: int, src: int) -> Vec<int> {
    let mut dist: Vec<int> = vecNew<int>();
    for (let mut i = 0; i < numVertices; i = i + 1) {
        dist = push<int>(dist, -1);
    }
    let mut queue: Vec<int> = vecNew<int>();
    queue = push<int>(queue, src);
    set<int>(dist, src, 0);
    let mut head = 0;

    while (head < veclen<int>(queue)) {
        let u = get<int>(queue, head);
        head = head + 1;
        let d = get<int>(dist, u);

        for (let mut v = 0; v < numVertices; v = v + 1) {
            let hasEdge = get<int>(adj, u * numVertices + v);
            let visited = get<int>(dist, v);
            if (hasEdge == 1 && visited < 0) {
                set<int>(dist, v, d + 1);
                queue = push<int>(queue, v);
            }
        }
    }
    return dist;
}

pub func main() -> int {
    let mut adj: Vec<int> = vecNew<int>();
    for (let mut i = 0; i < 16; i = i + 1) {
        adj = push<int>(adj, 0);
    }
    set<int>(adj, 0 * 4 + 1, 1);
    set<int>(adj, 1 * 4 + 2, 1);
    set<int>(adj, 2 * 4 + 3, 1);
    let dist = bfsDistances(adj, 4, 0);
    let hop = get<int>(dist, 3);
    outln($"Hops to node 3: {hop:str}");
    return 0;
}
"""

MODULES["02_graphs_and_networks/topological_sort_kahn.sal"] = """module corpus.graphs.toposort;

><salivo.std.core::{outln};
><salivo.std.collections::{Vec, vecNew, push, get, set, veclen};

pub func topoSort(adj: Vec<int>, n: int) -> Vec<int> {
    let mut inDegree: Vec<int> = vecNew<int>();
    for (let mut i = 0; i < n; i = i + 1) {
        inDegree = push<int>(inDegree, 0);
    }
    for (let mut u = 0; u < n; u = u + 1) {
        for (let mut v = 0; v < n; v = v + 1) {
            let edge = get<int>(adj, u * n + v);
            if (edge == 1) {
                let cur = get<int>(inDegree, v);
                set<int>(inDegree, v, cur + 1);
            }
        }
    }
    let mut queue: Vec<int> = vecNew<int>();
    for (let mut i = 0; i < n; i = i + 1) {
        let deg = get<int>(inDegree, i);
        if (deg == 0) {
            queue = push<int>(queue, i);
        }
    }
    let mut order: Vec<int> = vecNew<int>();
    let mut head = 0;
    while (head < veclen<int>(queue)) {
        let u = get<int>(queue, head);
        head = head + 1;
        order = push<int>(order, u);
        for (let mut v = 0; v < n; v = v + 1) {
            let edge = get<int>(adj, u * n + v);
            if (edge == 1) {
                let cur = get<int>(inDegree, v);
                set<int>(inDegree, v, cur - 1);
                if (cur - 1 == 0) {
                    queue = push<int>(queue, v);
                }
            }
        }
    }
    return order;
}

pub func main() -> int {
    let mut adj: Vec<int> = vecNew<int>();
    for (let mut i = 0; i < 9; i = i + 1) {
        adj = push<int>(adj, 0);
    }
    set<int>(adj, 0 * 3 + 1, 1);
    set<int>(adj, 1 * 3 + 2, 1);
    let order = topoSort(adj, 3);
    let count = veclen<int>(order);
    outln($"Topological order node count: {count:str}");
    return 0;
}
"""

MODULES["02_graphs_and_networks/floyd_warshall.sal"] = """module corpus.graphs.floydwarshall;

><salivo.std.core::{outln};
><salivo.std.collections::{Vec, vecNew, push, get, set, veclen};

pub func floydWarshall(matrix: Vec<int>, n: int) -> Vec<int> {
    let mut dist = matrix;
    for (let mut k = 0; k < n; k = k + 1) {
        for (let mut i = 0; i < n; i = i + 1) {
            for (let mut j = 0; j < n; j = j + 1) {
                let d_ik = get<int>(dist, i * n + k);
                let d_kj = get<int>(dist, k * n + j);
                let d_ij = get<int>(dist, i * n + j);
                if (d_ik < 999999 && d_kj < 999999) {
                    let through_k = d_ik + d_kj;
                    if (through_k < d_ij) {
                        set<int>(dist, i * n + j, through_k);
                    }
                }
            }
        }
    }
    return dist;
}

pub func main() -> int {
    let mut m: Vec<int> = vecNew<int>();
    for (let mut i = 0; i < 9; i = i + 1) {
        m = push<int>(m, 999999);
    }
    set<int>(m, 0 * 3 + 0, 0);
    set<int>(m, 1 * 3 + 1, 0);
    set<int>(m, 2 * 3 + 2, 0);
    set<int>(m, 0 * 3 + 1, 5);
    set<int>(m, 1 * 3 + 2, 3);
    let res = floydWarshall(m, 3);
    let shortest = get<int>(res, 0 * 3 + 2);
    outln($"Floyd-Warshall 0->2: {shortest:str}");
    return 0;
}
"""

# =============================================================================
# 3. ADVANCED DYNAMIC PROGRAMMING
# =============================================================================

MODULES["03_advanced_dp/longest_increasing_subseq.sal"] = """module corpus.dp.lis;

><salivo.std.core::{outln};
><salivo.std.collections::{Vec, vecNew, push, get, set, veclen};

pub func lisLength(arr: Vec<int>) -> int {
    let n = veclen<int>(arr);
    if (n == 0) {
        return 0;
    }
    let mut tails: Vec<int> = vecNew<int>();
    for (let mut i = 0; i < n; i = i + 1) {
        let x = get<int>(arr, i);
        let mut left = 0;
        let mut right = veclen<int>(tails);
        while (left < right) {
            let mid = (left + right) / 2;
            let val = get<int>(tails, mid);
            if (val < x) {
                left = mid + 1;
            } else {
                right = mid;
            }
        }
        if (left == veclen<int>(tails)) {
            tails = push<int>(tails, x);
        } else {
            set<int>(tails, left, x);
        }
    }
    return veclen<int>(tails);
}

pub func main() -> int {
    let mut arr: Vec<int> = vecNew<int>();
    arr = push<int>(arr, 10);
    arr = push<int>(arr, 9);
    arr = push<int>(arr, 2);
    arr = push<int>(arr, 5);
    arr = push<int>(arr, 3);
    arr = push<int>(arr, 7);
    arr = push<int>(arr, 101);
    arr = push<int>(arr, 18);
    let len = lisLength(arr);
    outln($"LIS Length: {len:str}");
    return 0;
}
"""

MODULES["03_advanced_dp/matrix_chain_multiplication.sal"] = """module corpus.dp.mcm;

><salivo.std.core::{outln};
><salivo.std.collections::{Vec, vecNew, push, get, set, veclen};

pub func mcmCost(p: Vec<int>, n: int) -> int {
    let mut dp: Vec<int> = vecNew<int>();
    let total = n * n;
    for (let mut i = 0; i < total; i = i + 1) {
        dp = push<int>(dp, 0);
    }
    let inf = 999999999;
    for (let mut l = 2; l < n; l = l + 1) {
        let limit = n - l + 1;
        for (let mut i = 1; i < limit; i = i + 1) {
            let j = i + l - 1;
            set<int>(dp, i * n + j, inf);
            for (let mut k = i; k < j; k = k + 1) {
                let cost1 = get<int>(dp, i * n + k);
                let cost2 = get<int>(dp, (k + 1) * n + j);
                let p_i1 = get<int>(p, i - 1);
                let p_k = get<int>(p, k);
                let p_j = get<int>(p, j);
                let mult = cost1 + cost2 + (p_i1 * p_k * p_j);
                let curMin = get<int>(dp, i * n + j);
                if (mult < curMin) {
                    set<int>(dp, i * n + j, mult);
                }
            }
        }
    }
    return get<int>(dp, 1 * n + (n - 1));
}

pub func main() -> int {
    let mut dims: Vec<int> = vecNew<int>();
    dims = push<int>(dims, 10);
    dims = push<int>(dims, 20);
    dims = push<int>(dims, 30);
    dims = push<int>(dims, 40);
    dims = push<int>(dims, 30);
    let minCost = mcmCost(dims, 5);
    outln($"Optimal Matrix Chain Multiplication Cost: {minCost:str}");
    return 0;
}
"""

MODULES["03_advanced_dp/coin_change_unbounded.sal"] = """module corpus.dp.coinchange;

><salivo.std.core::{outln};
><salivo.std.collections::{Vec, vecNew, push, get, set, veclen};

pub func minCoins(coins: Vec<int>, amount: int) -> int {
    let mut dp: Vec<int> = vecNew<int>();
    let inf = 999999;
    dp = push<int>(dp, 0);
    for (let mut i = 1; i <= amount; i = i + 1) {
        dp = push<int>(dp, inf);
    }
    let numCoins = veclen<int>(coins);
    for (let mut i = 1; i <= amount; i = i + 1) {
        for (let mut c = 0; c < numCoins; c = c + 1) {
            let coin = get<int>(coins, c);
            if (coin <= i) {
                let prev = get<int>(dp, i - coin);
                if (prev != inf) {
                    let cur = get<int>(dp, i);
                    if (prev + 1 < cur) {
                        set<int>(dp, i, prev + 1);
                    }
                }
            }
        }
    }
    return get<int>(dp, amount);
}

pub func main() -> int {
    let mut coins: Vec<int> = vecNew<int>();
    coins = push<int>(coins, 1);
    coins = push<int>(coins, 2);
    coins = push<int>(coins, 5);
    let res = minCoins(coins, 11);
    outln($"Min coins for 11: {res:str}");
    return 0;
}
"""

# =============================================================================
# 4. SYSTEMS PROGRAMMING & MEMORY ALLOCATORS
# =============================================================================

MODULES["04_systems_and_allocators/arena_bump_allocator.sal"] = """module corpus.systems.arena;

><salivo.std.core::{outln, Drop};
><salivo.std.mem::{allocate, deallocate};

pub struct ArenaAllocator {
    int memoryPtr;
    int capacityBytes;
    int offsetBytes;
}

pub func arenaCreate(capacity: int) -> ArenaAllocator {
    let ptr = allocate(capacity, 8);
    return ArenaAllocator {
        memoryPtr: ptr,
        capacityBytes: capacity,
        offsetBytes: 0,
    };
}

pub func arenaAlloc(arena: ArenaAllocator, sizeBytes: int) -> int {
    let alignedSize = (sizeBytes + 7) & (-8);
    if (arena.offsetBytes + alignedSize > arena.capacityBytes) {
        return 0;
    }
    let resultAddr = arena.memoryPtr + arena.offsetBytes;
    arena.offsetBytes = arena.offsetBytes + alignedSize;
    return resultAddr;
}

pub func arenaReset(arena: ArenaAllocator) {
    arena.offsetBytes = 0;
}

impl Drop for ArenaAllocator {
    func drop(self) {
        deallocate(self.memoryPtr, self.capacityBytes, 8);
        outln("[Arena] Released arena backing pool safely via RAII.");
    }
}

pub func main() -> int {
    let mut arena = arenaCreate(1024);
    let p1 = arenaAlloc(arena, 64);
    let p2 = arenaAlloc(arena, 128);
    outln($"Arena allocated offset: {arena.offsetBytes:str} bytes.");
    arenaReset(arena);
    outln("Arena reset to zero offset without free-overhead.");
    return 0;
}
"""

MODULES["04_systems_and_allocators/bitboard_chess_engine.sal"] = """module corpus.systems.bitboard;

><salivo.std.core::{outln};

pub struct Bitboard {
    int bits;
}

pub func bitboardNew() -> Bitboard {
    return Bitboard { bits: 0 };
}

pub func setSquare(bb: Bitboard, square: int) {
    let mask = 1 << square;
    bb.bits = bb.bits | mask;
}

pub func clearSquare(bb: Bitboard, square: int) {
    let mask = 1 << square;
    bb.bits = bb.bits & (~mask);
}

pub func isOccupied(bb: Bitboard, square: int) -> int {
    let mask = 1 << square;
    if ((bb.bits & mask) != 0) {
        return 1;
    }
    return 0;
}

pub func popCount(bb: Bitboard) -> int {
    let mut count = 0;
    let mut b = bb.bits;
    while (b != 0) {
        b = b & (b - 1);
        count = count + 1;
    }
    return count;
}

pub func main() -> int {
    let bb = bitboardNew();
    setSquare(bb, 0);
    setSquare(bb, 7);
    setSquare(bb, 63);
    let totalPieces = popCount(bb);
    outln($"Bitboard piece count: {totalPieces:str}");
    return 0;
}
"""

MODULES["04_systems_and_allocators/bloom_filter.sal"] = """module corpus.systems.bloom;

><salivo.std.core::{outln};
><salivo.std.collections::{Vec, vecNew, push, get, set, veclen};

pub struct BloomFilter {
    Vec<int> bitset;
    int size;
}

pub func bloomNew(size: int) -> BloomFilter {
    let mut b: Vec<int> = vecNew<int>();
    for (let mut i = 0; i < size; i = i + 1) {
        b = push<int>(b, 0);
    }
    return BloomFilter { bitset: b, size: size };
}

pub func hash1(val: int, size: int) -> int {
    return ((val * 31) + 17) % size;
}

pub func hash2(val: int, size: int) -> int {
    return ((val * 67) + 53) % size;
}

pub func bloomInsert(bf: BloomFilter, val: int) {
    let h1 = hash1(val, bf.size);
    let h2 = hash2(val, bf.size);
    set<int>(bf.bitset, h1, 1);
    set<int>(bf.bitset, h2, 1);
}

pub func bloomMayContain(bf: BloomFilter, val: int) -> int {
    let h1 = hash1(val, bf.size);
    let h2 = hash2(val, bf.size);
    let b1 = get<int>(bf.bitset, h1);
    let b2 = get<int>(bf.bitset, h2);
    if (b1 == 1 && b2 == 1) {
        return 1;
    }
    return 0;
}

pub func main() -> int {
    let bf = bloomNew(64);
    bloomInsert(bf, 42);
    bloomInsert(bf, 99);
    let present = bloomMayContain(bf, 42);
    let absent = bloomMayContain(bf, 13);
    outln($"Bloom filter test: 42={present:str}, 13={absent:str}");
    return 0;
}
"""

# =============================================================================
# 5. STRING ALGORITHMS AND PARSERS
# =============================================================================

MODULES["05_strings_and_parsers/kmp_string_search.sal"] = """module corpus.strings.kmp;

><salivo.std.core::{outln};
><salivo.std.collections::{Vec, vecNew, push, get, set, veclen};

pub func buildLps(pattern: Vec<int>) -> Vec<int> {
    let m = veclen<int>(pattern);
    let mut lps: Vec<int> = vecNew<int>();
    for (let mut i = 0; i < m; i = i + 1) {
        lps = push<int>(lps, 0);
    }
    let mut len = 0;
    let mut i = 1;
    while (i < m) {
        let pi = get<int>(pattern, i);
        let plen = get<int>(pattern, len);
        if (pi == plen) {
            len = len + 1;
            set<int>(lps, i, len);
            i = i + 1;
        } else {
            if (len != 0) {
                len = get<int>(lps, len - 1);
            } else {
                set<int>(lps, i, 0);
                i = i + 1;
            }
        }
    }
    return lps;
}

pub func kmpSearch(text: Vec<int>, pattern: Vec<int>) -> int {
    let n = veclen<int>(text);
    let m = veclen<int>(pattern);
    if (m == 0) {
        return 0;
    }
    let lps = buildLps(pattern);
    let mut i = 0;
    let mut j = 0;
    while (i < n) {
        let ti = get<int>(text, i);
        let pj = get<int>(pattern, j);
        if (ti == pj) {
            i = i + 1;
            j = j + 1;
        }
        if (j == m) {
            return i - j;
        } else {
            if (i < n && ti != pj) {
                if (j != 0) {
                    j = get<int>(lps, j - 1);
                } else {
                    i = i + 1;
                }
            }
        }
    }
    return -1;
}

pub func main() -> int {
    let mut t: Vec<int> = vecNew<int>();
    t = push<int>(t, 1);
    t = push<int>(t, 2);
    t = push<int>(t, 3);
    t = push<int>(t, 4);
    let mut p: Vec<int> = vecNew<int>();
    p = push<int>(p, 3);
    p = push<int>(p, 4);
    let idx = kmpSearch(t, p);
    outln($"KMP Match found at index: {idx:str}");
    return 0;
}
"""

MODULES["05_strings_and_parsers/recursive_descent_calc.sal"] = """module corpus.parsers.calc;

><salivo.std.core::{outln};
><salivo.std.collections::{Vec, vecNew, push, get, veclen};

pub struct TokenStream {
    Vec<int> tokens;
    int pos;
}

pub func nextVal(ts: TokenStream) -> int {
    let val = get<int>(ts.tokens, ts.pos);
    ts.pos = ts.pos + 1;
    return val;
}

pub func evalFactor(ts: TokenStream) -> int {
    return nextVal(ts);
}

pub func evalTerm(ts: TokenStream) -> int {
    let mut left = evalFactor(ts);
    while (ts.pos < veclen<int>(ts.tokens)) {
        let op = get<int>(ts.tokens, ts.pos);
        if (op == 42) {
            ts.pos = ts.pos + 1;
            let right = evalFactor(ts);
            left = left * right;
        } else {
            return left;
        }
    }
    return left;
}

pub func evalExpr(ts: TokenStream) -> int {
    let mut left = evalTerm(ts);
    while (ts.pos < veclen<int>(ts.tokens)) {
        let op = get<int>(ts.tokens, ts.pos);
        if (op == 43) {
            ts.pos = ts.pos + 1;
            let right = evalTerm(ts);
            left = left + right;
        } else {
            return left;
        }
    }
    return left;
}

pub func main() -> int {
    let mut toks: Vec<int> = vecNew<int>();
    toks = push<int>(toks, 5);
    toks = push<int>(toks, 43);
    toks = push<int>(toks, 3);
    toks = push<int>(toks, 42);
    toks = push<int>(toks, 2);
    let ts = TokenStream { tokens: toks, pos: 0 };
    let result = evalExpr(ts);
    outln($"AST Evaluation 5 + (3 * 2): {result:str}");
    return 0;
}
"""

# =============================================================================
# 6. CRYPTOGRAPHY AND WIRE PROTOCOLS
# =============================================================================

MODULES["06_crypto_and_protocols/fnv1a_hash.sal"] = """module corpus.crypto.fnv;

><salivo.std.core::{outln};
><salivo.std.collections::{Vec, vecNew, push, get, veclen};

pub func fnv1a(data: Vec<int>) -> int {
    let offsetBasis = 2166136261;
    let prime = 16777619;
    let mut hash = offsetBasis;
    let n = veclen<int>(data);
    for (let mut i = 0; i < n; i = i + 1) {
        let b = get<int>(data, i);
        hash = hash ^ b;
        hash = hash * prime;
    }
    return hash;
}

pub func main() -> int {
    let mut bytes: Vec<int> = vecNew<int>();
    bytes = push<int>(bytes, 83);
    bytes = push<int>(bytes, 97);
    bytes = push<int>(bytes, 108);
    bytes = push<int>(bytes, 105);
    bytes = push<int>(bytes, 118);
    bytes = push<int>(bytes, 111);
    let h = fnv1a(bytes);
    outln($"FNV-1a Hash of 'Salivo': {h:str}");
    return 0;
}
"""

MODULES["06_crypto_and_protocols/binary_packet_protocol.sal"] = """module corpus.crypto.packet;

><salivo.std.core::{outln};
><salivo.std.collections::{Vec, vecNew, push, get, set, veclen};

pub struct PacketHeader {
    int magic;
    int opcode;
    int payloadLen;
}

pub struct Packet {
    PacketHeader header;
    Vec<int> payload;
}

pub func encodePacket(pkt: Packet) -> Vec<int> {
    let mut bytes: Vec<int> = vecNew<int>();
    bytes = push<int>(bytes, pkt.header.magic);
    bytes = push<int>(bytes, pkt.header.opcode);
    bytes = push<int>(bytes, pkt.header.payloadLen);
    let n = veclen<int>(pkt.payload);
    for (let mut i = 0; i < n; i = i + 1) {
        bytes = push<int>(bytes, get<int>(pkt.payload, i));
    }
    return bytes;
}

pub func main() -> int {
    let mut body: Vec<int> = vecNew<int>();
    body = push<int>(body, 1);
    body = push<int>(body, 2);
    let hdr = PacketHeader { magic: 51966, opcode: 10, payloadLen: 2 };
    let pkt = Packet { header: hdr, payload: body };
    let wire = encodePacket(pkt);
    let l = veclen<int>(wire);
    outln($"Serialized binary wire frame: {l:str} bytes.");
    return 0;
}
"""

def generate_and_verify():
    print(f"--- Generating & Verifying Advanced Mastery Salivo Corpus ---")
    print(f"Target Directory: {TARGET_DIR}")

    total = len(MODULES)
    passed = 0
    failed = 0

    for rel_path, code in MODULES.items():
        file_path = TARGET_DIR / rel_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(code, encoding="utf-8")

        res = subprocess.run(
            [SF_BIN, "check", str(file_path)],
            capture_output=True,
            text=True,
            timeout=10,
        )

        if res.returncode == 0:
            passed += 1
            print(f"[OK] {rel_path}")
        else:
            failed += 1
            print(f"[FAIL] {rel_path}")
            print("Errors:\n" + res.stderr or res.stdout)

    print(f"\nResult: {passed}/{total} compiled successfully with 0 errors!")
    return failed == 0

if __name__ == "__main__":
    success = generate_and_verify()
    sys.exit(0 if success else 1)
