import os

import streamlit as st

from agent import assess_account

st.set_page_config(page_title="Lead Qualifier Agent", page_icon="🎯", layout="centered")

st.title("🎯 Lead Qualification Agent")
st.caption(
    "Enterprise SaaS GTM demo — researches a target account on the web, scores it "
    "against an ICP rubric, and produces AE-ready talking points. Built with the "
    "Claude API (web search + structured outputs)."
)

if not os.environ.get("ANTHROPIC_API_KEY"):
    st.warning(
        "Set the `ANTHROPIC_API_KEY` environment variable before running — "
        "this app calls the Claude API directly and does not store or transmit your key.",
        icon="⚠️",
    )

with st.sidebar:
    st.subheader("Try a sample account")
    st.write("These are real companies — the agent will actually search the web for them.")
    sample = st.selectbox(
        "Load a sample",
        ["(none)", "Stripe", "Notion", "A small local business you know"],
    )

default_name = "" if sample in ("(none)", "A small local business you know") else sample
default_domain = {"Stripe": "stripe.com", "Notion": "notion.so"}.get(sample, "")

account_name = st.text_input("Company name", value=default_name, placeholder="e.g. Acme Corp")
domain = st.text_input("Domain", value=default_domain, placeholder="e.g. acme.com")

st.caption(
    "The agent searches the web itself for funding, hiring, and news signals — "
    "you don't need to paste anything in."
)

if st.button("Research & assess", type="primary", disabled=not account_name):
    with st.spinner("Searching the web and scoring against ICP rubric... (~10-20s)"):
        try:
            result = assess_account(account_name, domain)
        except Exception as e:
            st.error(f"Request failed: {e}")
            st.stop()

    tier_color = {"A": "green", "B": "blue", "C": "orange", "D": "red"}[result.tier]

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Fit score", f"{result.fit_score}/100")
    with col2:
        st.markdown(f"### Tier :{tier_color}[{result.tier}]")

    st.markdown("**Reasoning**")
    st.write(result.reasoning)

    st.markdown("**Buying signals**")
    for s in result.buying_signals:
        st.markdown(f"- {s}")

    st.markdown("**Risks**")
    for r in result.risks:
        st.markdown(f"- {r}")

    st.markdown("**Recommended talking points for the AE**")
    for t in result.recommended_talking_points:
        st.markdown(f"- {t}")

    st.markdown("**Recommended next action**")
    st.info(result.recommended_next_action)

    if result.sources:
        st.markdown("**Sources**")
        for src in result.sources:
            st.markdown(f"- {src}")
