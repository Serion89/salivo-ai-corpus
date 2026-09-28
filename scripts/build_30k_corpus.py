#!/usr/bin/env python3
"""
Production 30,000-File Salivo Code Synthesis & Stage-3 Verification Engine.
Generates 30 diverse families x 1,000 verified variations.
"""

import os
import sys
import subprocess
import time
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

os.environ["SALIVO_COMPILER"] = "stage3"
DEFAULT_SF = r"C:\Users\sahil\.salivo\bin\sf.exe"

def verify_file(file_path):
    res = subprocess.run(
        [DEFAULT_SF, "check", str(file_path)],
        capture_output=True,
        text=True,
        timeout=10,
        env=os.environ
    )
    return (file_path, res.returncode == 0, res.stderr or res.stdout)

# -----------------------------------------------------------------------------
# 30 Generators (1,000 files each = 30,000 files)
# -----------------------------------------------------------------------------

def gen_bubble_sort(i, out_dir):
    fpath = out_dir / f"bubble_sort_{i:04d}.sal"
    seed = (i * 7 + 13) % 100
    code = f"""module corpus.gen.dsa.bubble_{i};
><salivo.std.core::{{outln}};
><salivo.std.collections::{{Vec, vecNew, push, set, get, veclen}};

pub func sortList(list: Vec<int>) {{
    let n = veclen<int>(list);
    for (let mut a = 0; a < n; a = a + 1) {{
        let limit = n - a - 1;
        for (let mut b = 0; b < limit; b = b + 1) {{
            let next_idx = b + 1;
            let v1 = get<int>(list, b);
            let v2 = get<int>(list, next_idx);
            if (v1 > v2) {{
                set<int>(list, b, v2);
                set<int>(list, next_idx, v1);
            }}
        }}
    }}
}}

pub func main() -> int {{
    let mut numbers: Vec<int> = vecNew<int>();
    numbers = push<int>(numbers, {seed + 40});
    numbers = push<int>(numbers, {seed + 10});
    numbers = push<int>(numbers, {seed + 30});
    numbers = push<int>(numbers, {seed + 20});
    sortList(numbers);
    let first = get<int>(numbers, 0);
    outln($"Smallest element: {{first:str}}");
    return 0;
}}
"""
    fpath.write_text(code, encoding="utf-8")
    return fpath

def gen_selection_sort(i, out_dir):
    fpath = out_dir / f"selection_sort_{i:04d}.sal"
    seed = (i * 11 + 17) % 100
    code = f"""module corpus.gen.dsa.selection_{i};
><salivo.std.core::{{outln}};
><salivo.std.collections::{{Vec, vecNew, push, set, get, veclen}};

pub func selectionSort(list: Vec<int>) {{
    let n = veclen<int>(list);
    for (let mut a = 0; a < n; a = a + 1) {{
        let mut min_idx: int = a;
        for (let mut b = a + 1; b < n; b = b + 1) {{
            if (get<int>(list, b) < get<int>(list, min_idx)) {{
                min_idx = b;
            }}
        }}
        if (min_idx != a) {{
            let t1 = get<int>(list, a);
            let t2 = get<int>(list, min_idx);
            set<int>(list, a, t2);
            set<int>(list, min_idx, t1);
        }}
    }}
}}

pub func main() -> int {{
    let mut arr: Vec<int> = vecNew<int>();
    arr = push<int>(arr, {seed + 50});
    arr = push<int>(arr, {seed + 5});
    arr = push<int>(arr, {seed + 25});
    selectionSort(arr);
    let s = get<int>(arr, 0);
    outln($"Sorted min: {{s:str}}");
    return 0;
}}
"""
    fpath.write_text(code, encoding="utf-8")
    return fpath

