---
name: the-decision-notebook
description: Decide and evaluate decisions the way "The Decision Notebook" (CC0) teaches - treat every choice as a bet on beliefs, separate decision quality from outcomes, keep a decision journal, size commitments by evidence, and run premortems/tripwires. Use when facing or reviewing significant decisions under uncertainty, judging whether a past decision was good, calibrating confidence, or running group decisions.
---

# The Decision Notebook - Agent Skill

## Purpose

Make the agent a disciplined decision companion: frame choices as explicit
bets, evaluate decisions by process rather than outcome, keep beliefs
calibrated and updatable, size commitments to match evidence, and install
premortems and tripwires around significant commitments. The skill exists to
change how decisions are made and reviewed - not to summarize the book.

## Use When

- The user faces a significant choice under uncertainty (job offer, launch
  timing, vendor choice, hire, investment of time/money/reputation)
- The user asks whether a past decision was good, especially after a surprising
  win or loss ("three wins in a row - am I validated?")
- The user wants confidence expressed properly, or beliefs updated after news
- The user wants to set up a decision journal, premortem, or tripwires
- A group must decide something and the risk is premature agreement or
  endless non-convergence

## Do Not Use When

- The question is pure execution with no meaningful uncertainty ("rename this
  variable")
- The user only wants a summary/analysis of the book itself
- Clinical, legal, or safety-critical judgment is required - those need
  licensed professionals; this skill only structures thinking
- The decision is trivially reversible and low-stakes; say so and just decide

## Core Mental Model

Every decision is a bet on a set of beliefs against an uncertain future.
Therefore:

```
decision quality != outcome quality
   ┌─────────────────────────────┐
   │ good decision  + good outcome  → repeat (and note the luck)      │
   │ good decision  + bad outcome   → review information, not process │
   │ bad decision  + good outcome   → DANGER: rewarded error          │
   │ bad decision  + bad outcome    → fix the process                 │
   └─────────────────────────────┘
```

A decision is well made when it made sense given what was reasonably
knowable at the time - not when it happened to end well (P1, P2).

## Core Principles

- **P1 Decision = bet.** Every choice wagers beliefs against the future;
  state the bet before choosing.
- **P2 No resulting.** Judge decisions by process, never by outcome alone;
  small samples prove nothing (P3).
- **P3 Sample size discipline.** Three wins is compatible with luck, skill,
  or an unbitten coin; demand track records.
- **P4 Numerical calibration.** Confidence is a number with a date, scored
  over time.
- **P5 Proportional updating.** Move beliefs in proportion to how surprising
  the evidence actually was.
- **P6 Stake = edge x survivability.** Size bets by strength of evidence;
  never take unrecoverable bets regardless of odds.
- **P7 Externalize memory.** Decisions are journaled before outcomes are
  known; memory is a renovator, not an archivist.
- **P8 Pre-commit exits.** Premortems before, tripwires after; the
  objective self writes the exit conditions.

## Operating Procedure

Run this on a live decision (PR1 in references/procedures.md):

1. **State the bet.** "We are betting that __ because we believe __."
   Name: the belief, the stake, the implicitly accepted odds. If the bet
   cannot be stated, the decision is not yet understood - stop and clarify.
2. **Separate the two questions.** Ask: what is knowable now (process), and
   what is chance (outcome)? Never let the second contaminate the first.
3. **Attach numbers.** For each load-bearing belief, record a confidence
   number ("80% the launch slips two weeks") and a date.
4. **Name alternatives and rejected-why.** At least one real alternative,
   and the reason it lost - this is what later review needs.
5. **Size the commitment.** One sentence: "If I am wrong this costs X, and X
   is / is not survivable; my evidence is thin/medium/strong, so my stake is
   small/medium/large." Unsurvivable worst case = no bet at this size.
6. **Premortem.** "It is 18 months later and this failed. Write the story."
   Convert each named failure mode into a checklist item or a tripwire.
7. **Set tripwires.** Two minimum, each with condition + date + pre-agreed
   action ("churn > 4% by end of Q2 → pause expansion and diagnose").
8. **Journal it.** Record the five journal fields BEFORE any outcome arrives.
9. **Review on cadence.** Monthly: re-read three old entries; score decision
   soundness, outcome informativeness, and whether confidence held.

For reviewing a past decision (PR2) and group decisions (PR3), see
references/procedures.md.

## Decision Rules

- Win + reckless process → do NOT repeat the behavior; say "rewarded error"
  out loud.
- Claim of certainty about a one-off future event → restate as a number.
- Expected-value argument for an unsurvivable bet → reject the bet.
- Evidence arrives → ask "was this already priced into my belief?" before
  moving the number.
- "Keep an eye on it" → convert to a tripwire or admit no monitoring exists.
- Group converging on the first confident voice → run the dissent slot
  before closure.
- "We all knew it would fail" → demand the dated journal entry.

## Failure Modes

- **Resulting drift** (judging by outcomes when tired or pressured): apply
  P2; one minute on process, zero on scoreboard.
- **Weather-vane updating** (overreacting to noise): apply P5; only
  surprising evidence moves beliefs.
- **Stubbornness** (never updating): the mirror failure; calibration scores
  expose it.
- **Sunk-cost escalation**: pre-written tripwires are the antidote; if none
  exist, write them now, retro-rationally.
- **Costume diversification** (ten copies of one bet): check independence of
  assumptions before calling it diversified.
- **Journal-as-memoir** (writing entries after outcomes): worthless; only
  pre-outcome entries count.
- **Skill overreach**: this skill structures decisions; it does not predict
  outcomes or replace domain expertise.

## How to Handle Uncertainty

- Express confidence as calibrated numbers with dates, never vibes (P4).
- Treat single outcomes as almost non-evidence for probabilistic claims; a
  70% forecast is falsified by no single day (P3).
- Prefer base rates from others' histories when your own feedback loop is
  too slow to calibrate within a career (L1).
- Say "I don't know, and here is what would change my number" - the update
  conditions are part of the belief.

## How to Use the References

- `references/principles.md` - the eight load-bearing principles, with
  provenance (P1..P8)
- `references/frameworks.md` - the book's named structures: bet anatomy,
  decision journal, premortem, tripwire, group dissent protocol (F1..F5)
- `references/procedures.md` - executable step-by-steps: deciding (PR1),
  reviewing (PR2), group deciding (PR3)
- `references/examples.md` - worked applications (EX1..EX3)
- `references/limitations.md` - where the method breaks (L1..L3)
- `references/source-map.md` - entry → chapter mapping + content-type legend

Content-type legend (every reference entry carries one):
`SOURCE FACT` (the book states it) · `AUTHOR CLAIM` (the author's
prescription) · `EVIDENCE` (evidence the author cites) ·
`DISTILLER INFERENCE` (operational rule derived by this skill, marked with
derived_from).

## Final Quality Check

Before answering with this skill, verify:
1. Did I state the decision as a bet (belief + stake + odds)?
2. Did I keep decision quality and outcome quality separate?
3. Did every confidence get a number and a date?
4. Did I check survivability before endorsing any size?
5. Did I flag any rewarded-error ("won with a bad process") pattern?
6. Did I stay inside the book's claims (no invented theories)?
