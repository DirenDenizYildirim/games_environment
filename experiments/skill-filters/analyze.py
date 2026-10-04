"""Turn raw run logs into the plots and tables used in RESULTS.md.

    python analyze.py main      # -> results/main_*.csv, results/main_curve.png, results/main_summary.txt
    python analyze.py calib     # -> calibration table

Everything here is computed from results/runs/<batch>/*/train.csv, final_eval.csv,
phase1_eval.json, so plots can be regenerated at any time (also mid-run, for partial data).
Rules follow DECISIONS.md section 6.
"""
import glob
import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results")
CONFIG = json.load(open(os.path.join(HERE, "config.json")))
BIN = 100_000
SUBTASKS = ("navigate", "hazard", "key_door")
COND_NAME = {"A": "A  full view (baseline)", "B": "B  skill filters (the idea)",
             "C": "C  sub-tasks, no filtering", "D": "D  full view + sub-goal rewards"}


def load_train(path):
    from ppo import ALL_COLS, read_train_csv
    df = pd.DataFrame(read_train_csv(path)).reindex(columns=ALL_COLS)
    return df.apply(pd.to_numeric, errors="coerce").fillna(0)


def load_runs(batch):
    runs = []
    for d in sorted(glob.glob(os.path.join(RES, "runs", batch, "*"))):
        name = os.path.basename(d)
        cond, size, seed = name.split("_")
        r = dict(dir=d, name=name, cond=cond, size=int(size[4:]), seed=int(seed[1:]))
        tp = os.path.join(d, "train.csv")
        r["train"] = load_train(tp) if os.path.exists(tp) else None
        fe = os.path.join(d, "final_eval.csv")
        r["final"] = pd.read_csv(fe) if os.path.exists(fe) else None
        p1 = os.path.join(d, "phase1_eval.json")
        r["phase1"] = json.load(open(p1)) if os.path.exists(p1) else None
        fj = os.path.join(d, "final.json")
        r["done"] = os.path.exists(fj)
        r["summary"] = json.load(open(fj)) if r["done"] else None
        runs.append(r)
    return runs