def gen_insertion_sort(i, out_dir):
    fpath = out_dir / f"insertion_sort_{i:04d}.sal"
    seed = (i * 13 + 7) % 100
    code = f"""module corpus.gen.dsa.insertion_{i};
><salivo.std.core::{{outln}};
><salivo.std.collections::{{Vec, vecNew, push, set, get, veclen}};

pub func insertionSort(list: Vec<int>) {{
    let n = veclen<int>(list);
    for (let mut a = 1; a < n; a = a + 1) {{
        let key = get<int>(list, a);
        let mut b: int = a - 1;
        while (b >= 0 && get<int>(list, b) > key) {{
            set<int>(list, b + 1, get<int>(list, b));
            b = b - 1;
        }}
        set<int>(list, b + 1, key);
    }}
}}

pub func main() -> int {{
    let mut v: Vec<int> = vecNew<int>();
    v = push<int>(v, {seed + 80});
    v = push<int>(v, {seed + 15});
    v = push<int>(v, {seed + 45});
    insertionSort(v);
    let first = get<int>(v, 0);
    outln($"Insertion min: {{first:str}}");
    return 0;
}}
"""
    fpath.write_text(code, encoding="utf-8")
    return fpath

def gen_binary_search(i, out_dir):
    fpath = out_dir / f"bin_search_{i:04d}.sal"
    target = 10 + (i % 20) * 5
    code = f"""module corpus.gen.dsa.bsearch_{i};
><salivo.std.core::{{outln, Option, some, none}};
><salivo.std.collections::{{Vec, vecNew, push, get, veclen}};

pub func search(v: Vec<int>, target: int) -> Option<int> {{
    let mut l: int = 0;
    let mut r: int = veclen<int>(v) - 1;
    while (l <= r) {{
        let m: int = (l + r) / 2;
        let val = get<int>(v, m);
        if (val == target) {{
            return some(m);
        }} else if (val < target) {{
            l = m + 1;
        }} else {{
            r = m - 1;
        }}
    }}
    return none();
}}

pub func main() -> int {{
    let mut v: Vec<int> = vecNew<int>();
    for (let mut k = 0; k < 25; k = k + 1) {{
        v = push<int>(v, 10 + k * 5);
    }}
    let target_val: int = {target};
    let res = search(v, target_val);
    if (res.is_some) {{
        outln($"Found target: {{target_val:str}}");
    }}
    return 0;
}}
"""
    fpath.write_text(code, encoding="utf-8")
    return fpath

def gen_linear_search(i, out_dir):
    fpath = out_dir / f"linear_search_{i:04d}.sal"
    thresh = 50 + (i % 30)
    code = f"""module corpus.gen.dsa.lsearch_{i};
><salivo.std.core::{{outln}};
><salivo.std.collections::{{Vec, vecNew, push, get, veclen}};

pub func countGreaterThan(v: Vec<int>, threshold: int) -> int {{
    let n = veclen<int>(v);
    let mut c: int = 0;
    for (let mut a = 0; a < n; a = a + 1) {{
        if (get<int>(v, a) > threshold) {{
            c = c + 1;
        }}
    }}
    return c;
}}

pub func main() -> int {{
    let mut v: Vec<int> = vecNew<int>();
    for (let mut k = 0; k < 20; k = k + 1) {{
        v = push<int>(v, 20 + k * 4);
    }}
    let count = countGreaterThan(v, {thresh});
    outln($"Matches above threshold: {{count:str}}");
    return 0;
}}
"""
    fpath.write_text(code, encoding="utf-8")
    return fpath

def gen_fibonacci(i, out_dir):
    fpath = out_dir / f"fibonacci_{i:04d}.sal"
    n_val = 5 + (i % 15)
    code = f"""module corpus.gen.dsa.fib_{i};
><salivo.std.core::{{outln}};

pub func fib(n: int) -> int {{
    if (n <= 0) {{ return 0; }}
    if (n == 1) {{ return 1; }}
    let mut a: int = 0;
    let mut b: int = 1;
    for (let mut k = 2; k <= n; k = k + 1) {{
        let next_val = a + b;
        a = b;
        b = next_val;
    }}
    return b;
}}

pub func main() -> int {{
    let n_input: int = {n_val};
    let res = fib(n_input);
    outln($"Fibonacci result: {{res:str}}");
    return 0;
}}
"""
    fpath.write_text(code, encoding="utf-8")
    return fpath

