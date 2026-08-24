# DERIVATION — chaos-games — 2026-08-24

**Question under test:** is §7.1's variance integral consistent with §6.2's own statement that
separation in value space is bounded?

**Answer: no, and there are two compounding defects, not one.** Correcting both changes the
bridge prediction from *exponential in λL* to *saturating in λL*, which changes what §5.2
should regress on.

**Scope.** This file is an analysis of `~/MainIdeas/Theories/chaos-games-theory.md` v0.1. It
**edits nothing**. Every change it implies to §3.3, §5.2 or §7.1 is Tier 3 and his.

> **NOT RED-TEAMED.** `PROTOCOL.md` §3.3 triggers **1** (proposes a change to a claim) and
> **2** (redefines a measured quantity, `γ²_eff`) both fire. The findings below are
> **claims, not verdicts**. F-1 and F-2 are arithmetic and can be recomputed in ten minutes;
> do that before acting on either.

---

## 1. What §7.1 says

Each decision in `G_p` injects a perturbation with probability `p`. A perturbation injected at
turn `t` has `L−t` turns to amplify at rate `λ`, contributing variance `∝ e^{2λ(L−t)}`. Summing
over injection times:

```
γ²_eff  ∝  ∫₀^L e^{2λ(L−t)} dt  =  (e^{2λL} − 1) / (2λ)
```

substituted into §3.2's `σ²(p) = σ₀² + p γ²` to give the boxed

```
ρ(p,L) = √L (1−p) μ / sqrt( σ₀² + p κ (e^{2λL} − 1)/(2λ) )
```

and the stated prediction: **τ_skill is decreasing in λ, exponentially in λL**; high-divergence
games collapse at dramatically lower noise than their decision count predicts; Paper B's `λ̂`
should absorb Paper A's residuals when added to §5.2's regression.

---

## 2. F-1 — the substitution fails its own limit check

§3.2's `γ²` is a **per-decision** variance: `Var[X_L] = L(σ₀² + pγ²)` follows from §3.1's
`X_L ~ N(Lμ, Lσ²)`. §7.1's integral is a **total over all L injection opportunities**.
Substituting the second into the slot of the first inserts a spurious factor of `L`.

The limit check makes it visible. As `λ → 0` (no amplification), `(e^{2λL} − 1)/(2λ) → L`, so
§7.1's boxed formula becomes

```
ρ  →  √L (1−p) μ / sqrt( σ₀² + p κ L )
```

which is **not** §3.2's `ρ = √L(1−p)μ / sqrt(σ₀² + pγ²)`. With no amplification at all, the two
sections must agree, and they do not.

**This is the check §3.4 performs on itself** — *"Verify the limit θ→0 recovers μ(1−p)√L/σ. It
does."* §7.1 performs no such check and does not pass one.

**Correction.** `γ²_eff` must be the *mean* per-decision contribution, not the sum:

```
γ²_eff  =  (κ/L) ∫₀^L [ d(a)/d₀ ]² da,     a = L − t
```

Under §7.1's own unbounded `d(a) = d₀ e^{λa}` this gives `γ²_eff = κ (e^{2λL} − 1)/(2λL)`, which
correctly → `κ` as `λ → 0`. The exponential blow-up survives this correction alone. It does not
survive F-2.

---

## 3. F-2 — the integrand contradicts §6.2

§6.2 states it explicitly:

> *"Consequence: `d_t ∈ [0, Δ_max]` is bounded, so growth is logistic rather than exponential
> and late-time data will drag any naive exponential fit toward zero."*

§7.1's integrand is `e^{2λ(L−t)}` — unbounded. A perturbation cannot contribute more than
`Δ_max²` of value-space variance, because `V: S → [0,1]` and `d_t = |V(s_t) − V(s'_t)|`.

Using §6.3's own logistic instead:

```
d(a) = Δ_max d₀ e^{λa} / ( Δ_max + d₀(e^{λa} − 1) )   →   Δ_max
```

with saturation time

