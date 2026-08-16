# Work Order 02 - Distillation (Decision Making)

The skill scaffold is in `skill/`. Fill it in. This work order is
self-contained; the full rules live in prompts/distill_common.md and
prompts/distill_skill.md (read them first if unfamiliar).

## Classification (already validated)

```yaml
primary_category: decision-making
subcategory: uncertainty
confidence: 0.9
rationale: 'The book''s eight chapters all teach one capability: making and reviewing
  decisions under uncertainty. Chapter titles name the core moves - "Every Decision
  Is a Bet", "Resulting", belief updating/calibration, decision journaling, bet sizing,
  premortems and tripwires, group dissent. The method is probabilistic decision quality
  (belief/confidence numbers, outcome vs. process separation), which is squarely the
  decision-making profile. psychology-behavior is a mild alternative because Chapter
  2 discusses outcome bias as a cognitive trap, but the book teaches a decision procedure,
  not theories of mind.'
alternative_categories:
- category: psychology-behavior
  confidence: 0.45
tags:
- probability
- belief-updating
- outcome-bias
- decision-quality
- calibration
method: agent

```

## Category profile: decision-making

Extract with THIS focus:

focus:
- decision principles (timeless rules the author argues for)
- decision frameworks (named models with inputs, steps, outputs)
- uncertainty handling (probabilistic thinking, confidence levels, scenarios)
- cognitive biases the book targets, and their counter-moves
- decision procedures (step-by-step processes an agent can run)
- evidence updating (how to change beliefs when new information arrives)
- failure modes (classic ways decisions go wrong, per the book)
- when to use / not use the book's approach
epistemic_guardrails:
- Keep decisions and outcomes separate; never let the skill claim an outcome proves
  a decision was right.
- Preserve probability language ("likely", "x% confident") instead of false certainty.
- Distinguish the author's prescriptive advice from descriptions of what people actually
  do.


## Required SKILL.md sections

- Purpose
- Use When
- Do Not Use When
- Core Mental Model
- Core Principles
- Operating Procedure
- Decision Rules
- Failure Modes
- How to Handle Uncertainty
- How to Use the References
- Final Quality Check

## Required references files

- principles.md: Core principles of the book, each tagged with content type and source.
- frameworks.md: Named frameworks and models, with inputs, steps, and outputs.
- procedures.md: Step-by-step procedures an agent can execute.
- examples.md: Worked examples (paraphrased), showing the method applied.
- limitations.md: Where the book's approach breaks, contested claims, and scope limits.
- source-map.md: Map from every distilled item back to chapter/section, plus the content-type legend.

## Book digest (full text: workspace/book/text.md)

