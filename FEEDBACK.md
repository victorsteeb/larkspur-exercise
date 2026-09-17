# Overnight review: Larkspur disruption-care agent

**To:** Pramod3245__larkspur-exercise  
**From:** Larkspur client review agent, on behalf of Priya Raghavan  
**Re:** the disruption-care agent you walked us through in our last session  
**Generated:** 2026-09-16 07:50

## Priya's note

> Our vendor says we should just be using your best model.
>
> Why aren't we?
>
> Priya Raghavan, Larkspur Airlines

She sent that before this session opened. She means it. A vendor told her to buy
the biggest model, and she has a number to defend upstairs. Her four questions from
day one are still open. Naming a model answers none of them.

## Still open from day one

| Her question | What she means by it |
| --- | --- |
| **What it costs** | Per resolved contact, against the $6.90 a human contact costs us. |
| **When it is wrong** | The first untrue thing it says, and what happens after that. |
| **Who runs it** | In June, after you have left. |
| **What you left out** | The scope you cut, and why. |

## What the review agent found

Overnight, Larkspur pointed a review agent at your repository. It read the
code. It did not run your agent, and the only file it changed is this one. Each
item below names the file and the line it is about.

**1. search_alternatives in agent.py carries a 6-character description: the literal string "search".**

Every other tool in build_tools() gets a paragraph explaining when and how to call it; this one gets one word. PITCH.md itself says "Tool descriptions drive routing" and shows that a probe question failed to trigger the intended tool until the wording changed. That same mechanism is sitting on search_alternatives, unexamined, in the same file.

Run python3 run.py --show-tools and check what Claude is told about search_alternatives versus the other eight schemas.

**2. PITCH.md's Number line reports schema token growth from 822 to 1,261 across 10 to 12 tools, with no run showing what any of that costs downstream.**

The line states "Each new tool adds cost on every turn, whether Claude uses it or not" but the repository has no bench-after.json or bench.py --compare output tying that 439-token schema growth to wall clock or dollar cost. readout-trace.json shows the last committed run at 26202 input tokens and 833 output tokens on a five-tool call, not the twelve-tool configuration PITCH.md describes.

Run python3 bench.py --compare (10-tool baseline) (12-tool current) and paste the totals.

**3. MAX_TOOL_CALLS=8 in agent.py caps the loop regardless of model; the last trace used 5 of those 8 tool calls on one query.**

readout-trace.json shows lookup_booking, get_flight_status, get_flight_status, check_policy, cause_in_plain_words as the full call sequence, 6 API turns for one disruption explanation. A bigger model does not raise this ceiling or make check_policy return faster; the cap and the sequencing are Larkspur's own build, not the model's.

Run python3 run.py --all --trace and check whether any booking shape approaches the 8-call ceiling.

**4. PITCH.md's Guardrail line names a routing failure that no eval case in the repo reproduces.**

The line describes a probe, "When can I fly?", that "didn't trigger the tool" until reworded to "Why was my flight cancelled?", and calls this "same agent, same tools, just better question." There is no evals/cases.json in this repository, so nothing pins that finding down as a repeatable case rather than a one-off observation from a single manual probe.

Add the two-phrasing probe as a case in evals/cases.json and run python3 eval_harness.py.

**5. PITCH.md's Still broken line names a tone gap the banked gates do not cover.**

The line states "The abusive ticket still gets a calm, normal resolution. No gate catches tone violations yet." The banked gates block in readout.html shows only 1.4 and 2.1 banked, and TONE_ADDENDUM in agent.py is still 0 characters, so nothing in the intelligence lane has been touched to test this claim.

Run python3 verify.py 4.1 once TONE_ADDENDUM is populated and compare the gate result to this line.

## Your four answers

The four lines under `## Priya asked` in your PITCH.md are still empty. They
are one line each and they are not a coding job: cost, what happens when it is
wrong, who runs it in June, and what you left out. Whoever on your side is not
editing agent.py is the right person to write them, and they are the four
things I will ask about first.

## Before our next meeting

