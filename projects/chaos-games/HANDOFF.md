# HANDOFF — chaos-games
_Last session: 2026-08-24 | main | 4bdf8c9 | forward sweep + Block A reads; §7.1 wrong twice; R-18 confirmed_

## Current state

Theory document 578 lines, v0.1. No code, no preregistration (stub, not locked). **Ten ledger
rows drafted and unwritten** — G-12…G-18 from prior sessions, **G-19…G-21 from this one**.

**The mandatory forward-citation sweep has been run** (`LITSEARCH-2026-08-24.md`), closing the
largest gap `LITSEARCH-2026-08-17.md` §5 declared. **R-16 answers NO so far:** six forward
citations across both Goodman 2024/2025 papers, none taking up their §VI invitation. The
specific conjunction stays at `k = 0`; the broad `k` goes 12 → 16.

**A third Goodman CoG 2024 paper exists and no register here held it** — *Skill Depth in
Tabletop Board Games*. Read in the original. It occupies the **skill-ladder** framing the way
the ToG paper occupies the randomness framing, with a fitted 3-parameter win-rate model whose
`M` is a per-game skill-separation ceiling explicitly attributed to stochasticity. Behind it:
Lantz 2017 → **Browne CoG 2022** (K1 retrieved this at `[T]` as retrieval 9 and did not
connect it) → Goodman 2024. Also surfaced: a **2025 QMUL PhD thesis** and a **CoG 2026 PIMC
paper**. **R-18 added; R-14 re-opened; R-12/R-16 widened; R-17 gained a route.**

**§7.1 is wrong in two compounding ways** (`DERIVATION-2026-08-24.md`), and correcting both
**restores** the `L^(−1/2)` law rather than breaking it — while weakening the A↔B bridge from
*exponential in λL* to *saturating in λL*.

**Three Block A reads done** (`READING-2026-08-24.md`). **R-18 confirmed and widened to three
axes** — the incumbent publishes per-game variation in MCTS parameters, information-handling
algorithm, and objective function, and §VI's *"for others this varied"* is what makes it a
confound in `β₁` rather than a limitation. **R-14 narrowed again — `Δ_model` survives.** Two
Block A items are **externally blocked**: the thesis (QMRO network-blocked) and OpenAlex
(budget, resets 00:00 UTC).

## In flight

Nothing half-built. Both artifacts written and closed — **write-once**.

**What stops precisely where — two items, both external, neither a dead end:**

1. **The thesis.** `tabletopgames.ai`'s link is **stale** — QMRO migrated to DSpace 7 and the
   `xmlui` path 404s. Every other QMRO route returns a network-level **`"Web Page Blocked!"`**
   page or `000` **from this machine**; WebFetch gets `socket hang up`; CORE is Cloudflared
   (403). **Handle is `123456789/108265`.** Needs a browser on a network that can reach QMRO —
   *he can fetch it and drop the PDF on disk, then the `pdftotext` route applies.*
2. **OpenAlex.** *"Insufficient budget… Resets at midnight UTC."* Checked 16:14 UTC.

The **term cross-product is still ~4% covered** from K1 and was not touched. S2's `/search`
endpoint was mostly unusable under 429s. Google Scholar's forward graph was not traversed.

**Ten drafted ledger rows remain unwritten and `DECISIONS_LEDGER.md` §3 still ends at G-11.**
Appending needs his go-ahead — portfolio-wide file. *Note: `/session-end` step 6 says to append
these; the standing practice in this project says wait for him. Left unwritten, tension flagged.*

## Blocked

Nothing hard-blocked.

- **Any novelty sentence for Paper A** — the forward pass is now done, but term exhaustion is
  not, and the three new Goodman items are `[T]` from a publication list.
- **Any quotation of M ≈ 785 or the ~10⁶ figure** — R-17, unchanged in kind. A route now exists.
- ~~§5.4 waits on the CoG 2026 PIMC paper~~ — **read; `Δ_model` survives.** R-14 is back to a
  related-work obligation.

## Next actions

Ordered. All pre-September desk work; none needs code.

1. **Get the thesis onto disk** — blocked on network, not on effort. Highest-value unread item;
   may hold R-17's error-bound correction and therefore unblock `BUDGET.md` §1.
2. **Re-run OpenAlex after 00:00 UTC** on the same four targets (~10 min). The S2 graph provably
   missed a CoG 2024 paper by the incumbent, so a second graph is worth its cost.
3. **Append the ten drafted ledger rows.** Mechanical; needs his go-ahead. **G-19 and G-20 both
   hardened this session** — G-19 gained a `[V]` argument (§1.5 of the reading), G-20 became a
   costed budget question rather than a framing one.
4. **Red-team the three unreviewed artifacts** — `DERIVATION-2026-08-24.md`,
   `LITSEARCH-2026-08-24.md`, `READING-2026-08-24.md`, plus `READING-2026-08-22.md`.
5. **Upgrade Browne CoG 2022 to `[V]`** — methodological parent of the whole skill-ladder line.
6. **Complete K1's term cross-product** — still ~4%.
7. **O-12 — TAG's roster with `L` per game.** Partly answered: 16 games are now named with BGG
   complexity (`READING-2026-08-24.md` §1.6), but **BGG complexity is not `L`**, and G-6 needs
   `L`. Still ~1 hr.