def gen_sieve(i, out_dir):
    fpath = out_dir / f"sieve_{i:04d}.sal"
    limit = 20 + (i % 40)
    code = f"""module corpus.gen.dsa.sieve_{i};
><salivo.std.core::{{outln}};
><salivo.std.collections::{{Vec, vecNew, push, set, get}};

pub func countPrimes(limit: int) -> int {{
    if (limit < 2) {{ return 0; }}
    let mut flags: Vec<int> = vecNew<int>();
    for (let mut a = 0; a <= limit; a = a + 1) {{
        flags = push<int>(flags, 0);
    }}
    for (let mut p = 2; p * p <= limit; p = p + 1) {{
        if (get<int>(flags, p) == 0) {{
            for (let mut m = p * p; m <= limit; m = m + p) {{
                set<int>(flags, m, 1);
            }}
        }}
    }}
    let mut count: int = 0;
    for (let mut k = 2; k <= limit; k = k + 1) {{
        if (get<int>(flags, k) == 0) {{
            count = count + 1;
        }}
    }}
    return count;
}}

pub func main() -> int {{
    let limit_val: int = {limit};
    let c = countPrimes(limit_val);
    outln($"Primes count: {{c:str}}");
    return 0;
}}
"""
    fpath.write_text(code, encoding="utf-8")
    return fpath

def gen_matrix(i, out_dir):
    fpath = out_dir / f"matrix_{i:04d}.sal"
    r = 2 + (i % 3)
    c = 2 + ((i + 1) % 3)
    code = f"""module corpus.gen.math.matrix_{i};
><salivo.std.core::{{outln}};
><salivo.std.collections::{{Vec, vecNew, push, get, veclen}};

pub func main() -> int {{
    let rows: int = {r};
    let cols: int = {c};
    let total = rows * cols;
    let mut data: Vec<int> = vecNew<int>();
    for (let mut k = 0; k < total; k = k + 1) {{
        data = push<int>(data, k * {i % 5 + 1});
    }}
    let len_v = veclen<int>(data);
    outln($"Matrix total cells: {{len_v:str}}");
    return 0;
}}
"""
    fpath.write_text(code, encoding="utf-8")
    return fpath

def gen_knapsack(i, out_dir):
    fpath = out_dir / f"knapsack_{i:04d}.sal"
    cap = 6 + (i % 6)
    code = f"""module corpus.gen.dsa.knapsack_{i};
><salivo.std.core::{{outln}};
><salivo.std.collections::{{Vec, vecNew, push, set, get}};
><salivo.std.math::{{max}};

pub struct Item {{ int weight; int value; }}

pub func main() -> int {{
    let capacity: int = {cap};
    let mut dp: Vec<int> = vecNew<int>();
    for (let mut a = 0; a <= capacity; a = a + 1) {{
        dp = push<int>(dp, 0);
    }}
    let mut items: Vec<Item> = vecNew<Item>();
    items = push<Item>(items, Item {{ weight: 2, value: 3 }});
    items = push<Item>(items, Item {{ weight: 3, value: 5 }});
    items = push<Item>(items, Item {{ weight: 4, value: 7 }});

    for (let mut j = 0; j < 3; j = j + 1) {{
        let it = get<Item>(items, j);
        let mut w: int = capacity;
        while (w >= it.weight) {{
            let best = max(get<int>(dp, w), get<int>(dp, w - it.weight) + it.value);
            set<int>(dp, w, best);
            w = w - 1;
        }}
    }}
    let res = get<int>(dp, capacity);
    outln($"Optimal knapsack value: {{res:str}}");
    return 0;
}}
"""
    fpath.write_text(code, encoding="utf-8")
    return fpath

def gen_lcs(i, out_dir):
    fpath = out_dir / f"lcs_{i:04d}.sal"
    code = f"""module corpus.gen.dsa.lcs_{i};
><salivo.std.core::{{outln}};
><salivo.std.collections::{{Vec, vecNew, push, set, get}};
><salivo.std.math::{{max}};

pub func main() -> int {{
    let mut a: Vec<int> = vecNew<int>();
    a = push<int>(a, {10 + (i % 3)});
    a = push<int>(a, 20);
    a = push<int>(a, 30);

    let mut b: Vec<int> = vecNew<int>();
    b = push<int>(b, 20);
    b = push<int>(b, {30 + (i % 2)});

    let mut dp: Vec<int> = vecNew<int>();
    for (let mut k = 0; k < 12; k = k + 1) {{
        dp = push<int>(dp, 0);
    }}
    outln("LCS table initialized successfully.");
    return 0;
}}
"""
    fpath.write_text(code, encoding="utf-8")
    return fpath