```
TITLE: The Decision Notebook
AUTHOR: (unknown)
FORMAT: md
WORDS: 2123
CHAPTERS: 8

CHAPTER TITLES:
  1. Chapter 1 — Every Decision Is a Bet (~279 words)
  2. Chapter 2 — Resulting: The Trap of Judging by Outcomes (~280 words)
  3. Chapter 3 — Updating: Hearing the Crowd Correctly (~249 words)
  4. Chapter 4 — The Decision Journal (~247 words)
  5. Chapter 5 — Sizing: Bold When Right, Careful When Unsure (~247 words)
  6. Chapter 6 — Premortems and Tripwires (~254 words)
  7. Chapter 7 — Deciding in Groups: Permission to Disagree (~233 words)
  8. Chapter 8 — The Practicing Decider (~286 words)

EXCERPTS:
--- [1] Chapter 1 — Every Decision Is a Bet ---
## Chapter 1 — Every Decision Is a Bet Most people think of betting as something that happens in casinos. This notebook starts from a different claim: every decision is a bet. When you accept a job offer, you are betting that the role will suit you better than the alternatives. When you ship a feature early, you are betting that the speed matters more than the polish. When you hire someone, you are betting on how they will behave in a year, under pressure you have not seen yet. Two things follow from treating decisions as bets. First, every bet is a wager on a set of beliefs. If you believe the market will grow, you bet on capacity; if you believe it will shrink, you bet on cash. The decision reveals the belief, which means you can inspect the belief directly instead of arguing about the decision. Second, bets are made against an uncertain future. You cannot know how the dice will land. You can only make choices whose expected value is favorable and whose downside you can survive. A good decision is one that made sense given what was reasonably knowable at the time - not one that happened to end well. The habit to build: when facing a choice, say out loud what you are betting on. "I am betting that this vendor's reliability holds at 10x our current volume." If you cannot state the bet, you do not yet understand the decision. A bet has three parts: the belief it rests on, the stake involved, and the odds you implicitly accept. Beginners look only at the stake. Practitioners write down all three before choosing. ... instead of arguing about the decision. Second, bets are made against an uncertain future. You cannot know how the dice will land. You can only make choices whose expected value is favorable and whose downside you can survive. A good decision is one that made sense given what was reasonably knowable at the time - not one that happened to end well. The habit to build: when facing a choice, say out loud what you are betting on. "I am betting that this vendor's reliability holds at 10x our current volume." If you cannot state the bet, you do not yet understand the decision. A bet has three parts: the belief it rests on, the stake involved, and the odds you implicitly accept. Beginners look only at the stake. Practitioners write down all three before choosing.
--- [2] Chapter 2 — Resulting: The Trap of Judging by Outcomes ---
## Chapter 2 — Resulting: The Trap of Judging by Outcomes There is a name for the most seductive error in decision-making: resulting. Resulting is judging a decision purely by how it turned out. The trader who makes a reckless bet and wins believes the bet was good. The careful driver who gets hit believes taking the road was bad. Both conclusions confuse the quality of the decision with the quality of the outcome. Why does resulting persist? Because outcomes are vivid and visible, while decision quality is invisible. You see the win or the loss; you never see the branch of the tree that did not happen. Our stories naturally compress into "it worked" or "it did not," dropping all the probability along the way. The correction is to separate two questions that feel like one: Was the decision well made? And did it turn out well? There are four combinations, and only one of them - a well-made decision with a good outcome - deserves repetition. A badly made decision that succeeds is the most dangerous cell in the table, because it teaches the wrong lesson and rewards it. One more nuance: a small number of outcomes tells you almost nothing. Three wins in a row is compatible with skill, with luck, and with a coin that has not had time to show its true bias. Sample size is not pedantry; it is the difference between evidence and anecdote. The habit to build: after any meaningful outcome, spend one minute on the process and zero minutes on the scoreboard. Ask what information was available, what was assumed, and what the alternatives were. Only then look at the result. ... ecision well made? And did it turn out well? There are four combinations, and only one of them - a well-made decision with a good outcome - deserves repetition. A badly made decision that succeeds is the most dangerous cell in the table, because it teaches the wrong lesson and rewards it. One more nuance: a small number of outcomes tells you almost nothing. Three wins in a row is compatible with skill, with luck, and with a coin that has not had time to show its true bias. Sample size is not pedantry; it is the difference between evidence and anecdote. The habit to build: after any meaningful outcome, spend one minute on the process and zero minutes on the scoreboard. Ask what information was available, what was assumed, and what the alternatives were. Only then look at the result.
--- [3] Chapter 3 — Updating: Hearing the Crowd Correctly ---
## Chapter 3 — Updating: Hearing the Crowd Correctly Beliefs are not trophies; they are working estimates that should move when information arrives. The skill is updating without overreacting. Imagine a weather forecaster who said rain was 70% likely, and it did not rain. Was the forecaster wrong? Strictly, no - a 70% claim is falsified by neither rain nor sunshine on any single day. A single outcome almost never settles a probabilistic claim. What settles it is a track record: over hundreds of 70%-rain days, does it rain about 70% of the time? This is the discipline of calibration. To practice it, attach numbers to your beliefs - "I am 80% confident this launch slips by two weeks" - and record them. Numbers can be scored; vibes cannot. When new evidence arrives, move proportionally. Evidence that was already expected should barely move you; surprising evidence should move you a lot. A team that always meets its estimates learns nothing from an on-time delivery, but a lot from a late one. Ask of every update: was this information already priced into my belief? Beware the two failure modes. The stubborn never update, treating every surprise as noise. The weather-vanes update on everything, treating noise as signal. The midpoint discipline: before changing a belief, state what would have made you change it more, and what would have left it unchanged. The habit to build: keep your confidence statements numerical and dated, and review the old numbers before making new ones. ... When new evidence arrives, move proportionally. Evidence that was already expected should barely move you; surprising evidence should move you a lot. A team that always meets its estimates learns nothing from an on-time delivery, but a lot from a late one. Ask of every update: was this information already priced into my belief? Beware the two failure modes. The stubborn never update, treating every surprise as noise. The weather-vanes update on everything, treating noise as signal. The midpoint discipline: before changing a belief, state what would have made you change it more, and what would have left it unchanged. The habit to build: keep your confidence statements numerical and dated, and review the old numbers before making new ones.
--- [4] Chapter 4 — The Decision Journal ---
## Chapter 4 — The Decision Journal Memory is a renovator, not an archivist. It rebuilds the past to fit the present, quietly converting "I thought it would probably work" into "I knew it would." The defense is externalization: a decision journal. A journal entry is made before the outcome is known, and it has five fields. The decision itself, stated as a bet. The beliefs it rests on, with confidence numbers. The alternatives you rejected, and why. The information you wish you had. And the tripwires - the events that would tell you the bet is going wrong. The entry must be written before the outcome arrives; a journal written afterward is a memoir, not an instrument. Date everything. Sign it, if that makes it feel real. Review cadence matters more than entry quality. Once a month, read three old entries and score them: was the decision sound, was the outcome informative, and did the confidence numbers hold up? Over a year, patterns emerge that no single decision can show - that you are systematically overconfident about timelines, say, or that your rejected alternatives keep winning. The journal also protects you from hindsight in groups. When a colleague says "we all knew this would fail," the entry from the time is the counter-evidence. It converts vague regret into specific lessons. The habit to build: one entry per significant decision, five minutes to write, one monthly review. The journal is the cheapest laboratory you will ever run. ... eview cadence matters more than entry quality. Once a month, read three old entries and score them: was the decision sound, was the outcome informative, and did the confidence numbers hold up? Over a year, patterns emerge that no single decision can show - that you are systematically overconfident about timelines, say, or that your rejected alternatives keep winning. The journal also protects you from hindsight in groups. When a colleague says "we all knew this would fail," the entry from the time is the counter-evidence. It converts vague regret into specific lessons. The habit to build: one entry per significant decision, five minutes to write, one monthly review. The journal is the cheapest laboratory you will ever run.
--- [5] Chapter 5 — Sizing: Bold When Right, Careful When Unsure ---
## Chapter 5 — Sizing: Bold When Right, Careful When Unsure How much should you stake on a belief? Everything depends on two variables you control separately: how right you think you are, and how much it costs to be wrong. Amateurs vary only the second. Professionals vary both. The rule of this notebook: stake in proportion to your edge, and never in proportion to your excitement. When evidence is thin, make the bet small enough that being wrong is cheap tuition. When evidence stacks up, size up gradually - because even a strong belief deserves a shakedown cruise. Asymmetry is the second principle. A good bet has a small downside and a meaningful upside, or it is insured against ruin. Before any significant commitment, name the worst realistic case. If that case is unrecoverable - the company dies, the reputation is gone, the savings are lost - the probability of gain does not matter. Survivable errors are tuition; unrecoverable ones end the game. No expected value calculation rescues a bet you cannot afford to lose. A third principle: diversify across independent bets, not across many copies of the same bet. Ten startup investments in the same sector, funded on the same assumption, are one bet wearing ten costumes. The habit to build: for every significant commitment, write one sentence - "if I am wrong, this costs me X, and X is/is not survivable" - and one more: "my evidence is thin/medium/strong, so my stake is small/medium/large." ... ame the worst realistic case. If that case is unrecoverable - the company dies, the reputation is gone, the savings are lost - the probability of gain does not matter. Survivable errors are tuition; unrecoverable ones end the game. No expected value calculation rescues a bet you cannot afford to lose. A third principle: diversify across independent bets, not across many copies of the same bet. Ten startup investments in the same sector, funded on the same assumption, are one bet wearing ten costumes. The habit to build: for every significant commitment, write one sentence - "if I am wrong, this costs me X, and X is/is not survivable" - and one more: "my evidence is thin/medium/strong, so my stake is small/medium/large."
--- [6] Chapter 6 — Premortems and Tripwires ---
## Chapter 6 — Premortems and Tripwires Two cheap rituals prevent expensive mistakes: the premortem and the tripwire. The premortem runs before you commit. Imagine it is eighteen months later and the decision has failed badly. Write the story of the failure - in the past tense, with specifics. "We lost the key client because we never assigned an owner to the migration." The strange tense matters: research on prospective hindsight suggests people find more failure modes when they assume the failure has already happened. Run it with the whole team; every failure story told aloud becomes a checklist item nobody has to be brave to raise later. The tripwire runs after you commit. It is a pre-agreed signal that converts a vague "let's keep an eye on it" into a decision. A tripwire has three parts: a measurable condition, a date, and an action. "If churn exceeds 4% by the end of Q2, we pause the expansion and diagnose." Without the pre-agreed action, hitting the number just produces a meeting; with it, the number produces a choice. Tripwires defend against two known biases. Escalation of commitment: the desire to invest more in a failing course because you already invested. And the status quo drift: the tendency of unexamined decisions to continue by default. Both are weakened when the exit condition was written by the you who was still objective. The habit to build: no significant commitment without one premortem story and two written tripwires - one for time, one for a leading metric. ... n it" into a decision. A tripwire has three parts: a measurable condition, a date, and an action. "If churn exceeds 4% by the end of Q2, we pause the expansion and diagnose." Without the pre-agreed action, hitting the number just produces a meeting; with it, the number produces a choice. Tripwires defend against two known biases. Escalation of commitment: the desire to invest more in a failing course because you already invested. And the status quo drift: the tendency of unexamined decisions to continue by default. Both are weakened when the exit condition was written by the you who was still objective. The habit to build: no significant commitment without one premortem story and two written tripwires - one for time, one for a leading metric.
--- [7] Chapter 7 — Deciding in Groups: Permission to Disagree ---
## Chapter 7 — Deciding in Groups: Permission to Disagree Groups do not automatically think better than individuals; they think differently, and whether that helps is a design choice. Two failure patterns dominate. The first is premature agreement: the room converges on the first confident voice, and dissent, being socially expensive, never gets priced in. The second is ritual disagreement: objections fly freely, but nothing converges, because disagreement is an identity rather than an input. The countermeasure to the first failure is a formal dissent slot. Before the decision closes, one person is assigned to argue the strongest case against it. The role rotates; the argument is delivered in full; the decision maker must respond to it in one sentence, out loud. The point is not to be persuaded but to force the counter-case into the record where it can be right. The countermeasure to the second is convergence discipline. Every discussion ends in one of three declared states: decided, decided-pending-one-named- piece-of-information, or explicitly deferred with a date. "We discussed it" is not an outcome. Finally, separate the accuracy incentive from the popularity incentive. Ask people for their estimates privately before the group discusses, then reveal all answers at once. The spread of private answers is information the first speaker would have destroyed. The habit to build: private estimates before discussion, a rotating dissent slot before closure, and a declared convergence state after. ... ce, out loud. The point is not to be persuaded but to force the counter-case into the record where it can be right. The countermeasure to the second is convergence discipline. Every discussion ends in one of three declared states: decided, decided-pending-one-named- piece-of-information, or explicitly deferred with a date. "We discussed it" is not an outcome. Finally, separate the accuracy incentive from the popularity incentive. Ask people for their estimates privately before the group discusses, then reveal all answers at once. The spread of private answers is information the first speaker would have destroyed. The habit to build: private estimates before discussion, a rotating dissent slot before closure, and a declared convergence state after.
--- [8] Chapter 8 — The Practicing Decider ---
## Chapter 8 — The Practicing Decider This notebook closes with a warning and a promise. The warning: none of these tools - the bet framing, the journal, the premortem - makes you certain. They do not reduce the uncertainty of the world by one iota. What they reduce is your error rate given that uncertainty, and your blindness to your own error rate. The promise: deciding well is a practice, not a talent. Every element in this book is a habit that compounds. The journal entries accumulate into calibration data. The premortems accumulate into pattern memory. The tripwires accumulate into an organization that can act without re-litigating. Where does the method fail? Three honest limits. It works poorly when the feedback loop is too slow - if outcomes take a decade, the journal cannot correct you within a career, and you should lean on base rates from other people's histories instead of your own. It works poorly for decisions that are not repeated - one-off, high-stakes choices deserve external counsel over personal calibration. And it assumes you can stomach being visibly wrong on the record; if the culture punishes journaled errors, people will stop journaling, and the whole apparatus goes dark. A last word on beginning. Do not adopt the whole notebook at once. Adopt one practice - the decision journal is the usual first - and run it for a month. The practices sell themselves or they do not; that, too, is a bet, and a cheap one. --- *End of The Decision Notebook. This sample book is dedicated to the public domain under CC0 1.0. It exists to demonstrate book-to-agent-skill; it is deliberately short and is not a substitute for a full-length book.* ... lean on base rates from other people's histories instead of your own. It works poorly for decisions that are not repeated - one-off, high-stakes choices deserve external counsel over personal calibration. And it assumes you can stomach being visibly wrong on the record; if the culture punishes journaled errors, people will stop journaling, and the whole apparatus goes dark. A last word on beginning. Do not adopt the whole notebook at once. Adopt one practice - the decision journal is the usual first - and run it for a month. The practices sell themselves or they do not; that, too, is a bet, and a cheap one. --- *End of The Decision Notebook. This sample book is dedicated to the public domain under CC0 1.0. It exists to demonstrate book-to-agent-skill; it is deliberately short and is not a substitute for a full-length book.*
```

## When done

Run `book2skill validate <workspace>/skill` to check, then
`book2skill finalize --workspace <workspace>` to install.
