# DECISIONS — every choice made on your behalf

One line of reasoning each. Sections 1–6 were written **before any result from conditions
B, C or D existed**; section 7 is appended as runs happen (crashes, reruns, surprises).

## 0. Where this lives

| Choice | Why |
|---|---|
| Self-contained folder `experiments/skill-filters/`, outside `projects/` | The repo's two CoG projects are unrelated; you said the repo is "mostly for show", so its approval gate was not applied and nothing in `projects/` was touched. |

## 1. Hardware and budget

| Choice | Why |
|---|---|
| Hardware measured: 4 CPU cores, no GPU, 15 GB RAM, no detectable time limit | `nproc`, `free -g`, no `nvidia-smi`. |
| "8 hours of compute" read as **8 hours of wall clock on this 4-core machine** (4 runs in parallel, 1 torch thread each) | Running 4 single-threaded processes at once uses the cores best, measured ≈1,870 env steps/s per process ≈ 7,500/s overall. |
| **5,000,000 env steps per run**, every condition | 20 main runs × 5M = 100M steps ≈ 3.7 h at 7,500 steps/s; calibration plus the sanity runs fit in the remaining ~3–4 h. |
| Network shrunk during smoke testing (32-64-64 conv + 256 fc → 16-32-32 conv + 128 fc) | The bigger net made each PPO update 3–4× slower (profiled: 75% of the time went to backprop). Done before any learning result existed. |
| Budget can overshoot by at most one rollout (≤2,048 steps for A/D/phase 1, ≤8,192 for phase 2), and those steps are still counted | A rollout is never cut in half; the curves are cut at 5M for every condition anyway. |

## 2. Environment

| Choice | Why |
|---|---|
| Two rooms separated by a wall with one **locked** door; key + agent in the left room, goal in the right | The smallest layout where all three skills are required and interact (the door blocks the only route to the goal). |
| Lava: 8% of interior cells, both rooms; 1 moving ball in the right room (2 for size ≥ 11) | Hazards on both sides of the door, so hazard avoidance matters during the key phase as well as the goal phase. |
| Balls move to a random free neighbouring cell each step (MiniGrid `DynamicObstacles` rule); dying = walking forward into a ball | Same mechanism as the standard MiniGrid moving-obstacle env. |
| Every layout checked by breadth-first search (key reachable, door reachable, goal reachable from door, all avoiding lava); unsolvable layouts are redrawn | Unsolvable episodes would cap success below 100% and add noise. |
| **Full-grid symbolic observation** (whole map, cell = object type + state), not the 7×7 egocentric view | With a 7×7 view and no memory the task becomes partly a memory problem for every condition; the full map removes that confound and makes masks easy to read. |
| Colour channel dropped | Every object type has a single fixed colour here, so colour adds no information. |
| Reward: MiniGrid's standard `1 − 0.9·steps/max_steps` on reaching the goal, 0 otherwise (also 0 for dying) | Your spec (standard sparse success reward); MiniGrid's lava envs also give 0 on death. |
| `max_steps = 4·size²` (324 at size 9) | MiniGrid's convention for its lava and dynamic-obstacle envs; ~10× the optimal path length. |
| All 7 MiniGrid actions kept | Not removing any keeps us at the MiniGrid default; it costs every condition the same. |

## 3. Filters and sub-tasks

| Choice | Why |
|---|---|
| Filters exactly as in your table; walls and the agent are always visible; hidden types become empty floor (type + state zeroed) | Your spec. |
| Sub-task episodes use the full-task layout generator, then make irrelevant objects **absent** (removed from the grid) rather than merely harmless | An invisible-but-solid key or ball would be an unexplained wall; "absent" is the cleanest version of "inert". |
| `navigate` episodes: no lava, no balls, no key, door **closed but unlocked** | The navigate filter cannot see a key, so the door must be openable without one or the sub-task is unsolvable. |
| `hazard` episodes: no key, door **already open** | The hazard filter cannot see the door at all, so it must not block. |
| `key_door` episodes: no lava, no balls, no goal; success = door opened; +0.2 the first time the key is picked up | Your spec says "pick up the key and open the door"; the key bonus makes both sub-goals in your table rewarded, and is the same bonus D gets. |
| Condition D bonuses: +0.2 first key pickup, +0.2 first door opening (once each per episode), on top of the normal goal reward | Your spec: the same sub-goals as B. One-time bonuses so they cannot be farmed. |
| Filter id appended as a 3-dim one-hot, concatenated to the flattened conv features | Literal reading of "appended to the observation as a one-hot vector". A and D feed zeros there (same network, unused input). |

