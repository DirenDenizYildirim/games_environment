"""Single-file PPO (CleanRL style) for the skill-filter experiment.

One script runs every condition:

    A  full-view baseline: one policy, full observation, full task, sparse reward
    D  same as A plus sub-goal bonuses (+0.2 key picked up, +0.2 door opened)
    B  phase 1: one skill policy trained on sub-task episodes, a filter sampled uniformly
       each episode, observation MASKED by that filter, filter id appended as one-hot.
       phase 2: skill policy frozen; a controller (same network) sees the full observation
       and picks the active filter every K env steps, trained with PPO on the full task.
    C  identical to B except the skill policy always sees the UNMASKED observation.

Every environment step (phase 1, phase 2, training rollouts) counts toward --total-steps.
Evaluation episodes do not train anything and are not counted.

Writes to --out:
    train.csv          one row per PPO update (curve data, outcome counts, filter usage)
    phase1_eval.json   (B, C) per-sub-task success of the skill policy at the end of phase 1
    final_eval.csv     one row per final evaluation episode on the full task
    final.json         summary + "done" marker
    ckpt.pt            checkpoint for resuming an interrupted run
"""
import argparse
import csv
import json
import os
import time
from collections import Counter, deque

import numpy as np
import torch
import torch.nn as nn
from torch.distributions import Categorical

from skillenv import N_STATES, N_TYPES, SUBTASKS, SkillFilterEnv, apply_filter, FILTER_HIDES, LAVA, BALL

OUTCOMES = ("success", "lava", "ball", "timeout")
N_ACTIONS = 7


def parse_args(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--cond", choices="ABCD", required=True)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--size", type=int, default=9)
    p.add_argument("--lava-frac", type=float, default=0.08)
    p.add_argument("--max-steps-mult", type=int, default=4, help="episode limit = mult * size^2")
    p.add_argument("--total-steps", type=int, default=2_000_000)
    p.add_argument("--out", required=True)
    # PPO hyperparameters: identical for every condition and for both phases
    p.add_argument("--num-envs", type=int, default=16)
    p.add_argument("--num-steps", type=int, default=128)
    p.add_argument("--lr", type=float, default=5e-4)
    p.add_argument("--gamma", type=float, default=0.99)
    p.add_argument("--gae-lambda", type=float, default=0.95)
    p.add_argument("--update-epochs", type=int, default=4)
    p.add_argument("--num-minibatches", type=int, default=4)
    p.add_argument("--clip-coef", type=float, default=0.2)
    p.add_argument("--ent-coef", type=float, default=0.01)
    p.add_argument("--vf-coef", type=float, default=0.5)
    p.add_argument("--max-grad-norm", type=float, default=0.5)
    # skill-filter method
    p.add_argument("--K", type=int, default=4, help="controller picks a filter every K env steps")
    p.add_argument("--phase1-max-frac", type=float, default=0.5)
    p.add_argument("--phase1-target", type=float, default=0.9)
    p.add_argument("--freeze-skill", type=int, default=1)
    p.add_argument("--phase1-only", type=int, default=0, help="sanity check: stop after phase 1")
    # evaluation / bookkeeping
    p.add_argument("--final-eval-episodes", type=int, default=500)
    p.add_argument("--phase1-eval-episodes", type=int, default=300)
    p.add_argument("--ckpt-every", type=int, default=25, help="updates between checkpoints")
    return p.parse_args(argv)


