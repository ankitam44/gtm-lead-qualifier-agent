# Lead Qualification Agent

**Problem:** Enterprise SaaS AEs spend a meaningful chunk of their week doing manual
account research before a first outbound touch — checking company size, funding,
hiring trends, and tech stack, then guessing at talking points. Reps triage inconsistently,
and reps with better research skills simply outperform reps without them.

**What this agent does:** Takes raw signals about a target account (funding news, job
postings, tech stack mentions, leadership quotes — anything a rep would normally
Google) and returns:

- An ICP fit score (0–100) and tier (A/B/C/D)
- The specific buying signals it found (not invented ones — the prompt explicitly
  penalizes thin evidence rather than fabricating it)
- Risks that might sink the deal
- AE-ready talking points grounded in the evidence
- A single recommended next action

**Target user:** SDR/AE, or a RevOps team building automated lead routing.

**Why it matters for GTM:** This is the same shape of problem Clay, Common Room, and
most "AI SDR" tooling are built around — automating the qualification step so reps
spend their time on outreach and conversation, not research. Building even a rough
version demonstrates understanding of the actual bottleneck (research time, inconsistent
triage) rather than just "AI can summarize things."

**What's mocked vs. real:**
- Mocked: account enrichment (`sample_accounts.py`) — in production this would come from
  Clearbit, LinkedIn Sales Navigator, Crunchbase, or a similar enrichment API.
- Real: the scoring and reasoning logic, which calls Claude via structured outputs
  (`client.messages.parse`) to guarantee a validated JSON response.

**Metrics you'd track in production:** % of A/B-tier leads that convert to meetings,
time-to-first-touch after a lead is scored, AE override rate (how often reps disagree
with the tier — a high override rate means the rubric needs tuning).

## Running it

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your-key-here
streamlit run app.py
```

Pick a sample account from the sidebar, or paste your own raw signals for any company.