```
t_sat = (1/λ) log(Δ_max/d₀)
```

**`t_sat` is §6.7's prediction horizon `T_pred` with `Δ_tol = Δ_max`.** The document already
names this quantity; it just does not use it here.

Splitting the corrected integral at `t_sat`, for `L ≫ t_sat`:

```
∫₀^{t_sat} d₀² e^{2λa} da  =  (Δ_max² − d₀²)/(2λ)  ≈  Δ_max²/(2λ)
∫_{t_sat}^{L}  Δ_max² da   =  Δ_max² (L − t_sat)
```

so, with the F-1 normalization,

```
γ²_eff  ≈  κ (Δ_max/d₀)² [ 1 − t_sat/L + 1/(2λL) ]   →   κ (Δ_max/d₀)²
```

**a constant in L.**

---

## 4. What this does to the two headline claims

### 4.1 The `L^(−1/2)` law is restored, not broken

With `γ²_eff` asymptotically constant, `ρ = √L(1−p)μ / sqrt(σ₀² + pκ(Δ_max/d₀)²)` recovers the
√L form, and §3.3's `1 − τ_skill ∝ L^(−1/2)` survives **for every game, at every λ**.

This is the opposite of what §7.1's uncorrected form implies, and it is good news for Paper A:
the bridge does not threaten the headline law. Under §7.1 as written, `γ²_eff ~ e^{2λL}` would
make `1 − τ_skill` *grow* with L for `λL ≫ 1`, i.e. the central claim would fail in every game
with appreciable λ. That failure is an artifact of the two defects above.

### 4.2 The bridge prediction changes form, and weakens

`γ²_eff` is bounded on both sides:

```
λ → 0   :  γ²_eff → κ                  (no amplification, contribution stays d₀²)
λ → ∞   :  γ²_eff → κ (Δ_max/d₀)²      (instant saturation)
```

So λ's total influence on `ρ` is a factor of at most `Δ_max/d₀` — a **per-game constant**, not
an unbounded exponential. The residual λ-dependence at finite L is the `t_sat/L` term, i.e.
`O( log(Δ_max/d₀) / (λL) )`.

**Direction survives: `τ_skill` is still decreasing in λ.** *"Exponential in λL"* and
*"dramatically lower"* do not. The correct functional form is **saturating in λL with a ceiling
set by `(Δ_max/d₀)²`**.

### 4.3 §5.2's prescribed test is misspecified

§7.1 says: *"add `λ̂` to §5.2's regression and check it absorbs residual variance."* §5.2 is
linear in `log(1 − τ̂_skill)`. Under §4.2 the correct covariate is a **saturating function of
`λ̂L`**, not `λ̂` entered linearly. Entering it linearly tests a functional form the corrected
derivation does not predict, and — given the degrees-of-freedom problem already flagged at
n = 8–12 with 3 predictors — will most likely return a null that is uninformative either way.

`Δ_max/d₀` is measurable per game and is the natural scale: it is *"how many single-edit
perturbations fit inside the value range."*

---

## 5. F-3 — §3.3's approximation is applied outside its stated domain, and is not needed

§3.3 derives the threshold *"working in the weak-noise regime where `pγ² ≪ σ₀²`"*.

But the threshold it derives sits at **p ≈ 0.9**, not in any weak-noise regime. With
`δ = 0.05`, `z_δ = Φ^{-1}(0.55) ≈ 0.1257`; a strong agent winning 90% at `p = 0` has
`ρ₀ = μ√L/σ₀ = Φ^{-1}(0.9) ≈ 1.28`, giving

```
1 − τ_skill = z_δ σ₀ /(μ√L) = 0.1257 / 1.28 ≈ 0.098      →   τ_skill ≈ 0.90
```

Dropping `pγ²` at `p ≈ 0.9` requires `γ² ≪ σ₀²`. `γ²` is the variance injected by a decision
made uniformly at random; its scale is set by §3.5's decision-value gap `g(s)`. There is no
reason to expect it small relative to baseline per-decision variance, and the document offers
none.