# ---------------------------------------------------------------------------- network
class Agent(nn.Module):
    """Same architecture for every policy in every condition (skill, baseline, controller)."""

    def __init__(self, size, n_actions, n_task=len(SUBTASKS)):
        super().__init__()
        c = N_TYPES + N_STATES
        self.n_task = n_task
        self.conv = nn.Sequential(
            nn.Conv2d(c, 16, 3, padding=1), nn.ReLU(),
            nn.Conv2d(16, 32, 3, padding=1), nn.ReLU(),
            nn.Conv2d(32, 32, 3, stride=2, padding=1), nn.ReLU(),
            nn.Flatten(),
        )
        with torch.no_grad():
            flat = self.conv(torch.zeros(1, c, size, size)).shape[1]
        self.fc = nn.Sequential(nn.Linear(flat + n_task, 128), nn.ReLU())
        self.actor = nn.Linear(128, n_actions)
        self.critic = nn.Linear(128, 1)
        nn.init.orthogonal_(self.actor.weight, 0.01); nn.init.zeros_(self.actor.bias)
        nn.init.orthogonal_(self.critic.weight, 1.0); nn.init.zeros_(self.critic.bias)

    def features(self, obs, task):
        # obs: (B, W, H, 2) integer (type, state) -> one-hot planes (B, 15, W, H)
        obs = obs.long()
        x = torch.cat([nn.functional.one_hot(obs[..., 0], N_TYPES),
                       nn.functional.one_hot(obs[..., 1].clamp(max=N_STATES - 1), N_STATES)], -1)
        x = x.permute(0, 3, 1, 2).float()
        return self.fc(torch.cat([self.conv(x), task], 1))

    def get_value(self, obs, task):
        return self.critic(self.features(obs, task)).squeeze(-1)

    def get_action_and_value(self, obs, task, action=None):
        h = self.features(obs, task)
        dist = Categorical(logits=self.actor(h))
        if action is None:
            action = dist.sample()
        return action, dist.log_prob(action), dist.entropy(), self.critic(h).squeeze(-1)


def onehot(ids, n=len(SUBTASKS)):
    out = np.zeros((len(ids), n), dtype=np.float32)
    for i, t in enumerate(ids):
        if t is not None and t >= 0:
            out[i, t] = 1.0
    return out


# ---------------------------------------------------------------------------- PPO update
def ppo_update(agent, opt, b, args):
    """b: dict of flat tensors obs, task, actions, logprobs, advantages, returns."""
    n = b["actions"].shape[0]
    mb = n // args.num_minibatches
    stats = Counter()
    for _ in range(args.update_epochs):
        idx = torch.randperm(n)
        for s in range(0, n, mb):
            j = idx[s:s + mb]
            _, newlogp, ent, v = agent.get_action_and_value(b["obs"][j], b["task"][j], b["actions"][j])
            ratio = (newlogp - b["logprobs"][j]).exp()
            adv = b["advantages"][j]
            adv = (adv - adv.mean()) / (adv.std() + 1e-8)
            pg = torch.max(-adv * ratio, -adv * ratio.clamp(1 - args.clip_coef, 1 + args.clip_coef)).mean()
            vloss = 0.5 * ((v - b["returns"][j]) ** 2).mean()
            loss = pg - args.ent_coef * ent.mean() + args.vf_coef * vloss
            opt.zero_grad()
            loss.backward()
            nn.utils.clip_grad_norm_(agent.parameters(), args.max_grad_norm)
            opt.step()
            stats["pg"] += pg.item(); stats["v"] += vloss.item(); stats["ent"] += ent.mean().item()
            stats["n"] += 1
    return {k: stats[k] / stats["n"] for k in ("pg", "v", "ent")}


def gae(rewards, values, dones, next_value, next_done, gamma, lam):
    T = rewards.shape[0]
    adv = torch.zeros_like(rewards)
    last = 0
    for t in reversed(range(T)):
        nonterm = 1.0 - (next_done if t == T - 1 else dones[t + 1])
        nv = next_value if t == T - 1 else values[t + 1]
        delta = rewards[t] + gamma * nv * nonterm - values[t]
        adv[t] = last = delta + gamma * lam * nonterm * last
    return adv, adv + values


