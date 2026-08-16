# Work Order 01 - Classification

Classify the book, then write `classification.yaml` in the workspace root
(schema: schemas/classification.schema.json).

## Book digest

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
## Chapter 1 — Every Decision Is a Bet Most people think of betting as something that happens in casinos. This notebook starts from a different claim: every decision is a bet. When you accept a job offer, you are betting that the role will suit you better than the alternatives. When you ship a feature early, you are betting that the speed matters more than the polish. When you hire someone, you are betting on how they will behave in a year, under pressure you have not seen yet. Two things follow from treating decisions as bets. First, every bet is a wager on a set of beliefs. If you believe the market will grow, you bet on capacity; if you believe it will shrink, you bet on cash. The decision reveals the belief, which means you can inspect the belief directly instead of arguing about the decision. Second, bets are made against an uncertain future. You cannot know how the dice will land. You can only make choices whose expected value ... instead of arguing about the decision. Second, bets are made against an uncertain future. You cannot know how the dice will land. You can only make choices whose expected value is favorable and whose downside you can survive. A good decision is one that made sense given what was reasonably knowable at the time - not one that happened to end well. The habit to build: when facing a choice, say out loud what you are betting on. "I am betting that this vendor's reliabilit
--- [2] Chapter 2 — Resulting: The Trap of Judging by Outcomes ---
## Chapter 2 — Resulting: The Trap of Judging by Outcomes There is a name for the most seductive error in decision-making: resulting. Resulting is judging a decision purely by how it turned out. The trader who makes a reckless bet and wins believes the bet was good. The careful driver who gets hit believes taking the road was bad. Both conclusions confuse the quality of the decision with the quality of the outcome. Why does resulting persist? Because outcomes are vivid and visible, while decision quality is invisible. You see the win or the loss; you never see the branch of the tree that did not happen. Our stories naturally compress into "it worked" or "it did not," dropping all the probability along the way. The correction is to separate two questions that feel like one: Was the decision well made? And did it turn out well? There are four combinations, and only one of them - a well-made decision with a good outcome - deserves repet ... ecision well made? And did it turn out well? There are four combinations, and only one of them - a well-made decision with a good outcome - deserves repetition. A badly made decision that succeeds is the most dangerous cell in the table, because it teaches the wrong lesson and rewards it. One more nuance: a small number of outcomes tells you almost nothing. Three wins in a row is compatible with skill, with luck, and with a coin that has not had time to show its true bi
--- [3] Chapter 3 — Updating: Hearing the Crowd Correctly ---
## Chapter 3 — Updating: Hearing the Crowd Correctly Beliefs are not trophies; they are working estimates that should move when information arrives. The skill is updating without overreacting. Imagine a weather forecaster who said rain was 70% likely, and it did not rain. Was the forecaster wrong? Strictly, no - a 70% claim is falsified by neither rain nor sunshine on any single day. A single outcome almost never settles a probabilistic claim. What settles it is a track record: over hundreds of 70%-rain days, does it rain about 70% of the time? This is the discipline of calibration. To practice it, attach numbers to your beliefs - "I am 80% confident this launch slips by two weeks" - and record them. Numbers can be scored; vibes cannot. When new evidence arrives, move proportionally. Evidence that was already expected should barely move you; surprising evidence should move you a lot. A team that always meets its estimates learns not ... When new evidence arrives, move proportionally. Evidence that was already expected should barely move you; surprising evidence should move you a lot. A team that always meets its estimates learns nothing from an on-time delivery, but a lot from a late one. Ask of every update: was this information already priced into my belief? Beware the two failure modes. The stubborn never update, treating every surprise as noise. The weather-vanes update on everything, treating nois
--- [4] Chapter 4 — The Decision Journal ---
## Chapter 4 — The Decision Journal Memory is a renovator, not an archivist. It rebuilds the past to fit the present, quietly converting "I thought it would probably work" into "I knew it would." The defense is externalization: a decision journal. A journal entry is made before the outcome is known, and it has five fields. The decision itself, stated as a bet. The beliefs it rests on, with confidence numbers. The alternatives you rejected, and why. The information you wish you had. And the tripwires - the events that would tell you the bet is going wrong. The entry must be written before the outcome arrives; a journal written afterward is a memoir, not an instrument. Date everything. Sign it, if that makes it feel real. Review cadence matters more than entry quality. Once a month, read three old entries and score them: was the decision sound, was the outcome informative, and did the confidence numbers hold up? Over a year, patterns ... eview cadence matters more than entry quality. Once a month, read three old entries and score them: was the decision sound, was the outcome informative, and did the confidence numbers hold up? Over a year, patterns emerge that no single decision can show - that you are systematically overconfident about timelines, say, or that your rejected alternatives keep winning. The journal also protects you from hindsight in groups. When a colleague says "we all knew this would fa
--- [5] Chapter 5 — Sizing: Bold When Right, Careful When Unsure ---
## Chapter 5 — Sizing: Bold When Right, Careful When Unsure How much should you stake on a belief? Everything depends on two variables you control separately: how right you think you are, and how much it costs to be wrong. Amateurs vary only the second. Professionals vary both. The rule of this notebook: stake in proportion to your edge, and never in proportion to your excitement. When evidence is thin, make the bet small enough that being wrong is cheap tuition. When evidence stacks up, size up gradually - because even a strong belief deserves a shakedown cruise. Asymmetry is the second principle. A good bet has a small downside and a meaningful upside, or it is insured against ruin. Before any significant commitment, name the worst realistic case. If that case is unrecoverable - the company dies, the reputation is gone, the savings are lost - the probability of gain does not matter. Survivable errors are tuition; unrecoverable ones ... ame the worst realistic case. If that case is unrecoverable - the company dies, the reputation is gone, the savings are lost - the probability of gain does not matter. Survivable errors are tuition; unrecoverable ones end the game. No expected value calculation rescues a bet you cannot afford to lose. A third principle: diversify across independent bets, not across many copies of the same bet. Ten startup investments in the same sector, funded on the same assumption, ar
--- [6] Chapter 6 — Premortems and Tripwires ---
## Chapter 6 — Premortems and Tripwires Two cheap rituals prevent expensive mistakes: the premortem and the tripwire. The premortem runs before you commit. Imagine it is eighteen months later and the decision has failed badly. Write the story of the failure - in the past tense, with specifics. "We lost the key client because we never assigned an owner to the migration." The strange tense matters: research on prospective hindsight suggests people find more failure modes when they assume the failure has already happened. Run it with the whole team; every failure story told aloud becomes a checklist item nobody has to be brave to raise later. The tripwire runs after you commit. It is a pre-agreed signal that converts a vague "let's keep an eye on it" into a decision. A tripwire has three parts: a measurable condition, a date, and an action. "If churn exceeds 4% by the end of Q2, we pause the expansion and diagnose." Without the pre-agre ... n it" into a decision. A tripwire has three parts: a measurable condition, a date, and an action. "If churn exceeds 4% by the end of Q2, we pause the expansion and diagnose." Without the pre-agreed action, hitting the number just produces a meeting; with it, the number produces a choice. Tripwires defend against two known biases. Escalation of commitment: the desire to invest more in a failing course because you already invested. And the status quo drift: the tendency o
--- [7] Chapter 7 — Deciding in Groups: Permission to Disagree ---
## Chapter 7 — Deciding in Groups: Permission to Disagree Groups do not automatically think better than individuals; they think differently, and whether that helps is a design choice. Two failure patterns dominate. The first is premature agreement: the room converges on the first confident voice, and dissent, being socially expensive, never gets priced in. The second is ritual disagreement: objections fly freely, but nothing converges, because disagreement is an identity rather than an input. The countermeasure to the first failure is a formal dissent slot. Before the decision closes, one person is assigned to argue the strongest case against it. The role rotates; the argument is delivered in full; the decision maker must respond to it in one sentence, out loud. The point is not to be persuaded but to force the counter-case into the record where it can be right. The countermeasure to the second is convergence discipline. Every discus ... ce, out loud. The point is not to be persuaded but to force the counter-case into the record where it can be right. The countermeasure to the second is convergence discipline. Every discussion ends in one of three declared states: decided, decided-pending-one-named- piece-of-information, or explicitly deferred with a date. "We discussed it" is not an outcome. Finally, separate the accuracy incentive from the popularity incentive. Ask people for their estimates privatel
--- [8] Chapter 8 — The Practicing Decider ---
## Chapter 8 — The Practicing Decider This notebook closes with a warning and a promise. The warning: none of these tools - the bet framing, the journal, the premortem - makes you certain. They do not reduce the uncertainty of the world by one iota. What they reduce is your error rate given that uncertainty, and your blindness to your own error rate. The promise: deciding well is a practice, not a talent. Every element in this book is a habit that compounds. The journal entries accumulate into calibration data. The premortems accumulate into pattern memory. The tripwires accumulate into an organization that can act without re-litigating. Where does the method fail? Three honest limits. It works poorly when the feedback loop is too slow - if outcomes take a decade, the journal cannot correct you within a career, and you should lean on base rates from other people's histories instead of your own. It works poorly for decisions that are ... l
...[truncated]
```

## Heuristic pre-classification (hint only - confirm or replace)

```yaml
primary_category: decision-making
confidence: 0.54
rationale: 'Keyword heuristic matched ''Decision Making'' most strongly (score 91
  vs runner-up psychology-behavior at 21) across title, chapter titles, and sampled
  body text. This is a hint only: method=heuristic, confidence capped at 0.6; an agent
  should confirm or replace it.'
alternative_categories:
- category: psychology-behavior
  confidence: 0.38
tags: []
method: heuristic

```

## Instructions

1. Read the digest above (and workspace/book/text.md as needed).
2. Pick exactly ONE primary category from taxonomy/categories.yaml:
   decision-making, investing-finance, business-strategy, psychology-behavior, research-science, learning-education, writing, communication-negotiation, productivity, leadership-management, technology-engineering, creativity-design, philosophy-thinking, health-performance, reference-knowledge, other
3. Judge honestly - confidence below 0.5 means genuinely torn.
4. Write classification.yaml (fields per the schema; set method: agent).
5. Run: `book2skill distill --workspace <workspace>` to validate and scaffold.
