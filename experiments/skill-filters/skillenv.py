"""The custom MiniGrid "full task" plus its three skill sub-tasks and filters.

Layout (re-randomised every episode):

    +-----------+---------------+
    | agent     |   moving ball |
    | key       D   (blue)      |
    |   lava    |  lava   goal  |
    +-----------+---------------+

* A vertical wall splits the grid into two rooms. It has one locked yellow door (D).
* The agent and the yellow key start in the left room; the green goal is in the right room.
* Lava cells are scattered in both rooms; blue balls move randomly in the right room.
* Every layout is checked with breadth-first search so it is always solvable.

Modes:
    "full"      everything live (the real task)
    "navigate"  lava/balls/key removed, door unlocked (closed): reach the goal
    "hazard"    key removed, door already open: reach the goal without touching a hazard
    "key_door"  lava/balls/goal removed: pick up the key (+0.2) then open the door (success)

Observations are the FULL grid (not the 7x7 egocentric view): an int array of shape
(size, size, 2) holding (object type, state) for each cell. The agent cell holds
type=agent, state=direction. Colour is dropped because every object type here has a
single fixed colour, so it carries no information.
"""
from collections import deque

import numpy as np
from minigrid.core.constants import OBJECT_TO_IDX
from minigrid.core.grid import Grid
from minigrid.core.mission import MissionSpace
from minigrid.core.world_object import Ball, Door, Goal, Key, Lava, Wall
from minigrid.minigrid_env import MiniGridEnv

EMPTY, WALL, DOOR, KEY, BALL, GOAL, LAVA, AGENT = (
    OBJECT_TO_IDX[k] for k in ("empty", "wall", "door", "key", "ball", "goal", "lava", "agent")
)
N_TYPES = 11  # MiniGrid object-type vocabulary size
N_STATES = 4  # door state (0 open, 1 closed, 2 locked) or agent direction (0..3)

SUBTASKS = ("navigate", "hazard", "key_door")
# Object types each filter lets through. Walls and the agent are always visible.
FILTER_VISIBLE = {
    "navigate": {WALL, DOOR, GOAL},
    "hazard": {WALL, LAVA, BALL, GOAL},
    "key_door": {WALL, KEY, DOOR},
}
# Which hazard types each filter hides (used for the failure-cause breakdown).
FILTER_HIDES = {f: {LAVA, BALL} - vis for f, vis in FILTER_VISIBLE.items()}

KEY_BONUS = 0.2  # sub-goal bonus for picking up the key (key_door sub-task and condition D)
DOOR_BONUS = 0.2  # sub-goal bonus for opening the door (condition D only)


def apply_filter(obs, filt):
    """Mask an observation (H, W, 2) or batch (..., H, W, 2): hidden types become empty floor."""
    if filt is None:
        return obs
    out = obs.copy()
    t = out[..., 0]
    keep = np.isin(t, list(FILTER_VISIBLE[filt] | {AGENT, EMPTY}))
    out[..., 0] = np.where(keep, t, EMPTY)
    out[..., 1] = np.where(keep, out[..., 1], 0)
    return out


