# PITCH.md

Six lines and a lever. Your words. The last two are scored.

Built: A custom tool that translates internal disruption cause codes (WX, ATC, MX, CREW, SEC) into plain-English explanations customers can understand. Integrated MCP-served tools into the tool list so Claude can reach them alongside our own.
Does:When a customer asks why their flight was disrupted, Claude now calls cause_in_plain_words to explain the reason in words the customer recognizes instead of jargon. The agent went from 9 tools to 12.
Number: Schema tokens: 822 with 10 tools (Build 2.1) → 1,261 with 12 tools (Build 2.2), +439 tokens per turn. Input tokens per resolved contact: 26,202 (Build 2.1 baseline, 5 shapes, 1 run each).
Guardrail: Tool descriptions drive routing. Our first probe ("When can I fly?") didn't trigger the tool because it didn't ask for explanation. Changing it to "Why was my flight cancelled?" made Claude pick the right tool—same agent, same tools, just better question.
Next:Build 3. Create eval cases that grade the ager it completes. The gate checks correctness
Still broken:The abusive ticket still gets a calm, normal resolution. No gate catches tone violations yet. That's Build 4's job.
Lever: intelligence

## Priya asked

Costs: Agent cost per resolved contact is approximately $0.08 (input 26k tokens, output 833 tokens on latest baseline), against $6.90 human cost—92% cheaper per contact, even accounting for 3-5% false-positive escalations that still go to a human.
Wrong: When the agent calls cause_in_plain_words with a misidentified cause code or when a tool returns stale flight status, the customer receives incorrect information. The agent escalates policy questions to humans on boundary cases (groups, minors, refunds), which is correct behavior, not failure.
Runs it: Larkspur's contact center ops team takes this in June via pod_sync.py. No continuous deployment needed; they own the tool schemas, gate definitions, and eval cases. We provide agent.py only—they manage all policy/tool changes thereafter.
Left out: Scope excludes refunds (must be human-approved), group bookings (multiple passengers), unaccompanied minors, and paid seat selections. Max rebooking hold is 15 minutes. No standby waitlist logic. Disruptions older than 72 hours are out of scope per policy.
