# ASSUMPTIONS — chaos-games

_One row per `ASSUMPTION:` marker in the code. Format: `../../docs/PROTOCOL.md` §5.6._

The pre-publication audit greps the code for `ASSUMPTION:` and diffs against this table.
**Unmatched entries in either direction are defects** — a marker with no row means something
was guessed and not declared; a row with no marker means the code changed and the ledger did
not.

An assumption is something *guessed because nobody knows*. A **choice** — where a different
answer was available and would change downstream work — is not an assumption; it is a
`DECISIONS_LEDGER.md` row. `PROTOCOL.md` §5.7.

---

| ID | What was assumed | Marker location | What would validate it | Status |
|---|---|---|---|---|

_No code, no markers, no rows._