def gen_gcd_lcm(i, out_dir):
    fpath = out_dir / f"gcd_{i:04d}.sal"
    a = 24 + (i * 3) % 50
    b = 18 + (i * 2) % 30 + 1
    code = f"""module corpus.gen.math.gcd_{i};
><salivo.std.core::{{outln}};

pub func gcd(a: int, b: int) -> int {{
    let mut x: int = a;
    let mut y: int = b;
    while (y != 0) {{
        let r = x % y;
        x = y;
        y = r;
    }}
    return x;
}}

pub func main() -> int {{
    let x_val: int = {a};
    let y_val: int = {b};
    let g = gcd(x_val, y_val);
    outln($"GCD computed: {{g:str}}");
    return 0;
}}
"""
    fpath.write_text(code, encoding="utf-8")
    return fpath

def gen_fast_pow(i, out_dir):
    fpath = out_dir / f"pow_{i:04d}.sal"
    base = 2 + (i % 5)
    exp = 3 + (i % 7)
    code = f"""module corpus.gen.math.pow_{i};
><salivo.std.core::{{outln}};

pub func modPow(base_val: int, exp_val: int, modulus: int) -> int {{
    let mut res: int = 1;
    let mut b: int = base_val % modulus;
    let mut e: int = exp_val;
    while (e > 0) {{
        if (e % 2 == 1) {{
            res = (res * b) % modulus;
        }}
        e = e / 2;
        b = (b * b) % modulus;
    }}
    return res;
}}

pub func main() -> int {{
    let p = modPow({base}, {exp}, 1000);
    outln($"Pow mod 1000: {{p:str}}");
    return 0;
}}
"""
    fpath.write_text(code, encoding="utf-8")
    return fpath

def gen_stats(i, out_dir):
    fpath = out_dir / f"stats_{i:04d}.sal"
    seed = (i * 5 + 3) % 40
    code = f"""module corpus.gen.math.stats_{i};
><salivo.std.core::{{outln}};
><salivo.std.collections::{{Vec, vecNew, push, get, veclen}};

pub func main() -> int {{
    let mut v: Vec<int> = vecNew<int>();
    v = push<int>(v, {seed + 10});
    v = push<int>(v, {seed + 25});
    v = push<int>(v, {seed + 35});
    let n = veclen<int>(v);
    let mut total: int = 0;
    for (let mut k = 0; k < n; k = k + 1) {{
        total = total + get<int>(v, k);
    }}
    let avg = total / n;
    outln($"Average: {{avg:str}}");
    return 0;
}}
"""
    fpath.write_text(code, encoding="utf-8")
    return fpath

def gen_sha256(i, out_dir):
    fpath = out_dir / f"sha256_{i:04d}.sal"
    code = f"""module corpus.gen.security.sha_{i};
><salivo.std.core::{{outln}};
><salivo.std.crypto::{{sha256Hex}};

pub func main() -> int {{
    let msg = "transaction_record_{i}";
    let h = sha256Hex(msg);
    outln($"SHA-256 digest: {{h}}");
    return 0;
}}
"""
    fpath.write_text(code, encoding="utf-8")
    return fpath

def gen_hmac(i, out_dir):
    fpath = out_dir / f"hmac_{i:04d}.sal"
    code = f"""module corpus.gen.security.hmac_{i};
><salivo.std.core::{{outln}};
><salivo.std.crypto::{{hmacSha256Hex, constantTimeEq}};

pub func main() -> int {{
    let key = "secret_key_{i}";
    let msg = "payload_content_{i}";
    let sig = hmacSha256Hex(key, msg);
    let ok = constantTimeEq(sig, sig);
    if (ok) {{
        outln("HMAC verification success.");
    }}
    return 0;
}}
"""
    fpath.write_text(code, encoding="utf-8")
    return fpath