class SkillFilterEnv(MiniGridEnv):
    def __init__(self, size=9, mode="full", subgoal_bonus=False, lava_frac=0.08, n_balls=None,
                 max_steps=None, **kwargs):
        assert mode in ("full",) + SUBTASKS
        self.mode = mode
        self.subgoal_bonus = subgoal_bonus  # condition D
        self.lava_frac = lava_frac
        self.n_balls = n_balls if n_balls is not None else (1 if size < 11 else 2)
        super().__init__(
            mission_space=MissionSpace(mission_func=lambda: "get the key, open the door, reach the goal"),
            grid_size=size,
            max_steps=max_steps or 4 * size * size,
            see_through_walls=True,
            **kwargs,
        )

    def set_mode(self, mode):
        """Takes effect on the next reset."""
        assert mode in ("full",) + SUBTASKS
        self.mode = mode

    # ------------------------------------------------------------------ layout
    def _gen_grid(self, width, height):
        for _ in range(1000):
            if self._try_layout(width, height):
                break
        else:
            raise RuntimeError("could not generate a solvable layout")
        self._apply_mode()
        self.mission = "get the key, open the door, reach the goal"

    def _try_layout(self, W, H):
        rng = self.np_random
        self.grid = Grid(W, H)
        self.grid.wall_rect(0, 0, W, H)
        wx = int(rng.integers(3, W - 3))  # wall column; each room >= 2 interior columns
        for y in range(H):
            self.grid.set(wx, y, Wall())
        dy = int(rng.integers(1, H - 1))
        self.door = Door("yellow", is_locked=True)
        self.door_pos = (wx, dy)
        self.grid.set(wx, dy, self.door)
        left = [(x, y) for x in range(1, wx) for y in range(1, H - 1)]
        right = [(x, y) for x in range(wx + 1, W - 1) for y in range(1, H - 1)]
        door_front, door_back = (wx - 1, dy), (wx + 1, dy)

        def pick(cells, taken):
            free = [c for c in cells if c not in taken]
            return free[int(rng.integers(len(free)))]

        taken = {door_front, door_back}
        self.agent_pos = pick(left, taken); taken.add(self.agent_pos)
        self.agent_dir = int(rng.integers(4))
        self.key_pos = pick(left, taken); taken.add(self.key_pos)
        self.goal_pos = pick(right, taken); taken.add(self.goal_pos)
        n_lava = max(1, round(self.lava_frac * (len(left) + len(right))))
        self.lava_pos = []
        for _ in range(n_lava):
            c = pick(left + right, taken); taken.add(c); self.lava_pos.append(c)
        self.ball_start = []
        for _ in range(self.n_balls):
            c = pick(right, taken); taken.add(c); self.ball_start.append(c)

        blocked = {(wx, y) for y in range(H)} | set(self.lava_pos)
        # agent -> a free neighbour of the key, agent -> door front, door back -> goal
        reach_left = self._bfs(self.agent_pos, blocked | {self.key_pos})
        key_ok = any(n in reach_left for n in self._nbrs(self.key_pos))
        door_ok = door_front in reach_left
        reach_right = self._bfs(door_back, blocked)
        goal_ok = self.goal_pos in reach_right
        return key_ok and door_ok and goal_ok

    def _nbrs(self, c):
        x, y = c
        return [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]

    def _bfs(self, start, blocked):
        W, H = self.width, self.height
        seen, q = {start}, deque([start])
        while q:
            c = q.popleft()
            for n in self._nbrs(c):
                if 0 < n[0] < W - 1 and 0 < n[1] < H - 1 and n not in blocked and n not in seen:
                    seen.add(n); q.append(n)
        return seen

    def _apply_mode(self):
        """Place objects, making the ones irrelevant to the active sub-task inert (= absent)."""
        m = self.mode
        if m in ("full", "key_door"):
            self.grid.set(*self.key_pos, Key("yellow"))
        if m == "navigate":
            self.door.is_locked = False  # closed but unlocked
        elif m == "hazard":
            self.door.is_locked, self.door.is_open = False, True
        if m != "key_door":
            self.grid.set(*self.goal_pos, Goal())
        if m in ("full", "hazard"):
            for c in self.lava_pos:
                self.grid.set(*c, Lava())
            self.balls = []
            for c in self.ball_start:
                b = Ball("blue"); self.grid.set(*c, b); b.init_pos = b.cur_pos = c
                self.balls.append(b)
        else:
            self.balls = []
        self.got_key = False
        self.opened_door = False

    # ------------------------------------------------------------------ dynamics
    def step(self, action):
        fwd = self.grid.get(*self.front_pos)
        hit_ball = action == self.actions.forward and fwd is not None and fwd.type == "ball"
        hit_lava = action == self.actions.forward and fwd is not None and fwd.type == "lava"

        # balls move first (into a random free cell of their 3x3 neighbourhood, never onto the agent)
        if not hit_ball:
            for b in self.balls:
                old = tuple(b.cur_pos)
                try:
                    self.place_obj(b, top=(old[0] - 1, old[1] - 1), size=(3, 3), max_tries=20)
                    self.grid.set(*old, None)
                except Exception:
                    pass

        obs, reward, terminated, truncated, info = super().step(action)
        outcome = None
        if hit_ball:
            terminated, reward, outcome = True, 0.0, "ball"
        elif hit_lava:
            outcome = "lava"  # base class already terminated with reward 0
        elif terminated and reward > 0:
            outcome = "success"

        if not self.got_key and self.carrying is not None and self.carrying.type == "key":
            self.got_key = True
            if self.mode == "key_door" or self.subgoal_bonus:
                reward += KEY_BONUS
        if not self.opened_door and self.door.is_open:
            self.opened_door = True
            if self.mode == "key_door":
                terminated, outcome = True, "success"
                reward += self._reward()
            elif self.subgoal_bonus:
                reward += DOOR_BONUS
        if outcome is None and truncated and not terminated:
            outcome = "timeout"
        info = {"outcome": outcome, "got_key": self.got_key, "opened_door": self.opened_door}
        return obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------ observation
    def gen_obs(self):
        W, H = self.width, self.height
        arr = np.zeros((W, H, 2), dtype=np.uint8)
        arr[..., 0] = EMPTY
        for i in range(W):
            for j in range(H):
                v = self.grid.get(i, j)
                if v is not None:
                    e = v.encode()
                    arr[i, j, 0], arr[i, j, 1] = e[0], e[2]
        arr[self.agent_pos[0], self.agent_pos[1]] = (AGENT, self.agent_dir)
        return {"image": arr, "direction": self.agent_dir, "mission": self.mission}


def render_ascii(obs):
    """Tiny text rendering of an (W, H, 2) observation, for the mask sanity check."""
    ch = {EMPTY: ".", WALL: "#", DOOR: "D", KEY: "k", BALL: "o", GOAL: "G", LAVA: "~"}
    arrows = ">v<^"
    W, H = obs.shape[:2]
    rows = []
    for y in range(H):
        row = ""
        for x in range(W):
            t, s = int(obs[x, y, 0]), int(obs[x, y, 1])
            if t == AGENT:
                row += arrows[s]
            elif t == DOOR:
                row += "DdO"[2 - s] if s in (0, 1, 2) else "D"  # D locked, d closed, O open
            else:
                row += ch.get(t, "?")
        rows.append(row)
    return "\n".join(rows)
