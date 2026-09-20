import os

import streamlit as st

from agent import assess_account
from sample_accounts import SAMPLE_ACCOUNTS

st.set_page_config(page_title="Lead Qualifier Agent", page_icon="🎯", layout="centered")

st.title("🎯 Lead Qualification Agent")
st.caption(
    "Enterprise SaaS GTM demo — scores a target account against an ICP rubric and "
    "produces AE-ready talking points. Built with the Claude API (structured outputs)."
)

if not os.environ.get("ANTHROPIC_API_KEY"):
    st.warning(
        "Set the `ANTHROPIC_API_KEY` environment variable before running — "
        "this app calls the Claude API directly and does not store or transmit your key.",
        icon="⚠️",
    )

with st.sidebar:
    st.subheader("Demo accounts")
    st.write("Enrichment normally comes from Clearbit/LinkedIn/Crunchbase-style APIs. "
             "For this demo, pick a mock account or paste your own signals.")
    chosen = st.selectbox("Load a sample account", ["(none)"] + list(SAMPLE_ACCOUNTS.keys()))

default_name = ""
default_domain = ""
default_signals = ""
if chosen != "(none)":
    default_name = chosen
    default_domain = SAMPLE_ACCOUNTS[chosen]["domain"]
    default_signals = SAMPLE_ACCOUNTS[chosen]["raw_signals"]

account_name = st.text_input("Account name", value=default_name)
domain = st.text_input("Domain", value=default_domain)
raw_signals = st.text_area(
    "Raw signals (news, job postings, firmographics, tech stack, funding...)",
    value=default_signals,
    height=220,
)

if st.button("Assess account", type="primary", disabled=not account_name):
    with st.spinner("Scoring account against ICP rubric..."):
        try:
            result = assess_account(account_name, domain, raw_signals)
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
