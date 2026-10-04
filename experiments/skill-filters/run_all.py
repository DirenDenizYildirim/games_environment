"""Run a batch of training jobs, 4 at a time, skipping finished runs and resuming partial ones.

    python run_all.py calib     # difficulty calibration (condition A only, separate seeds)
    python run_all.py sanity    # skill-policy learnability check (condition B, phase 1)
    python run_all.py main      # the 4 conditions x 5 seeds comparison

Every job writes to results/runs/<batch>/<cond>_size<size>_s<seed>/ and is safe to kill:
re-running the same command picks up from the last checkpoint.
"""
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG = json.load(open(os.path.join(HERE, "config.json")))


def jobs(batch):
    c = CONFIG
    if batch == "calib":
        return [("A", s, size, c["total_steps"], []) for size in c["calib_sizes"] for s in c["calib_seeds"]]
    if batch == "sanity":
        # phase 1 only: give it the full phase-1 allowance and stop right after
        return [("B", s, c["sanity_size"], c["total_steps"], ["--phase1-only", "1"])
                for s in c["calib_seeds"][:1]]
    if batch == "main":
        return [(cond, s, c["size"], c["total_steps"], []) for s in c["main_seeds"] for cond in "ABCD"]
    if batch.startswith("opt_"):
        return []  # optional extensions, added only after the main write-up
    raise SystemExit(f"unknown batch {batch}")


def run(job, batch):
    cond, seed, size, steps, extra = job
    out = os.path.join(HERE, "results", "runs", batch, f"{cond}_size{size}_s{seed}")
    if os.path.exists(os.path.join(out, "final.json")):
        return out, 0
    os.makedirs(out, exist_ok=True)
    cmd = [sys.executable, os.path.join(HERE, "ppo.py"), "--cond", cond, "--seed", str(seed),
           "--size", str(size), "--total-steps", str(steps), "--out", out,
           "--phase1-max-frac", str(CONFIG["phase1_max_frac"]), "--K", str(CONFIG["K"])] + extra
    with open(os.path.join(out, "stdout.log"), "a") as log:
        rc = subprocess.call(cmd, stdout=log, stderr=subprocess.STDOUT, cwd=HERE)
    print(f"[{'ok' if rc == 0 else 'FAILED rc=%d' % rc}] {out}", flush=True)
    return out, rc


if __name__ == "__main__":
    batch = sys.argv[1]
    workers = int(sys.argv[2]) if len(sys.argv) > 2 else CONFIG["workers"]
    js = jobs(batch)
    print(f"{batch}: {len(js)} jobs, {workers} workers", flush=True)
    with ThreadPoolExecutor(workers) as ex:
        results = list(ex.map(lambda j: run(j, batch), js))
    failed = [o for o, rc in results if rc]
    print(f"{batch}: {len(js) - len(failed)} ok, {len(failed)} failed", flush=True)
    sys.exit(1 if failed else 0)
