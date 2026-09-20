# Lead Qualification Agent

**Problem:** Enterprise SaaS AEs spend a meaningful chunk of their week doing manual
account research before a first outbound touch — checking company size, funding,
hiring trends, and tech stack, then guessing at talking points. Reps triage inconsistently,
and reps with better research skills simply outperform reps without them.

**What this agent does:** Takes a company name and domain, researches the account
itself using Claude's web search tool (funding news, job postings, headcount, leadership
changes), and returns:

- An ICP fit score (0–100) and tier (A/B/C/D)
- The specific buying signals it found via search (not invented ones — the prompt
  explicitly penalizes thin/ambiguous evidence rather than fabricating it)
- Risks that might sink the deal
- AE-ready talking points grounded in the evidence
- A single recommended next action
- The source URLs it actually used

**Target user:** SDR/AE, or a RevOps team building automated lead routing.

**Why it matters for GTM:** This is the same shape of problem Clay, Common Room, and
most "AI SDR" tooling are built around — automating the qualification step so reps
spend their time on outreach and conversation, not research. Building even a rough
version demonstrates understanding of the actual bottleneck (research time, inconsistent
triage) rather than just "AI can summarize things."

**What's mocked vs. real:** Nothing here is mocked — the agent performs live web
searches via Claude's `web_search` server tool and scores whatever it actually finds.
A thin or ambiguous search result correctly produces a low, hedged score rather than a
confident fabrication; that's the intended behavior, not a bug. In production you'd
likely pair this with (or fall back to) a dedicated enrichment API like Clearbit or
Crunchbase for structured firmographic fields the model can't reliably find via search
(exact headcount, precise funding round size, etc.).

**Metrics you'd track in production:** % of A/B-tier leads that convert to meetings,
time-to-first-touch after a lead is scored, AE override rate (how often reps disagree
with the tier — a high override rate means the rubric needs tuning).

## Running it

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your-key-here
streamlit run app.py
```

Type any real company's name and domain and click "Research & assess" — no manual signal
paste-in needed. Web search adds a few seconds of latency (~10–20s per run) and a small
per-run cost on top of the base model call.