def gen_token_bucket(i, out_dir):
    fpath = out_dir / f"bucket_{i:04d}.sal"
    cap = 10 + (i % 20)
    code = f"""module corpus.gen.security.bucket_{i};
><salivo.std.core::{{outln}};

pub struct Bucket {{ int capacity; int tokens; }}

pub func main() -> int {{
    let b = Bucket {{ capacity: {cap}, tokens: {cap} }};
    outln($"Bucket capacity: {{b.capacity:str}}");
    return 0;
}}
"""
    fpath.write_text(code, encoding="utf-8")
    return fpath

def gen_memory_buffer(i, out_dir):
    fpath = out_dir / f"mem_{i:04d}.sal"
    val = 100 + i * 2
    code = f"""module corpus.gen.systems.mem_{i};
><salivo.std.core::{{outln}};
><salivo.std.mem::{{allocate, deallocate, writei64, readi64}};

pub func main() -> int {{
    let addr = allocate(16, 8);
    writei64(addr, 0, {val});
    let read_val = readi64(addr, 0);
    deallocate(addr, 16, 8);
    outln($"Memory read value: {{read_val:str}}");
    return 0;
}}
"""
    fpath.write_text(code, encoding="utf-8")
    return fpath

def gen_raii_guard(i, out_dir):
    fpath = out_dir / f"raii_{i:04d}.sal"
    code = f"""module corpus.gen.systems.raii_{i};
><salivo.std.core::{{outln, Drop}};

pub struct ResourceGuard {{ int id; }}

impl Drop for ResourceGuard {{
    func drop(self) {{
        outln($"Cleaning up resource #{{self.id:str}}");
    }}
}}

pub func main() -> int {{
    let g = ResourceGuard {{ id: {i} }};
    outln("Scope running...");
    return 0;
}}
"""
    fpath.write_text(code, encoding="utf-8")
    return fpath

def gen_http_router(i, out_dir):
    fpath = out_dir / f"router_{i:04d}.sal"
    endpoint = f"/v1/api/endpoint_{i % 50}"
    code = f"""module corpus.gen.backend.router_{i};
><salivo.std.core::{{outln}};

pub func route(method: string, path: string) -> int {{
    if (method == "GET" && path == "{endpoint}") {{
        return 200;
    }}
    return 404;
}}

pub func main() -> int {{
    let status = route("GET", "{endpoint}");
    outln($"Route status: {{status:str}}");
    return 0;
}}
"""
    fpath.write_text(code, encoding="utf-8")
    return fpath

def gen_status_classifier(i, out_dir):
    fpath = out_dir / f"status_{i:04d}.sal"
    code_val = [200, 201, 204, 400, 401, 403, 404, 500, 502, 503][i % 10]
    code = f"""module corpus.gen.backend.status_{i};
><salivo.std.core::{{outln}};

pub func isSuccess(status: int) -> bool {{
    return status >= 200 && status < 300;
}}

pub func main() -> int {{
    let st: int = {code_val};
    let ok = isSuccess(st);
    if (ok) {{
        outln($"Status is SUCCESS");
    }} else {{
        outln($"Status is NOT SUCCESS");
    }}
    return 0;
}}
"""
    fpath.write_text(code, encoding="utf-8")
    return fpath

def gen_json_builder(i, out_dir):
    fpath = out_dir / f"json_{i:04d}.sal"
    code = f"""module corpus.gen.backend.json_{i};
><salivo.std.core::{{outln}};

pub func main() -> int {{
    let lbrace = "{{";
    let rbrace = "}}";
    let id_val: int = {i};
    let payload = $"{{lbrace}}\\"id\\": {{id_val:str}}, \\"active\\": true{{rbrace}}";
    outln(payload);
    return 0;
}}
"""
    fpath.write_text(code, encoding="utf-8")
    return fpath

def gen_middleware(i, out_dir):
    fpath = out_dir / f"middleware_{i:04d}.sal"
    code = f"""module corpus.gen.backend.mid_{i};
><salivo.std.core::{{outln}};

pub struct Request {{ string token; int id; }}

pub func checkToken(req: Request) -> bool {{
    return req.token == "valid_token";
}}

pub func main() -> int {{
    let req = Request {{ token: "valid_token", id: {i} }};
    let ok = checkToken(req);
    if (ok) {{
        outln("Middleware pass.");
    }}
    return 0;
}}
"""
    fpath.write_text(code, encoding="utf-8")
    return fpath