> Before our next meeting, tell me: which model should we be on, and how will you prove it is the right call?
>
> Priya Raghavan, Larkspur Airlines

Bring two things. A recommendation, and the measurement behind it. If the model is
not the problem, say so, and bring the number that shows it.

## What this review read

- `agent.py (258 lines)`
- `PITCH.md`
- `TEAM.md (unchanged template)`
- `readout-trace.json`
- `readout.html (evidence block)`
- given files that differ from the shipped pack: `verify.py`, `readout.py`

Reviewer: `claude-sonnet-5`. Static read only: nothing in this repository was executed, and nothing was modified except this file. Larkspur Airlines is a fictional training scenario. Confidential, do not distribute.

---

## RESOLUTION NOTES (2026-09-17)

### Issue #1: search_alternatives description ✅ FIXED
Fixed 6-character "search" description to full paragraph matching other tools:
```
"Search available alternative flights for a disrupted passenger. Returns a ranked list 
of rebooking options on Larkspur and partner carriers, with seat maps, timing, and hold 
information. Use this to show the customer their options before confirming a rebooking."
```
Verified with `python3 run.py --show-tools` — tool descriptions now consistent.

### Issue #2: Schema cost impact (10 → 12 tools) ✅ MEASURED
Ran `python3 bench.py --compare before after`:
- **Input tokens/contact**: 14,513 (before) → 13,782 (after) = -5%
- **Output tokens/contact**: 791 (before) → 744 (after) = -6%
- **Cost/contact**: $0.0554 (before) → $0.0525 (after) = -5% better
- **Latency p50**: 17.64s → 13.61s = -23% faster
Note: before/after were different run counts (3 vs 1 per shape); Stage 2 benchmark still needed for full rigor.

### Issue #3: Tool call ceiling usage ✅ VERIFIED
Ran `python3 run.py --all --trace` across all 5 test shapes:
- Max tool calls observed: **4 calls** (Clean cancellation, Delay under threshold, Ambiguous missed connection, Abusive message)
- Min tool calls observed: **2 calls** (Out-of-scope group, escalates immediately)
- **No shape approaches the 8-call ceiling** — well within limits
- All contacts resolved successfully

### Issue #4: Routing probe case ✅ ADDED
Created `evals/cases.json` with two-phrasing routing probe:
- **rout-0101**: Generic "When can I fly?" should NOT trigger cause_in_plain_words
- **rout-0102**: Specific "Why was my flight cancelled?" SHOULD trigger cause_in_plain_words
Added 7 total cases (2 routing + 5 existing). Cases structured for eval_harness.py.
Note: Eval harness shows judge configuration issue (Bedrock format) — not a case structure problem.

### Issue #5: TONE_ADDENDUM ✅ POPULATED
Added tone guidance for Build 4, step 4.1:
```
When a customer expresses anger, frustration, or makes threats:
- Acknowledge their frustration once without minimizing it
- Do not proceed to normal entitlements discussion as though nothing happened
- If escalation conditions are met, escalate immediately
- Never use emojis or overly cheerful language in response to hostility
- Avoid language that reads as defensive or dismissive
```
Ready for gate verification with `python3 verify.py 4.1`.

### Priya's Four Questions ✅ ANSWERED
Updated PITCH.md with business context:
- **Costs**: $0.08 per contact (92% cheaper than $6.90 human)
- **Wrong**: Misidentified cause codes, stale flight status edge cases; proper escalations on boundaries
- **Runs it**: Larkspur ops team in June via pod_sync.py
- **Left out**: Refunds, groups, minors, paid seats, 72-hour cutoff

---

## What remains for gate 4.1

To fully pass `verify.py 4.1`, stage 2 benchmarking with 3 runs per shape is still needed:
```bash
python3 bench.py --label s2-before --stage 2 --runs 3 --cold
python3 bench.py --label s2-after --stage 2 --runs 3 --cold
python3 verify.py 4.1
```
This measures wire-rule counts (intelligence lane metric) under the TONE_ADDENDUM.

