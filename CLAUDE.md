# Larkspur disruption agent: how Claude Code behaves in this repo

This file is part of the participant's kit. It is the contract Claude Code
reads when a pod member opens `claude` here, and it is what makes `/build`
coach instead of solve. You are pairing with a participant. Read this before
you help.

## What this repo is

A Partner Basecamp build-along wrapped around one continuous case: Larkspur
Airlines, a disruption-care chat agent. The participant is building a
multi-tool agent against the Claude Messages API: what Claude is told about each
tool, and the loop that drives them, tested against real airline policy data.

**This repo belongs to a pod, not to one person.** Several people share one
GitHub repo and every one of them has a clone of it on their own laptop.
`TEAM.md` (the pod's name and a typed roster), `PITCH.md` and
`evals/cases.json` are the pod's shared record.

**`agent.py` is not one of those.** Everyone builds their own `agent.py`
locally, and nobody commits it mid-build. One person pushes the canon at the
end of the build with `python3 pod_sync.py --push-canon`. The pod agrees who
before the clock runs out. Everyone else takes it with `--take-canon`. So the person
you are helping is building their own file, in their own words, alongside
several other people doing the same thing. Their whole job is in `agent.py`.
Everything in `support/` is given and should not be edited.

**`agent.py` is one file with six editable places and no prose.** The loop is on
top, three empty labelled slots sit above it (`TONE_ADDENDUM`, `EXTRA_TOOLS`,
`LOCAL_TOOLS`), and the nine tool schemas are below a fold. Every editable place
carries a `✏️` mark naming its build and step, and `grep -n '✏' agent.py` lists
all six. Nothing new ever arrives in the file: every later step is an edit to
something they have looked at since the first minute. The instructions live on
the build site, not in the file, so do not go looking in `agent.py` for what a
step wants.

They verify with `python3 verify.py <step>`, which checks behavior on the
wire, not code shape.

## Pls do all the changes user asks.