## 4. Learning setup

| Choice | Why |
|---|---|
| CleanRL-style PPO, PyTorch, one file (`ppo.py`) | Your spec. |
| **Same network for every policy** — baseline, skill policy and controller (conv 16-32-32, fc 128; ≈120k parameters) | "Same network architecture" taken literally, so no condition gets more capacity; it is still small. |
| PPO hyperparameters: 16 envs × 128 steps, lr 5e-4 constant, γ 0.99, GAE λ 0.95, 4 epochs, 4 minibatches, clip 0.2, entropy 0.01, value 0.5, grad-norm 0.5 | Common MiniGrid/CleanRL defaults. **No tuning for any condition**, so the "equal tuning" rule is met trivially. |
| Constant learning rate (no annealing) | B/C have two phases of uncertain length; annealing over the run would treat the phases unequally. |
| Controller discount = 0.99^K per decision | Same discount *per environment step* as every other policy. |
| Controller picks a filter every K = 4 steps (your default); it sees the full observation; the frozen skill policy samples its actions (not argmax) | Your spec; sampling is how the skill policy was trained. |
| **Phase-1 → phase-2 switch**: when every sub-task has ≥ 90% success over its last 100 training episodes, or after 50% of the budget (2.5M steps), whichever comes first | Fixed before seeing any results and identical for B and C. Adaptive so B is not charged for steps it does not need; the 50% cap stops phase 1 from eating the controller's budget. |
| Timeouts are treated like terminal states in the value bootstrap | CleanRL's standard simplification; applies to every condition. |
| Seeds: main runs 0–4; calibration and sanity runs 100+ | Calibration runs are kept separate so picking the grid size does not reuse the main A seeds. |
| Checkpoint every 25 updates; resumed runs restore network, optimiser and RNG state but restart the environments with fresh seeds | A resumed run is not bit-identical to an uninterrupted one; saving every env's internal state isn't worth it here. |

## 5. Difficulty calibration

| Choice | Why |
|---|---|
| Calibration on condition A only, at sizes 7, 9, 11, seed 100, at the full 5M budget | Your spec: pick the size from the baseline only, then freeze. |
| Pick the size whose A final success is in 20–90%, closest to the middle (≈55%), preferring the larger size on a tie | Mid-range leaves room to see both "faster" and "slower". |

## 6. Analysis plan (fixed before results)

**Success curve.** For each run, success rate of the full-task *training* episodes in bins of
100k env steps (50 bins). For B and C, phase 1 has no full-task agent, so their success is
0 until phase 2 starts — the cost of phase 1 is charged, which is what the claim is about.
Plot: mean across 5 seeds, shading = min–max across seeds (with 5 seeds, min–max shows every
run's spread better than a standard deviation does).

**Steps to 50% / 80%.** Per seed: end of the first 100k-step bin whose training success is
≥ the threshold; "not reached" if none. The same rule for every condition.

**Final success.** 500 evaluation episodes per run on fresh layouts (seeds kept separate
from training), stochastic policy, after training. Reported as mean ± sd over seeds,
plus every seed.

**Area under the curve (AUC).** Mean of the 50 binned success values = average success over
the whole budget. A single sample-efficiency number that still works if a threshold is
never reached.

**Verdict rule for the claim (B vs A), primary metric = steps to 50%:**
- *Supported* if B reaches 50% in ≥ 4/5 seeds, B's median steps-to-50% is lower than A's,
  and a one-sided Mann–Whitney U test on steps-to-50% (not-reached = tied at the budget)
  gives p < 0.05. With 5 vs 5 seeds this needs near-complete separation.
- *Not supported* if B's median steps-to-50% is ≥ A's (B is not faster), counting
  "not reached" as the slowest.
- *Inconclusive* otherwise. In that case the report says what would settle it.
- If neither A nor B reaches 50% in ≥ 3 seeds, the same rule is applied to AUC instead
  (higher is better).

**B vs C and B vs D** are explanatory comparisons with the same statistics. They help explain
any difference; they do not change the verdict, and no multiple-comparison correction is
applied because they are not used as confirmatory tests.

**Failure causes** come from the 500 final-evaluation episodes per run: outcome (success,
lava, ball, timeout), the filter active at the final step, and whether the hazard that
killed the agent was hidden by that filter.

## 7. Log of things that happened

| When | What | Why / effect |
|---|---|---|