def gen_query_parser(i, out_dir):
    fpath = out_dir / f"query_{i:04d}.sal"
    code = f"""module corpus.gen.backend.query_{i};
><salivo.std.core::{{outln}};
><salivo.std.collections::{{HashMap, mapNew, put, lookup}};
><salivo.std.option::{{unwrapOr}};

pub func main() -> int {{
    let mut m = mapNew<string, string>();
    m = put<string, string>(m, "page", "{i % 10 + 1}");
    let opt = lookup<string, string>(m, "page");
    let p = unwrapOr<string>(opt, "1");
    outln($"Page query parameter: {{p}}");
    return 0;
}}
"""
    fpath.write_text(code, encoding="utf-8")
    return fpath

def gen_jwt_claims(i, out_dir):
    fpath = out_dir / f"jwt_{i:04d}.sal"
    code = f"""module corpus.gen.backend.jwt_{i};
><salivo.std.core::{{outln}};

pub struct Claims {{ string sub; int exp; }}

pub func main() -> int {{
    let c = Claims {{ sub: "user_{i}", exp: {1700000000 + i * 10} }};
    outln($"Token subject: {{c.sub}}");
    return 0;
}}
"""
    fpath.write_text(code, encoding="utf-8")
    return fpath

def gen_api_key(i, out_dir):
    fpath = out_dir / f"apikey_{i:04d}.sal"
    code = f"""module corpus.gen.backend.apikey_{i};
><salivo.std.core::{{outln}};

pub struct ApiKey {{ string key; bool is_active; }}

pub func main() -> int {{
    let key = ApiKey {{ key: "ak_live_{i}", is_active: true }};
    if (key.is_active) {{
        outln("API key active.");
    }}
    return 0;
}}
"""
    fpath.write_text(code, encoding="utf-8")
    return fpath

def gen_html_tag(i, out_dir):
    fpath = out_dir / f"html_{i:04d}.sal"
    code = f"""module corpus.gen.frontend.html_{i};
><salivo.std.core::{{outln}};

pub func main() -> int {{
    let title = "Article #{i}";
    let h1 = $"<h1>{{title}}</h1>";
    outln(h1);
    return 0;
}}
"""
    fpath.write_text(code, encoding="utf-8")
    return fpath

def gen_ui_card(i, out_dir):
    fpath = out_dir / f"card_{i:04d}.sal"
    code = f"""module corpus.gen.frontend.card_{i};
><salivo.std.core::{{outln}};

pub struct Card {{ string title; int likes; }}

pub func main() -> int {{
    let c = Card {{ title: "Post #{i}", likes: {i * 3} }};
    let html = $"<div class='card'><h3>{{c.title}}</h3><span>{{c.likes:str}} likes</span></div>";
    outln(html);
    return 0;
}}
"""
    fpath.write_text(code, encoding="utf-8")
    return fpath

def gen_table_renderer(i, out_dir):
    fpath = out_dir / f"table_{i:04d}.sal"
    code = f"""module corpus.gen.frontend.table_{i};
><salivo.std.core::{{outln}};

pub func main() -> int {{
    let idx: int = {i};
    let row = $"<tr><td>{{idx:str}}</td><td>Service #{{idx:str}}</td></tr>";
    outln(row);
    return 0;
}}
"""
    fpath.write_text(code, encoding="utf-8")
    return fpath

def gen_css_class(i, out_dir):
    fpath = out_dir / f"css_{i:04d}.sal"
    is_prime = 1 if i % 2 == 0 else 0
    code = f"""module corpus.gen.frontend.css_{i};
><salivo.std.core::{{outln}};

pub func main() -> int {{
    let mut classes = "btn";
    if ({is_prime} == 1) {{
        classes = $"{{classes}} btn-primary";
    }} else {{
        classes = $"{{classes}} btn-secondary";
    }}
    outln($"Class: {{classes}}");
    return 0;
}}
"""
    fpath.write_text(code, encoding="utf-8")
    return fpath