# ---------------------------------------------------------------------------- run state
class Run:
    def __init__(self, args):
        self.args = args
        self.cond = args.cond
        os.makedirs(args.out, exist_ok=True)
        torch.manual_seed(args.seed)
        self.rng = np.random.default_rng(args.seed + 12345)
        self.skill = Agent(args.size, N_ACTIONS)
        self.skill_opt = torch.optim.Adam(self.skill.parameters(), lr=args.lr, eps=1e-5)
        self.ctrl = self.ctrl_opt = None
        if self.cond in "BC":
            self.ctrl = Agent(args.size, len(SUBTASKS))
            self.ctrl_opt = torch.optim.Adam(self.ctrl.parameters(), lr=args.lr, eps=1e-5)
        self.global_step = 0
        self.update = 0
        self.phase = 1 if self.cond in "BC" else 0  # 0 = single-phase (A, D)
        self.phase1_end_step = None
        self.sub_hist = {t: deque(maxlen=100) for t in range(len(SUBTASKS))}
        self.csv_path = os.path.join(args.out, "train.csv")
        self.ckpt_path = os.path.join(args.out, "ckpt.pt")
        self._resume()

    # -- persistence
    def _resume(self):
        if not os.path.exists(self.ckpt_path):
            if os.path.exists(self.csv_path):
                os.remove(self.csv_path)
            return
        ck = torch.load(self.ckpt_path, weights_only=False)
        self.skill.load_state_dict(ck["skill"]); self.skill_opt.load_state_dict(ck["skill_opt"])
        if self.ctrl is not None:
            self.ctrl.load_state_dict(ck["ctrl"]); self.ctrl_opt.load_state_dict(ck["ctrl_opt"])
        for k in ("global_step", "update", "phase", "phase1_end_step", "sub_hist"):
            setattr(self, k, ck[k])
        torch.set_rng_state(ck["torch_rng"]); self.rng = ck["np_rng"]
        # drop curve rows written after the checkpoint
        if os.path.exists(self.csv_path):
            with open(self.csv_path) as f:
                rows = list(csv.DictReader(f))
            keep = [r for r in rows if int(r["global_step"]) <= self.global_step]
            if rows:
                with open(self.csv_path, "w", newline="") as f:
                    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
                    w.writeheader(); w.writerows(keep)
        print(f"resumed {self.args.out} at step {self.global_step} (phase {self.phase})", flush=True)

    def save(self):
        ck = dict(skill=self.skill.state_dict(), skill_opt=self.skill_opt.state_dict(),
                  global_step=self.global_step, update=self.update, phase=self.phase,
                  phase1_end_step=self.phase1_end_step, sub_hist=self.sub_hist,
                  torch_rng=torch.get_rng_state(), np_rng=self.rng)
        if self.ctrl is not None:
            ck.update(ctrl=self.ctrl.state_dict(), ctrl_opt=self.ctrl_opt.state_dict())
        tmp = self.ckpt_path + ".tmp"
        torch.save(ck, tmp)
        os.replace(tmp, self.ckpt_path)

    def log(self, row):
        new = not os.path.exists(self.csv_path)
        with open(self.csv_path, "a", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(row.keys()))
            if new:
                w.writeheader()
            w.writerow(row)

    # -- environments
    def make_envs(self, mode, base_seed):
        envs = [SkillFilterEnv(size=self.args.size, mode=mode, subgoal_bonus=(self.cond == "D"),
                               **self.env_kw())
                for _ in range(self.args.num_envs)]
        obs = []
        for i, e in enumerate(envs):
            o, _ = e.reset(seed=base_seed + i)
            obs.append(o["image"])
        return envs, np.stack(obs)

    def env_kw(self):
        return dict(lava_frac=self.args.lava_frac, max_steps=self.args.max_steps_mult * self.args.size ** 2)

    def skill_input(self, obs, tasks):
        """Observation fed to the skill policy: masked by filter for B, raw for C/A/D."""
        if self.cond == "B":
            obs = np.stack([apply_filter(o, SUBTASKS[t]) for o, t in zip(obs, tasks)])
        return torch.as_tensor(obs), torch.as_tensor(onehot(tasks))

    # ------------------------------------------------------------------ single-phase (A, D)
    # and phase 1 (B, C) share one loop: the policy acts every env step.
    def train_flat(self, budget_end):
        a = self.args
        sub = self.phase == 1
        envs, obs = self.make_envs("full", a.seed * 100_000 + self.global_step)
        tasks = [-1] * a.num_envs
        if sub:
            for i, e in enumerate(envs):
                tasks[i] = int(self.rng.integers(len(SUBTASKS)))
                e.set_mode(SUBTASKS[tasks[i]])
                obs[i] = e.reset()[0]["image"]
        done = torch.zeros(a.num_envs)
        T, N = a.num_steps, a.num_envs
        while self.global_step < budget_end:
            t0 = time.time()
            buf = {k: [] for k in ("obs", "task", "actions", "logprobs", "rewards", "dones", "values")}
            cnt = Counter()
            for _ in range(T):
                o_t, k_t = self.skill_input(obs, tasks)
                with torch.no_grad():
                    act, logp, _, val = self.skill.get_action_and_value(o_t, k_t)
                buf["obs"].append(o_t); buf["task"].append(k_t); buf["actions"].append(act)
                buf["logprobs"].append(logp); buf["values"].append(val); buf["dones"].append(done)
                rew = np.zeros(N, dtype=np.float32); nd = np.zeros(N, dtype=np.float32)
                for i, e in enumerate(envs):
                    o, r, term, trunc, info = e.step(int(act[i]))
                    rew[i] = r
                    if term or trunc:
                        nd[i] = 1.0
                        oc = info["outcome"]
                        if sub:
                            cnt[f"sub{tasks[i]}_n"] += 1
                            cnt[f"sub{tasks[i]}_success"] += oc == "success"
                            self.sub_hist[tasks[i]].append(oc == "success")
                            tasks[i] = int(self.rng.integers(len(SUBTASKS)))
                            e.set_mode(SUBTASKS[tasks[i]])
                        else:
                            cnt["episodes"] += 1; cnt[oc] += 1
                        o = e.reset()[0]
                    obs[i] = o["image"]
                buf["rewards"].append(torch.as_tensor(rew))
                done = torch.as_tensor(nd)
                self.global_step += N
            o_t, k_t = self.skill_input(obs, tasks)
            with torch.no_grad():
                nv = self.skill.get_value(o_t, k_t)
            st = {k: torch.stack(v) for k, v in buf.items()}
            adv, ret = gae(st["rewards"], st["values"], st["dones"], nv, done, a.gamma, a.gae_lambda)
            b = dict(obs=st["obs"].reshape(T * N, *obs.shape[1:]), task=st["task"].reshape(T * N, -1),
                     actions=st["actions"].reshape(-1), logprobs=st["logprobs"].reshape(-1),
                     advantages=adv.reshape(-1), returns=ret.reshape(-1))
            ls = ppo_update(self.skill, self.skill_opt, b, a)
            self.update += 1
            row = self.base_row(ls, cnt, t0, T * N)
            if sub:
                for t in range(len(SUBTASKS)):
                    row[f"sub_{SUBTASKS[t]}_n"] = cnt[f"sub{t}_n"]
                    row[f"sub_{SUBTASKS[t]}_success"] = cnt[f"sub{t}_success"]
            self.log(row)
            if self.update % a.ckpt_every == 0:
                self.save()
            if sub and self.phase1_done():
                return
        if self.update % a.ckpt_every:
            self.save()

    def phase1_done(self):
        return all(len(h) == h.maxlen and np.mean(h) >= self.args.phase1_target
                   for h in self.sub_hist.values())

    def base_row(self, ls, cnt, t0, nsteps):
        row = dict(global_step=self.global_step, update=self.update, phase=self.phase,
                   episodes=cnt["episodes"], **{o: cnt[o] for o in OUTCOMES},
                   pg_loss=round(ls["pg"], 5), v_loss=round(ls["v"], 5), entropy=round(ls["ent"], 4),
                   sps=int(nsteps / (time.time() - t0)))
        return row

    # ------------------------------------------------------------------ phase 2 (B, C)
    def macro_step(self, envs, obs, filt, live, info_out):
        """Run up to K env steps per env with the frozen skill policy under filter `filt`.
        Returns summed reward, done flags, steps taken. Finished envs are reset in place."""
        a = self.args
        N = len(envs)
        R = np.zeros(N, dtype=np.float32); D = np.zeros(N, dtype=np.float32)
        active = np.ones(N, dtype=bool)
        steps = 0
        for _ in range(a.K):
            idx = np.nonzero(active)[0]
            if len(idx) == 0:
                break
            o_t, k_t = self.skill_input(obs[idx], [filt[i] for i in idx])
            with torch.no_grad():
                act, *_ = self.skill.get_action_and_value(o_t, k_t)
            for j, i in enumerate(idx):
                o, r, term, trunc, info = envs[i].step(int(act[j]))
                steps += 1
                R[i] += r
                if term or trunc:
                    D[i] = 1.0; active[i] = False
                    info_out.append((info, filt[i], live[i]))
                    live[i] = Counter()
                    o = envs[i].reset()[0]
                obs[i] = o["image"]
        return R, D, steps

    def train_controller(self, budget_end):
        a = self.args
        envs, obs = self.make_envs("full", a.seed * 100_000 + self.global_step + 7)
        live = [Counter() for _ in envs]  # filter usage within the current episode
        done = torch.zeros(a.num_envs)
        T, N = a.num_steps, a.num_envs
        g = a.gamma ** a.K  # same per-env-step discount as every other policy
        while self.global_step < budget_end:
            t0 = time.time(); s0 = self.global_step
            buf = {k: [] for k in ("obs", "task", "actions", "logprobs", "rewards", "dones", "values")}
            cnt = Counter()
            zero_task = torch.zeros(N, len(SUBTASKS))
            for _ in range(T):
                o_t = torch.as_tensor(obs)
                with torch.no_grad():
                    f, logp, _, val = self.ctrl.get_action_and_value(o_t, zero_task)
                fl = f.tolist()
                for i, x in enumerate(fl):
                    cnt[f"choose_{SUBTASKS[x]}"] += 1; live[i][x] += 1
                buf["obs"].append(o_t); buf["task"].append(zero_task); buf["actions"].append(f)
                buf["logprobs"].append(logp); buf["values"].append(val); buf["dones"].append(done)
                ended = []
                R, D, steps = self.macro_step(envs, obs, fl, live, ended)
                for info, fx, _ in ended:
                    oc = info["outcome"]
                    cnt["episodes"] += 1; cnt[oc] += 1
                    cnt[f"{oc}_under_{SUBTASKS[fx]}"] += 1
                buf["rewards"].append(torch.as_tensor(R))
                done = torch.as_tensor(D)
                self.global_step += steps
            with torch.no_grad():
                nv = self.ctrl.get_value(torch.as_tensor(obs), zero_task)
            st = {k: torch.stack(v) for k, v in buf.items()}
            adv, ret = gae(st["rewards"], st["values"], st["dones"], nv, done, g, a.gae_lambda)
            b = dict(obs=st["obs"].reshape(T * N, *obs.shape[1:]), task=st["task"].reshape(T * N, -1),
                     actions=st["actions"].reshape(-1), logprobs=st["logprobs"].reshape(-1),
                     advantages=adv.reshape(-1), returns=ret.reshape(-1))
            ls = ppo_update(self.ctrl, self.ctrl_opt, b, a)
            self.update += 1
            row = self.base_row(ls, cnt, t0, self.global_step - s0)
            for fx in SUBTASKS:
                row[f"choose_{fx}"] = cnt[f"choose_{fx}"]
                for oc in OUTCOMES:
                    row[f"{oc}_under_{fx}"] = cnt[f"{oc}_under_{fx}"]
            self.log(row)
            if self.update % a.ckpt_every == 0:
                self.save()
        if self.update % a.ckpt_every:
            self.save()

    # ------------------------------------------------------------------ evaluation
    def eval_subtasks(self):
        """Skill policy alone on each sub-task (its own filter / raw for C). Not counted in budget."""
        a = self.args
        res = {}
        for t, name in enumerate(SUBTASKS):
            env = SkillFilterEnv(size=a.size, mode=name, **self.env_kw())
            succ = 0
            for ep in range(a.phase1_eval_episodes):
                o = env.reset(seed=10_000_000 + ep)[0]["image"][None]
                while True:
                    o_t, k_t = self.skill_input(o, [t])
                    with torch.no_grad():
                        act, *_ = self.skill.get_action_and_value(o_t, k_t)
                    oo, r, term, trunc, info = env.step(int(act[0]))
                    o = oo["image"][None]
                    if term or trunc:
                        succ += info["outcome"] == "success"
                        break
            res[name] = succ / a.phase1_eval_episodes
        return res

    def final_eval(self):
        """Full task, fresh layouts (seeds disjoint from training), stochastic policy as trained."""
        a = self.args
        rows = []
        n_par = 25
        envs = [SkillFilterEnv(size=a.size, mode="full", **self.env_kw()) for _ in range(n_par)]
        next_ep = 0
        obs = np.zeros((n_par, a.size, a.size, 2), dtype=np.uint8)
        ep_id = [None] * n_par
        usage = [Counter() for _ in range(n_par)]
        cur_f = [0] * n_par
        tstep = [0] * n_par

        def start(i):
            nonlocal next_ep
            ep_id[i] = next_ep
            obs[i] = envs[i].reset(seed=20_000_000 + next_ep)[0]["image"]
            usage[i] = Counter(); tstep[i] = 0
            next_ep += 1

        for i in range(n_par):
            start(i)
        active = [True] * n_par
        while any(active):
            idx = [i for i in range(n_par) if active[i]]
            if self.cond in "AD":
                o_t = torch.as_tensor(obs[idx]); k_t = torch.zeros(len(idx), len(SUBTASKS))
                with torch.no_grad():
                    act, *_ = self.skill.get_action_and_value(o_t, k_t)
            else:
                need = [i for i in idx if tstep[i] % a.K == 0]
                if need:
                    with torch.no_grad():
                        f, *_ = self.ctrl.get_action_and_value(torch.as_tensor(obs[need]),
                                                               torch.zeros(len(need), len(SUBTASKS)))
                    for i, x in zip(need, f.tolist()):
                        cur_f[i] = x
                o_t, k_t = self.skill_input(obs[idx], [cur_f[i] for i in idx])
                with torch.no_grad():
                    act, *_ = self.skill.get_action_and_value(o_t, k_t)
            for j, i in enumerate(idx):
                if self.cond in "BC":
                    usage[i][cur_f[i]] += 1
                o, r, term, trunc, info = envs[i].step(int(act[j]))
                tstep[i] += 1
                if term or trunc:
                    oc = info["outcome"]
                    row = dict(episode=ep_id[i], outcome=oc, length=tstep[i],
                               got_key=int(info["got_key"]), opened_door=int(info["opened_door"]))
                    if self.cond in "BC":
                        fname = SUBTASKS[cur_f[i]]
                        hidden = FILTER_HIDES[fname]
                        row["filter_at_end"] = fname
                        row["killer_hidden"] = int((oc == "lava" and LAVA in hidden) or
                                                   (oc == "ball" and BALL in hidden))
                        for t, name in enumerate(SUBTASKS):
                            row[f"frac_{name}"] = round(usage[i][t] / tstep[i], 4)
                    else:
                        row["filter_at_end"] = "none"
                        row["killer_hidden"] = 0
                    rows.append(row)
                    if next_ep < a.final_eval_episodes:
                        start(i)
                    else:
                        active[i] = False
                else:
                    obs[i] = o["image"]
        rows.sort(key=lambda r: r["episode"])
        with open(os.path.join(a.out, "final_eval.csv"), "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader(); w.writerows(rows)
        return rows

    # ------------------------------------------------------------------ driver
    def run(self):
        a = self.args
        t_start = time.time()
        if self.phase == 0:
            self.train_flat(a.total_steps)
        else:
            if self.phase == 1:
                self.train_flat(int(a.phase1_max_frac * a.total_steps))
                self.phase1_end_step = self.global_step
                p1 = self.eval_subtasks()
                p1.update(phase1_end_step=self.global_step, reached_target=self.phase1_done())
                with open(os.path.join(a.out, "phase1_eval.json"), "w") as f:
                    json.dump(p1, f, indent=1)
                print(f"{a.out}: phase 1 ended at {self.global_step}: {p1}", flush=True)
                self.phase = 2
                self.save()
                if a.phase1_only:
                    with open(os.path.join(a.out, "final.json"), "w") as f:
                        json.dump(dict(vars(a), phase1=p1, done=True), f, indent=1)
                    return
            if not a.freeze_skill:
                raise NotImplementedError("unfrozen phase 2 is an optional extension")
            self.train_controller(a.total_steps)
        rows = self.final_eval()
        succ = float(np.mean([r["outcome"] == "success" for r in rows]))
        summary = dict(vars(a), final_success=succ, global_step=self.global_step,
                       phase1_end_step=self.phase1_end_step, wall_seconds_last_session=time.time() - t_start,
                       done=True)
        with open(os.path.join(a.out, "final.json"), "w") as f:
            json.dump(summary, f, indent=1)
        print(f"{a.out}: done, final success {succ:.3f}", flush=True)


if __name__ == "__main__":
    args = parse_args()
    torch.set_num_threads(1)
    if os.path.exists(os.path.join(args.out, "final.json")):
        print(f"{args.out} already complete")
    else:
        Run(args).run()
