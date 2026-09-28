#!/usr/bin/env python3
"""
Automated compiler verification runner for Salivo AI Corpus.
Strictly enforces the Stage 3 Self-Hosted Compiler (salivoc.exe).
Performs 2-stage verification on every .sal file:
  Stage 1: Syntax & Semantic Check (sf check)
  Stage 2: Full Stage-3 Native Compilation & Execution (sf run --compiler stage3)
"""

import os
import sys
import subprocess
import time
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

# Enforce Stage-3 compiler environment
os.environ["SALIVO_COMPILER"] = "stage3"

DEFAULT_SF = r"C:\Users\sahil\.salivo\bin\sf.exe"

def find_sf_binary():
    if os.path.exists(DEFAULT_SF):
        return DEFAULT_SF
    import shutil
    sf_in_path = shutil.which("sf")
    if sf_in_path:
        return sf_in_path
    raise FileNotFoundError("Could not find sf.exe compiler binary.")

def main():
    root_dir = Path(__file__).resolve().parent.parent
    corpus_dir = root_dir / "corpus"

    if not corpus_dir.exists():
        print(f"Error: Corpus directory not found at {corpus_dir}")
        sys.exit(1)

    sf_bin = find_sf_binary()
    print("==================================================")
    print(">> Salivo Compiler: Stage 3 Self-Hosted Compiler")
    print(f">> Driver: {sf_bin}")
    print(f">> Mode:   --compiler stage3 (SALIVO_COMPILER=stage3)")
    print(f">> Target: {corpus_dir}")
    print("==================================================\n")

    sal_files = sorted(list(corpus_dir.rglob("*.sal")))
    if not sal_files:
        print("No .sal files found to verify.")
        return

    print(f"Found {len(sal_files)} Salivo source file(s) to verify & execute.\n")

    passed = 0
    failed = 0
    start_time = time.time()

    for file_path in sal_files:
        rel_path = file_path.relative_to(root_dir)
        print(f"Testing [Stage-3]: {rel_path} ...", end=" ", flush=True)

        # Stage 1: Syntax & Semantic Check
        check_res = subprocess.run(
            [sf_bin, "check", str(file_path)],
            capture_output=True,
            text=True,
            timeout=15,
            env=os.environ
        )
        if check_res.returncode != 0:
            print("[FAIL - CHECK]")
            print(f"      {check_res.stderr.strip() or check_res.stdout.strip()}")
            failed += 1
            continue

        # Stage 2: Stage-3 Native Compilation & Execution
        run_res = subprocess.run(
            [sf_bin, "run", "--compiler", "stage3", str(file_path)],
            capture_output=True,
            text=True,
            timeout=20,
            env=os.environ
        )
        if run_res.returncode == 0:
            print("[PASS & EXECUTED OK]")
            passed += 1
        else:
            print("[FAIL - STAGE-3 RUN]")
            print(f"      {run_res.stderr.strip() or run_res.stdout.strip()}")
            failed += 1

    elapsed = time.time() - start_time
    print(f"\n==================================================")
    print(f"Stage-3 Verification Summary ({elapsed:.2f}s):")
    print(f"  Total Files:       {len(sal_files)}")
    print(f"  Stage-3 Executed:  {passed}")
    print(f"  Failed:            {failed}")
    print(f"==================================================")

    if failed > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()
