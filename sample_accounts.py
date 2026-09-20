"""Mock enrichment data — stands in for a live Clearbit/LinkedIn/Crunchbase pull.

In production this data would come from enrichment APIs; here it's hand-written
so the demo runs without external API keys or scraping.
"""

SAMPLE_ACCOUNTS = {
    "Northwind Logistics": {
        "domain": "northwindlogistics.com",
        "raw_signals": """\
- 850 employees, freight & supply chain, HQ Chicago
- Raised $40M Series C 3 months ago (TechCrunch)
- Posted 6 open roles in the last 30 days: 2x RevOps Manager, 1x Director of Sales Ops, \
3x Enterprise AE
- CRO quoted in a logistics trade publication: "our sales team is drowning in manual \
account research and our forecast accuracy is embarrassing"
- Currently listed as a Salesforce customer (LinkedIn job posting mentions \
"Salesforce, Outreach, and spreadsheets" as their current sales stack)
- No mention of any AI/GTM tooling vendor in job postings or press""",
    },
    "Bramblewood Studios": {
        "domain": "bramblewoodstudios.io",
        "raw_signals": """\
- 18 employees, indie game studio
- No funding announcements found
- One job posting: Unity Developer
- No sales team job postings, no RevOps mentions
- Twitter presence focused on game dev community, no enterprise buying signals""",
    },
    "Solace Health Systems": {
        "domain": "solacehealthsystems.com",
        "raw_signals": """\
- 3,200 employees, healthcare provider network
- Announced a new Chief Digital Officer 6 weeks ago (press release)
- New CDO's LinkedIn post: "modernizing how our regional sales and partnerships teams \
engage health systems is priority one this year"
- Job postings: 1x VP of Partnerships, 1x Sales Enablement Manager
- Existing vendor stack unclear — no explicit CRM or sales tool mentioned publicly
- Heavily regulated industry (HIPAA); average enterprise sales cycles reported at 9-12 months \
in an industry report""",
    },
}
