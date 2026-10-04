# Skill filters — does training on masked sub-tasks make an RL agent learn faster?

A self-contained experiment (unrelated to the rest of this repo). The answer is in
**[RESULTS.md](RESULTS.md)**; every choice made along the way is in **[DECISIONS.md](DECISIONS.md)**.

## Install

CPU only, Python 3.10+:

```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install minigrid gymnasium numpy pandas matplotlib
```

(Tested with torch 2.14.1+cpu, minigrid 3.1.0, gymnasium 1.3.0, numpy 2.4.6, pandas 3.0.6.)

## Reproduce everything

```bash
cd experiments/skill-filters
./reproduce.sh          # sanity checks, calibration, the 20 main runs, analysis (~8 h on 4 cores)
```

or step by step:

```bash
python sanity.py 9               # random policy + mask printouts -> results/sanity.txt
python run_all.py calib          # pick the grid size from the baseline only
python run_all.py sanity         # each sub-task learnable under its filter?
python run_all.py main           # conditions A, B, C, D x 5 seeds
python analyze.py calib && python analyze.py main   # tables + plot from the raw CSVs
```

Every run checkpoints as it goes. Kill anything at any time and re-run the same command to
resume; finished runs are skipped. `config.json` holds the budget, grid size and seeds.

## Files

| File | What it is |
|---|---|
| `skillenv.py` | The custom MiniGrid task (`SkillFilterEnv`), its three sub-task modes, the filters |
| `ppo.py` | Single-file PPO; runs any of the conditions A/B/C/D |
| `run_all.py` | Runs a batch of jobs 4 at a time, resumable |
| `analyze.py` | Rebuilds every table and plot from the raw logs |
| `sanity.py` | Checks that need no training (random policy, masks) |
| `results/runs/<batch>/<run>/train.csv` | Raw per-update log of each run (curve, outcomes, filter choices) |
| `results/runs/<batch>/<run>/final_eval.csv` | 500 evaluation episodes per run, with cause of failure |
| `results/main_*.csv`, `results/main_curve.png` | Derived tables and the main plot |