def gen_fintech_ledger(i, out_dir):
    fpath = out_dir / f"fintech_{i:04d}.sal"
    p = 1000 + (i * 50)
    r = 5
    t = 3
    code = f"""module corpus.gen.fintech.ledger_{i};
><salivo.std.core::{{outln}};

pub func simpleInterest(principal: int, rate: int, years: int) -> int {{
    return (principal * rate * years) / 100;
}}

pub func main() -> int {{
    let interest = simpleInterest({p}, {r}, {t});
    outln($"Interest computed: {{interest:str}}");
    return 0;
}}
"""
    fpath.write_text(code, encoding="utf-8")
    return fpath

ALL_GENERATORS = [
    ("dsa_sorting", gen_bubble_sort),
    ("dsa_sorting", gen_selection_sort),
    ("dsa_sorting", gen_insertion_sort),
    ("dsa_searching", gen_binary_search),
    ("dsa_searching", gen_linear_search),
    ("dsa_dp", gen_fibonacci),
    ("dsa_dp", gen_sieve),
    ("dsa_math", gen_matrix),
    ("dsa_dp", gen_knapsack),
    ("dsa_dp", gen_lcs),
    ("math_algebra", gen_gcd_lcm),
    ("math_algebra", gen_fast_pow),
    ("math_stats", gen_stats),
    ("security_crypto", gen_sha256),
    ("security_crypto", gen_hmac),
    ("security_crypto", gen_token_bucket),
    ("systems_mem", gen_memory_buffer),
    ("systems_raii", gen_raii_guard),
    ("backend_api", gen_http_router),
    ("backend_api", gen_status_classifier),
    ("backend_api", gen_json_builder),
    ("backend_api", gen_middleware),
    ("backend_api", gen_query_parser),
    ("backend_api", gen_jwt_claims),
    ("backend_api", gen_api_key),
    ("frontend_ui", gen_html_tag),
    ("frontend_ui", gen_ui_card),
    ("frontend_ui", gen_table_renderer),
    ("frontend_ui", gen_css_class),
    ("fintech_biz", gen_fintech_ledger),
]

def main():
    root_dir = Path(__file__).resolve().parent.parent
    corpus_root = root_dir / "corpus"
    
    batch_size = 1000  # 1000 per family = 30,000 files!
    total_expected = len(ALL_GENERATORS) * batch_size

    print(f"==================================================")
    print(f"Salivo 30,000-File High-Speed Synthesis Engine")
    print(f"Generators: {len(ALL_GENERATORS)} families")
    print(f"Per Family: {batch_size} files")
    print(f"Total Target: {total_expected} files")
    print(f"==================================================")

    generated_files = []
    t_start = time.time()

    # Step 1: Generate all files
    for fam_idx, (subdir_name, gen_func) in enumerate(ALL_GENERATORS):
        out_dir = corpus_root / f"gen_{subdir_name}"
        out_dir.mkdir(parents=True, exist_ok=True)
        for i in range(batch_size):
            fp = gen_func(i, out_dir)
            generated_files.append(fp)
        print(f"[{fam_idx + 1:02d}/30] Generated {batch_size} files in gen_{subdir_name}")

    t_gen = time.time()
    print(f"\nGeneration complete in {t_gen - t_start:.2f}s ({len(generated_files)} files).")
    print(f"Starting parallel Stage-3 compiler verification (16 workers)...")

    # Step 2: Parallel compiler verification
    passed = 0
    failed = 0
    with ProcessPoolExecutor(max_workers=16) as executor:
        futures = [executor.submit(verify_file, fp) for fp in generated_files]
        for idx, fut in enumerate(as_completed(futures), 1):
            fp, ok, err = fut.result()
            if ok:
                passed += 1
            else:
                failed += 1
                fp.unlink(missing_ok=True)
                if failed <= 5:
                    print(f"  [DISCARD] {fp.name}: {err[:80]}")
            if idx % 5000 == 0 or idx == len(generated_files):
                print(f"  Verified {idx}/{len(generated_files)} files ({passed} passed, {failed} discarded)...")

    t_verify = time.time()
    print(f"\n==================================================")
    print(f"Synthesis & Verification Summary:")
    print(f"  Generated: {len(generated_files)}")
    print(f"  Passed:    {passed}")
    print(f"  Discarded: {failed}")
    print(f"  Time:      {t_verify - t_gen:.2f}s verification")
    print(f"==================================================")

if __name__ == "__main__":
    main()