**The approximation is also unnecessary.** Keeping the term and expanding at small `q = 1−p`:

```
ρ = √L q μ / sqrt( σ₀² + (1−q) γ² )   ≈  √L q μ / sqrt( σ₀² + γ² )

⇒   1 − τ_skill  =  z_δ sqrt(σ₀² + γ²) / (μ √L)     ∝  L^(−1/2)
```

**The exponent is unchanged; only the prefactor moves, `σ₀ → sqrt(σ₀² + γ²)`.** §3.3 can drop
an approximation it does not need and become strictly more defensible at zero cost to the
claim. Recommend doing this regardless of F-1 and F-2 — it is the cheapest hardening in the
document.

---

## 6. F-4 — §3.4's `θ > 0` branch models unbounded growth on a bounded space

§3.4's algebra checks out. Both limits verify:

```
θ → 0   :  ρ → μ(1−p)√L/σ                    ✓ (as the document states)
|θ| > 0 :  ρ → μ(1−p)/σ · sqrt(2/|θ|)         ✓ (both signs, via the |θ| form)
```

But `E[X_L] = μ(1−p)(e^{θL} − 1)/θ` grows without bound for `θ > 0`, while `X_t = V(s_t) − V₀`
lives in a bounded value space — the same boundedness §6.2 relies on. Explosive drift on a
bounded domain is not a coherent process.

What snowballing physically is, is **early absorption**: the advantage reaches the boundary and
the match is decided, i.e. effective length `L_eff = min(L, hitting time)` rather than
exponential advantage growth. The *conclusion* — that `θ > 0` caps `ρ` — very likely survives,
because capped `L_eff` caps `ρ` directly. The **derivation** as written does not.

The `θ < 0` branch is a genuine mean-reverting OU and is unaffected.

**This matters for §7.2.** The predicted identity `θ ≈ λ` compares an OU drift coefficient to a
divergence exponent. If the `θ > 0` branch is really an absorption rate, then `θ` and `λ` are
not the same kind of object on that side, and a systematic disagreement in the snowballing
games would be a modelling artifact rather than §8.4's *"most informative failure."* The pilot
§7.2 recommends should therefore include **at least one `θ < 0` game and one `θ > 0` game**, or
it cannot distinguish the two explanations.

---

## 7. Summary

| # | Finding | Status | Cost to check |
|---|---|---|---|
| **F-1** | §7.1 substitutes a total into a per-decision slot; fails the `λ → 0` limit check that §3.4 performs on itself | arithmetic | 10 min |
| **F-2** | §7.1's integrand contradicts §6.2's boundedness; corrected, `γ²_eff` saturates at `κ(Δ_max/d₀)²` | arithmetic | 20 min |
| **F-2a** | Consequence: `L^(−1/2)` is **restored**, not broken — good news for Paper A | follows from F-1+F-2 | — |
| **F-2b** | Consequence: bridge prediction becomes **saturating in λL**, ceiling `(Δ_max/d₀)²`; direction survives, magnitude does not | follows from F-1+F-2 | — |
| **F-2c** | §5.2's prescribed "add `λ̂` linearly" is misspecified under the corrected form | follows from F-2b | — |
| **F-3** | §3.3's weak-noise approximation is applied at `p ≈ 0.9`, is unjustified there, and is **not needed** — the exponent survives without it | arithmetic | 10 min |
| **F-4** | §3.4's `θ > 0` branch is unbounded growth on a bounded space; conclusion likely survives, derivation does not; affects §7.2's pilot design | modelling | judgment |

**None of this requires compute, a testbed, or a line of code.** All four were reachable from
the document alone, which is an argument for doing this class of check before September rather
than after the first sweep.

**Not established here:** whether `Δ_max/d₀` is large enough per game for the saturating
λ-effect to be detectable at n = 8–12. That is the same power question already open against
§5.2 and it should be answered in the same simulation.

---

_Written once, 2026-08-24. Not to be edited. Not red-teamed. A revision is a second file._
