"""Sanity checks that need no training: random-policy score and mask printouts.

    python sanity.py [size]  ->  results/sanity.txt

(The two checks that need training - "each sub-task is learnable under its filter" and
"the baseline learns something" - come from the `sanity` and `calib` batches; analyze.py
adds them to the report.)
"""
import collections
import os
import sys

import numpy as np

from skillenv import SUBTASKS, SkillFilterEnv, apply_filter, render_ascii

size = int(sys.argv[1]) if len(sys.argv) > 1 else 9
out = []

for mode in ("full",) + SUBTASKS:
    env = SkillFilterEnv(size=size, mode=mode)
    rng = np.random.default_rng(0)
    c = collections.Counter()
    n_ep = 2000
    for ep in range(n_ep):
        env.reset(seed=30_000_000 + ep)
        while True:
            _, _, term, trunc, info = env.step(int(rng.integers(7)))
            if term or trunc:
                c[info["outcome"]] += 1
                break
    out.append(f"random policy, size {size}, mode {mode:9s} ({n_ep} episodes): "
               + ", ".join(f"{k} {v / n_ep:.1%}" for k, v in sorted(c.items())))

out.append("\nLegend: # wall, D locked door, d closed door, O open door, k key, o moving ball, "
           "~ lava, G goal, >v<^ agent")
env = SkillFilterEnv(size=size, mode="full")
for seed in (3, 11):
    obs = env.reset(seed=seed)[0]["image"]
    out.append(f"\n=== layout seed {seed}: full observation, then each filter ===")
    views = [("no filter", obs)] + [(f, apply_filter(obs, f)) for f in SUBTASKS]
    blocks = [[name.ljust(size)] + render_ascii(v).split("\n") for name, v in views]
    for row in zip(*blocks):
        out.append("   ".join(r.ljust(size) for r in row))

out.append("\n=== what each sub-task episode looks like (same layout seed 3, unfiltered) ===")
blocks = []
for mode in ("full",) + SUBTASKS:
    e = SkillFilterEnv(size=size, mode=mode)
    blocks.append([mode.ljust(size)] + render_ascii(e.reset(seed=3)[0]["image"]).split("\n"))
for row in zip(*blocks):
    out.append("   ".join(r.ljust(size) for r in row))

text = "\n".join(out)
print(text)
os.makedirs("results", exist_ok=True)
with open("results/sanity.txt", "w") as f:
    f.write(text + "\n")
