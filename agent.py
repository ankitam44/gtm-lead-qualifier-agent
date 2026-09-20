"""Lead qualification / account research agent.

Given a target account (raw firmographic + intent signals), scores ICP fit
and produces AE-ready talking points using Claude's structured outputs.
"""

from typing import List, Literal

import anthropic
from pydantic import BaseModel, Field

MODEL = "claude-opus-5"

SYSTEM_PROMPT = """You are a GTM/sales-ops analyst at an enterprise SaaS company. \
You score inbound and outbound target accounts against our ICP rubric and hand \
the output to an Account Executive who has never researched this company before.

ICP rubric (weight roughly evenly, but use judgment):
- Company size / employee count fit for enterprise SaaS (200+ employees is a good fit; \
  under 50 is a poor fit unless there are strong growth signals)
- Industry / vertical fit
- Buying signals: recent funding, hiring surges in relevant roles (e.g. RevOps, IT, \
  Engineering leadership), tech stack mentions that suggest a gap our product fills
- Evidence of active pain (news, job postings describing a problem we solve, \
  leadership quotes, product reviews)
- Timing signals (funding round, new exec hire, expansion, M&A)

Be skeptical. If the input signals are thin, say so and lower the score rather than \
inventing evidence. Never fabricate facts not present in the provided signals."""


class ICPAssessment(BaseModel):
    fit_score: int = Field(ge=0, le=100, description="Overall ICP fit, 0-100")
    tier: Literal["A", "B", "C", "D"] = Field(
        description="A = prioritize now, B = qualified nurture, C = long-shot, D = disqualify"
    )
    reasoning: str = Field(description="2-4 sentence justification for the score")
    buying_signals: List[str] = Field(description="Concrete signals found in the input")
    risks: List[str] = Field(description="Reasons this account might not close or isn't a fit")
    recommended_talking_points: List[str] = Field(
        description="Specific, evidence-based talking points an AE can open with"
    )
    recommended_next_action: str = Field(
        description="One concrete next step, e.g. 'Route to AE for outbound this week'"
    )


def assess_account(
    account_name: str,
    domain: str,
    raw_signals: str,
    client: anthropic.Anthropic | None = None,
) -> ICPAssessment:
    client = client or anthropic.Anthropic()

    user_content = (
        f"Account: {account_name}\n"
        f"Domain: {domain}\n\n"
        f"Raw signals (news, job postings, firmographics, tech stack, funding, etc.):\n"
        f"{raw_signals.strip() or '(none provided)'}"
    )

    response = client.messages.parse(
        model=MODEL,
        max_tokens=2048,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_content}],
        output_format=ICPAssessment,
    )

    return response.parsed_output
