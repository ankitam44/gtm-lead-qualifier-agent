"""Lead qualification / account research agent.

Given a target account (name + domain), the agent researches it itself using
Claude's web search tool, then scores ICP fit and produces AE-ready talking
points as validated structured output.
"""

import json
from typing import List, Literal

import anthropic
from pydantic import BaseModel, Field, ValidationError

MODEL = "claude-opus-5"

SYSTEM_PROMPT = """You are a GTM/sales-ops analyst at an enterprise SaaS company. \
You research and score inbound and outbound target accounts against our ICP rubric, \
then hand the output to an Account Executive who has never researched this company \
before.

Research the account using web search before scoring it. Look for: company size / \
employee count, industry, recent funding, hiring trends (especially RevOps, IT, \
Engineering leadership roles), leadership changes, news, and any public evidence of \
a pain point our product would solve. Use a handful of targeted searches (company \
name plus "funding", "careers", "employees", recent news) rather than one vague query.

ICP rubric (weight roughly evenly, but use judgment):
- Company size / employee count fit for enterprise SaaS (200+ employees is a good fit; \
  under 50 is a poor fit unless there are strong growth signals)
- Industry / vertical fit
- Buying signals: recent funding, hiring surges in relevant roles, tech stack mentions \
  that suggest a gap our product fills
- Evidence of active pain (news, job postings describing a problem we solve, \
  leadership quotes, product reviews)
- Timing signals (funding round, new exec hire, expansion, M&A)

Be skeptical. If your searches turn up thin or ambiguous evidence, say so and lower the \
score rather than inventing evidence. Never fabricate a fact you did not find via search. \
Once your research is sufficient, respond with the final JSON assessment and nothing else."""

OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "fit_score": {
            "type": "integer",
            "description": "Overall ICP fit, an integer from 0 to 100 inclusive",
        },
        "tier": {"type": "string", "enum": ["A", "B", "C", "D"]},
        "reasoning": {"type": "string"},
        "buying_signals": {"type": "array", "items": {"type": "string"}},
        "risks": {"type": "array", "items": {"type": "string"}},
        "recommended_talking_points": {"type": "array", "items": {"type": "string"}},
        "recommended_next_action": {"type": "string"},
        "sources": {
            "type": "array",
            "items": {"type": "string"},
            "description": "URLs of the sources actually used, if any were found",
        },
    },
    "required": [
        "fit_score",
        "tier",
        "reasoning",
        "buying_signals",
        "risks",
        "recommended_talking_points",
        "recommended_next_action",
        "sources",
    ],
    "additionalProperties": False,
}


class ICPAssessment(BaseModel):
    fit_score: int = Field(ge=0, le=100)
    tier: Literal["A", "B", "C", "D"]
    reasoning: str
    buying_signals: List[str]
    risks: List[str]
    recommended_talking_points: List[str]
    recommended_next_action: str
    sources: List[str]


def assess_account(
    account_name: str,
    domain: str,
    client: anthropic.Anthropic | None = None,
) -> ICPAssessment:
    client = client or anthropic.Anthropic()

    user_content = f"Research and score this account.\nCompany: {account_name}\nDomain: {domain}"

    response = client.messages.create(
        model=MODEL,
        max_tokens=8000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_content}],
        tools=[{"type": "web_search_20260209", "name": "web_search", "max_uses": 6}],
        output_config={"format": {"type": "json_schema", "schema": OUTPUT_SCHEMA}},
    )

    text_blocks = [b.text for b in response.content if b.type == "text"]
    if not text_blocks:
        raise RuntimeError(
            f"No text response returned (stop_reason={response.stop_reason}); "
            "the model may have stopped mid-search."
        )

    try:
        data = json.loads(text_blocks[-1])
        # The schema can't enforce numeric bounds server-side; clamp defensively
        # rather than hard-failing on an off-by-a-little score.
        if isinstance(data.get("fit_score"), int):
            data["fit_score"] = max(0, min(100, data["fit_score"]))
        return ICPAssessment.model_validate(data)
    except (json.JSONDecodeError, ValidationError) as e:
        raise RuntimeError(f"Model output did not match the expected schema: {e}") from e