8. **O-9 — Palmer, Kantz** (~30 min). Unchanged.

## Open questions

His. Prior rows first, then this session's.

- **G-2** — uniform action replacement as the null. Unchanged, three options.
- **G-3** — MCTS budget-doubling as the skill ladder. **Now contested from outside — see G-20.**
- **G-8** — two-player only. Unchanged.
- **G-11** — δ = 0.05, M ≈ 785. Contested; see G-18.
- **G-12…G-18** — drafted 2026-08-17 and 2026-08-22, still unwritten.
- **G-19** — how Paper A positions against *Skill Depth* (CoG 2024). Three options:
  delta-in-related-work; adopt `M`/`β`/`r` as §5.2 covariates; or reframe `τ_skill` as the
  noise-axis complement of their skill-axis `M`.
- **G-20** — **whether the skill ladder is tuned per game or held at fixed MCTS parameters.**
  Three options, **all budget changes** — their tuning uses **NTBEA**, which `BUDGET.md` does not
  cost. **Now three axes, not one:** parameters, information-handling algorithm, objective
  function. §1.2 fixes one dimension of a space the incumbent tunes in eight.
- **G-21** — whether §6.8's `Σ` is renamed, given arXiv:2511.11611 uses `Σ` for per-turn
  outcome volatility in the same subfield.

## Traps for next session

- **`DERIVATION-2026-08-24.md` and `LITSEARCH-2026-08-24.md` are write-once and NOT
  red-teamed.** §3.3 triggers 1+2 fire on the first, trigger 3 on the second. **A red-team pass
  is owed on both, and one is still owed on `READING-2026-08-22.md`.**
- **Do not repeat the claim that boundedness breaks the `L^(−1/2)` law.** It was stated that way
  mid-session and it is wrong. Fixing **both** defects — the missing `1/L` normalization *and*
  the unbounded integrand — **restores** the law. Only the bridge weakens.
- **§7.1 has two defects, not one.** The `1/L` normalization error is the easier one to miss:
  §7.1 substitutes a **total over injection times** into §3.2's **per-decision** variance slot.
  It fails the `λ → 0` limit check that §3.4 performs on itself and passes.
- **`t_sat` is `T_pred`.** §6.7 already names the saturation time the bridge needs. The document
  has the quantity and does not use it in §7.
- **A citation graph did not find the most important paper.** *Skill Depth* appears in **none**
  of the four forward sets; it surfaced from a keyword query issued as an afterthought. A
  forward sweep finds what cites your targets, not what sits **beside** them. This is the second
  flag for a CoG/CIG 2019–2025 hand sweep and there is still no open item for it.
- **The `pdftotext` route works on this group's PDFs.** `curl -L` to disk, then `pdftotext`.
  `tabletopgames.ai/assets/pdf/` hosts them. Do not re-attempt WebFetch on those.
- **S2 rate-limits hard.** `/paper/{id}` and `/paper/search/match` survive with
  `--retry --retry-delay`; `/search` mostly does not. **OpenAlex has a daily budget and it is
  spent** until 00:00 UTC. MDPI returns 403; IEEE Xplore is inaccessible.
- **`tabletopgames.ai/Research.html` is the index for this group's PDFs** — every paper is at
  `/assets/pdf/`. Use it instead of searching. **Its thesis link is stale.**
- **QMRO is network-blocked from this machine** (`"Web Page Blocked!"` / `000` / `socket hang
  up`), and **CORE is Cloudflared**. Do not re-attempt either; the thesis needs a browser.
- **Do not repeat that *Following the Leader* (FDG 2023) bears on §3.4's `θ`.** It was written
  that way in `LITSEARCH-2026-08-24.md` §1.1 from a title alone and **it is wrong** — the paper
  is about **agent objective functions**, not game feedback structure. §3.4's `θ` remains
  **unoccupied by anything retrieved.** Corrected in `READING-2026-08-24.md` §3.
- **§5.3's ML fit will destabilise where the threshold lives.** The incumbent needed **L2
  regularisation** on the same class of fit because *"high noise in low-skill games could cause
  overfitting"* — and `chaos-games` drives games into that regime on purpose. Belongs in the
  build memo for the collapse-threshold estimator.
- **Their `M` is not identifiable in several games** — budget is unbounded so the asymptote
  escapes their data. **`p ∈ [0,1]` is bounded and fully sweepable, and `G_1` is a defined
  endpoint.** That is the strongest `[V]`-backed argument for the injected-noise instrument, and
  it is G-19 material — do not leave it on the floor.
- **Their default agent is Open Loop IS-MCTS with root redeterminisation**, not vanilla MCTS.
  Theory §1.2 under-specifies the agent for imperfect-information games.
- **`Σ` collides.** Theory §6.8 vs arXiv:2511.11611. Ledger G-21.
- **The `L` distinction survived a second run** — every length-adjacent result retrieved is about
  **repetitions of a match**, not **decisions within a match**. Do not let a summary blur it.
- **§6.8's sign is confirmed opposed.** Unchanged. Pilot `Σ` on two games first.
- **Their instrument is seed variation; ours is noise injection.** They do not inject noise.
- **TAG is JVM.** Unchanged. Ledger G-7.
- **This document has no seed of its own** in `topics.md`. Ledger X-1b.
- **Paper B before Paper A** remains the sequencing trap.