def binned_curve(train, total):
    """Success rate of full-task training episodes per 100k-step bin (0 where no full-task agent)."""
    nb = int(np.ceil(total / BIN))
    t = train.copy()
    t["bin"] = ((t.global_step - 1) // BIN).clip(upper=nb - 1)
    g = t.groupby("bin")[["episodes", "success"]].sum().reindex(range(nb))
    sr = (g.success / g.episodes.replace(0, np.nan))
    last = int(t["bin"].max())
    # bins with no full-task episodes: 0 if before the last logged step (phase 1), NaN after
    sr = sr.where(~(sr.isna() & (sr.index <= last)), 0.0)
    return sr.values  # length nb, NaN only for bins not yet trained


def steps_to(curve, thr):
    hit = np.nonzero(np.nan_to_num(curve, nan=-1) >= thr)[0]
    return (hit[0] + 1) * BIN if len(hit) else None


def mann_whitney_less(x, y):
    """One-sided exact Mann-Whitney U: P(U <= u_obs) under H0, testing x tends to be smaller.
    Ties count 0.5. Exact by enumerating all relabelings (fine for 5 vs 5)."""
    from itertools import combinations
    x, y = list(x), list(y)
    allv = x + y
    n = len(x)

    def U(a, b):
        return sum((ai < bi) + 0.5 * (ai == bi) for ai in a for bi in b)
    u_obs = U(x, y)
    us = []
    for idx in combinations(range(len(allv)), n):
        a = [allv[i] for i in idx]
        b = [allv[i] for i in range(len(allv)) if i not in idx]
        us.append(U(a, b))
    us = np.array(us)
    return u_obs, float(np.mean(us >= u_obs - 1e-9))  # large U = x smaller


def fmt_steps(v):
    return "not reached" if v is None else f"{v / 1e6:.1f}M"


def analyze_main(batch="main"):
    total = CONFIG["total_steps"]
    runs = [r for r in load_runs(batch) if r["train"] is not None and r["done"]]  # finished runs only
    rows, curves = [], {}
    for r in runs:
        c = binned_curve(r["train"], total)
        curves[(r["cond"], r["seed"])] = c
        fin = r["final"]
        row = dict(cond=r["cond"], seed=r["seed"], done=r["done"],
                   steps_trained=int(r["train"].global_step.max()),
                   steps_to_50=steps_to(c, 0.5), steps_to_80=steps_to(c, 0.8),
                   auc=float(np.nanmean(c)) if r["done"] else np.nan,
                   final_train_success=float(np.nanmean(c[-5:])) if r["done"] else np.nan,
                   final_eval_success=float((fin.outcome == "success").mean()) if fin is not None else np.nan,
                   phase1_end_step=(r["summary"] or {}).get("phase1_end_step") if r["cond"] in "BC" else None)
        if r["phase1"]:
            for t in SUBTASKS:
                row[f"phase1_{t}"] = r["phase1"][t]
            row["phase1_end_step"] = r["phase1"]["phase1_end_step"]
            row["phase1_reached_target"] = r["phase1"]["reached_target"]
        rows.append(row)
    per_seed = pd.DataFrame(rows).sort_values(["cond", "seed"])
    per_seed.to_csv(os.path.join(RES, f"{batch}_per_seed.csv"), index=False)

    # curves to CSV
    nb = int(np.ceil(total / BIN))
    cdf = pd.DataFrame({"step_end": (np.arange(nb) + 1) * BIN})
    for (cond, seed), c in sorted(curves.items()):
        cdf[f"{cond}_s{seed}"] = c
    cdf.to_csv(os.path.join(RES, f"{batch}_curves.csv"), index=False)

    plot_curves(curves, per_seed, nb, os.path.join(RES, f"{batch}_curve.png"))
    lines = summary_text(per_seed, runs)
    open(os.path.join(RES, f"{batch}_summary.txt"), "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))


def plot_curves(curves, per_seed, nb, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    # validated categorical palette (dataviz skill, light mode); line style is a second encoding
    colors = {"A": "#2a78d6", "B": "#eb6834", "C": "#1baf7a", "D": "#eda100"}
    styles = {"A": "-", "B": "-", "C": "--", "D": "-."}
    short = {"A": "A baseline", "B": "B skill filters", "C": "C no filtering", "D": "D sub-goal rewards"}
    x = (np.arange(nb) + 1) * BIN / 1e6
    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    ends = []
    for cond in "ABCD":
        cs = [c for (k, s), c in curves.items() if k == cond]
        if not cs:
            continue
        M = np.array(cs)
        n = len(cs)
        mean = np.nanmean(M, 0)
        ax.fill_between(x, np.nanmin(M, 0), np.nanmax(M, 0), color=colors[cond], alpha=0.15, lw=0)
        ax.plot(x, mean, color=colors[cond], lw=2, ls=styles[cond], label=f"{COND_NAME[cond]}  (n={n} seeds)")
        if cond in "BC":
            for v in per_seed[per_seed.cond == cond].phase1_end_step.dropna():
                ax.axvline(v / 1e6, color=colors[cond], ls=":", lw=0.8, alpha=0.6)
        last = np.where(~np.isnan(mean))[0]
        if len(last):
            ends.append([mean[last[-1]], short[cond]])
    # direct labels at the right edge, nudged apart so they never overlap
    ends.sort()
    for i in range(1, len(ends)):
        ends[i][0] = max(ends[i][0], ends[i - 1][0] + 0.05)
    for y, lab in ends:
        ax.text(x[-1] + 0.06, y, lab, va="center", fontsize=8, color="#333333")
    for thr in (0.5, 0.8):
        ax.axhline(thr, color="#999999", ls="--", lw=0.6)
    ax.set_xlabel("total environment steps (millions), every step counted, incl. skill training")
    ax.set_ylabel("success rate on the full task")
    ax.set_ylim(-0.02, 1.02)
    ax.set_xlim(0, x[-1])
    ax.set_title(f"Full-task success during training: mean across seeds, shading = min to max\n"
                 f"(dotted vertical lines: end of phase 1 for each B/C seed; {CONFIG['env']['size']}x"
                 f"{CONFIG['env']['size']} grid)", fontsize=10)
    ax.legend(loc="upper left", fontsize=8, frameon=False)
    ax.grid(alpha=0.2, lw=0.5)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    fig.tight_layout()
    fig.subplots_adjust(right=0.82)
    fig.savefig(path, dpi=130)
    plt.close(fig)


def summary_text(ps, runs):
    L = []
    L.append("=== per-condition summary (n = number of seeds; comparison: between-condition, independent seeds) ===")
    L.append(f"{'cond':<4} {'n':>2} {'to 50% (per seed)':<44} {'to 80% (per seed)':<44} "
             f"{'final eval success':>20} {'AUC':>12}")
    for cond in "ABCD":
        d = ps[ps.cond == cond]
        if d.empty:
            continue
        s50 = ", ".join(fmt_steps(v if not pd.isna(v) else None) for v in d.steps_to_50)
        s80 = ", ".join(fmt_steps(v if not pd.isna(v) else None) for v in d.steps_to_80)
        fe = d.final_eval_success
        L.append(f"{cond:<4} {len(d):>2} {s50:<44} {s80:<44} "
                 f"{fe.mean():>9.3f} ± {fe.std(ddof=1) if len(fe) > 1 else 0:.3f}   "
                 f"{d.auc.mean():.3f} ± {d.auc.std(ddof=1) if len(d) > 1 else 0:.3f}")
    L.append("")
    L.append("final eval success per seed:")
    for cond in "ABCD":
        d = ps[ps.cond == cond]
        if not d.empty:
            L.append(f"  {cond}: " + ", ".join(f"s{s}={v:.3f}" for s, v in zip(d.seed, d.final_eval_success)))
    total = CONFIG["total_steps"]

    def censored(d, col):
        return [v if not pd.isna(v) else total + BIN for v in d[col]]
    L.append("")
    L.append("=== verdict statistics (pre-registered in DECISIONS.md section 6) ===")
    A, B = ps[ps.cond == "A"], ps[ps.cond == "B"]
    for other in "ACD":
        O = ps[ps.cond == other]
        if other == "A":
            X, Y = B, A
            label = "B vs A (primary)"
        else:
            X, Y = B, O
            label = f"B vs {other} (explanatory)"
        if len(X) < 2 or len(Y) < 2:
            continue
        for col in ("steps_to_50", "steps_to_80"):
            x, y = censored(X, col), censored(Y, col)
            u, p = mann_whitney_less(x, y)
            L.append(f"{label} {col}: B median {np.median(x) / 1e6:.2f}M (reached {X[col].notna().sum()}/{len(X)}), "
                     f"{('A' if other == 'A' else other)} median {np.median(y) / 1e6:.2f}M "
                     f"(reached {Y[col].notna().sum()}/{len(Y)}); one-sided Mann-Whitney (B faster) p = {p:.3f}"
                     f"   [not reached = {(total + BIN) / 1e6:.1f}M]")
        u, p = mann_whitney_less([-v for v in X.auc], [-v for v in Y.auc])
        L.append(f"{label} AUC: B {X.auc.mean():.3f}, other {Y.auc.mean():.3f}; one-sided M-W (B higher) p = {p:.3f}")
        u, p = mann_whitney_less([-v for v in X.final_eval_success], [-v for v in Y.final_eval_success])
        L.append(f"{label} final success: B {X.final_eval_success.mean():.3f}, other "
                 f"{Y.final_eval_success.mean():.3f}; one-sided M-W (B higher) p = {p:.3f}")

    # phase 1
    L.append("")
    L.append("=== phase 1 (B, C): skill policy alone on each sub-task, 300 eval episodes each ===")
    for cond in "BC":
        d = ps[ps.cond == cond]
        if d.empty or "phase1_navigate" not in d:
            continue
        for _, r in d.iterrows():
            if pd.isna(r.get("phase1_navigate")):
                continue
            L.append(f"  {cond} s{r.seed}: " + ", ".join(f"{t} {r[f'phase1_{t}']:.2f}" for t in SUBTASKS)
                     + f"   phase 1 ended at {r.phase1_end_step / 1e6:.2f}M steps"
                     + ("" if r.phase1_reached_target else " (hit the 50% cap, target not reached)"))

    # controller usage and failure causes from the final eval
    L.append("")
    L.append("=== final evaluation: outcomes (500 episodes per seed, pooled over seeds; "
             "per-seed numbers in results/main_failures.csv) ===")
    frows = []
    for r in runs:
        f = r["final"]
        if f is None:
            continue
        for _, e in f.iterrows():
            frows.append(dict(cond=r["cond"], seed=r["seed"], **e.to_dict()))
    if frows:
        F = pd.DataFrame(frows)
        F.to_csv(os.path.join(RES, "main_final_episodes.csv"), index=False)
        tab = F.groupby(["cond", "outcome"]).size().unstack(fill_value=0)
        tab = (tab.T / tab.sum(1)).T.round(3)
        L.append(tab.to_string())
        per = F.groupby(["cond", "seed", "outcome"]).size().unstack(fill_value=0)
        per.to_csv(os.path.join(RES, "main_failures.csv"))
        L.append("")
        L.append("failures (lava/ball/timeout) in B and C broken down by the filter active at the last step:")
        for cond in "BC":
            G = F[(F.cond == cond) & (F.outcome != "success")]
            if G.empty:
                continue
            n_all = (F.cond == cond).sum()
            L.append(f"  {cond}: {len(G)} failures out of {n_all} episodes")
            ct = G.groupby(["filter_at_end", "outcome"]).size().unstack(fill_value=0)
            L.append("    " + ct.to_string().replace("\n", "\n    "))
            deaths = G[G.outcome.isin(["lava", "ball"])]
            if len(deaths) and cond == "C":
                L.append(f"    (C's skill policy sees everything, so nothing is hidden from it. Same count, read as: "
                         f"deaths to a hazard type the active sub-task never contained in training)")
            if len(deaths):
                L.append(f"    deaths where the active filter hides the hazard type that killed the agent: "
                         f"{deaths.killer_hidden.sum()} / {len(deaths)} deaths "
                         f"({deaths.killer_hidden.mean():.1%}); "
                         f"= {deaths.killer_hidden.sum() / n_all:.1%} of all episodes")
            to = G[G.outcome == "timeout"]
            if len(to):
                L.append(f"    timeouts: had key {to.got_key.mean():.0%}, had opened door {to.opened_door.mean():.0%}")
        for cond in "AD":
            G = F[(F.cond == cond) & (F.outcome == "timeout")]
            if len(G):
                L.append(f"  {cond} timeouts: had key {G.got_key.mean():.0%}, had opened door {G.opened_door.mean():.0%}")
        L.append("")
        L.append("controller filter usage during final evaluation (share of steps, mean over episodes):")
        for cond in "BC":
            G = F[F.cond == cond]
            if G.empty:
                continue
            L.append(f"  {cond}: " + ", ".join(f"{t} {G[f'frac_{t}'].mean():.1%}" for t in SUBTASKS))
            for s in sorted(G.seed.unique()):
                H = G[G.seed == s]
                L.append(f"     s{s}: " + ", ".join(f"{t} {H[f'frac_{t}'].mean():.1%}" for t in SUBTASKS))
    return L


def analyze_calib():
    total = CONFIG["total_steps"]
    L = ["=== calibration: condition A only, success of training episodes ==="]
    for batch in CONFIG["calib"]:
      L.append(f"--- {batch}: " + "; ".join(f"size {v['size']} lava {v['lava_frac']:.0%} max_steps {v['max_steps_mult']}*size^2 "
                                           f"{'agent-centred' if v.get('ego', 1) else 'fixed-map'} view"
                                           for v in CONFIG["calib"][batch]))
      for r in load_runs(batch):
        if r["train"] is None:
            continue
        c = binned_curve(r["train"], total)
        fin = r["final"]
        fe = (fin.outcome == "success").mean() if fin is not None else float("nan")
        done = np.sum(~np.isnan(c))
        L.append(f"size {r['size']:>2} seed {r['seed']}: trained {r['train'].global_step.max() / 1e6:.2f}M, "
                 f"last-500k training success {np.nanmean(c[max(0, done - 5):done]):.3f}, "
                 f"final eval success {fe:.3f}  " + ("(done)" if r["done"] else "(stopped early or running)"))
        L.append("    curve (per 500k): " + " ".join(f"{np.nanmean(c[i:i + 5]):.2f}" for i in range(0, done, 5)))
    for r in load_runs("sanity"):
        if r["train"] is None:
            continue
        t = r["train"]
        t = t.assign(bin=t.global_step // 500_000)
        g = t.groupby("bin").sum(numeric_only=True)
        L.append(f"sanity {r['name']}: sub-task training success per 500k steps:")
        for s in SUBTASKS:
            L.append(f"    {s:9s} " + " ".join(f"{a / max(b, 1):.2f}" for a, b in
                                            zip(g[f"sub_{s}_success"], g[f"sub_{s}_n"])))
        if r["phase1"]:
            L.append(f"    phase-1 eval (300 episodes each): {r['phase1']}")
    text = "\n".join(L)
    print(text)
    open(os.path.join(RES, "calib_summary.txt"), "w").write(text + "\n")


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "main"
    if which == "calib":
        analyze_calib()
    else:
        analyze_main(which)
