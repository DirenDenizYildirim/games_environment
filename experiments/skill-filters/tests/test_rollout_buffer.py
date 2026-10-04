"""Regression test: rollout buffers must store each step's own observation.

A bug (fixed) stored torch.as_tensor(obs) views of an array the env loop overwrote in place,
so every stored observation silently became the last one. Conditions A, C, D and both
controllers trained on garbage while B's skill policy (whose masking copies) did not.

    python -m pytest tests/  (or: python tests/test_rollout_buffer.py)
"""
import os
import sys
import tempfile

import numpy as np
import torch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import ppo  # noqa: E402


def _captured_obs(cond, phase2=False):
    out = tempfile.mkdtemp()
    args = ppo.parse_args(["--cond", cond, "--size", "7", "--out", out, "--num-envs", "2",
                           "--num-steps", "8", "--total-steps", "16"])
    run = ppo.Run(args)
    seen = []
    agent = run.ctrl if phase2 else run.skill
    orig = agent.get_action_and_value

    def spy(obs, task, action=None):
        if action is None:  # rollout call (not the update call)
            seen.append((obs, obs.clone()))
        return orig(obs, task, action)
    agent.get_action_and_value = spy
    if phase2:
        run.phase = 2
        run.train_controller(16)
    else:
        if cond in "BC":
            run.phase = 1
        run.train_flat(16)
    return seen


def check(cond, phase2=False):
    seen = _captured_obs(cond, phase2)
    assert len(seen) >= 2
    for stored, snapshot in seen:
        assert torch.equal(stored, snapshot), f"{cond}: stored rollout obs changed after it was recorded"
    distinct = {tuple(s.flatten().tolist()) for s, _ in seen}
    assert len(distinct) > 1, f"{cond}: all rollout observations identical"


def test_flat_policies():
    for cond in "ABCD":
        check(cond)


def test_controllers():
    for cond in "BC":
        check(cond, phase2=True)


if __name__ == "__main__":
    test_flat_policies(); test_controllers(); print("ok")
