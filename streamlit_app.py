"""Itinerary Playbook — a small collection of hand-designed trip itineraries.

Each itinerary is a self-contained HTML page in ./static with its own art
direction. This entry point just wires them up as navigable pages; the
rendering itself lives in shared.py.

With `server.enableStaticServing` on (see .streamlit/config.toml) every page
is also reachable raw, with no Streamlit chrome at all, at:
    <app-url>/app/static/<name>.html
"""

import streamlit as st

st.set_page_config(
    page_title="Itinerary Playbook",
    page_icon="🌅",
    layout="wide",
    initial_sidebar_state="expanded",
)

PAGES = [
    st.Page("views/ibiza.py", title="Ibiza", icon="🌴", url_path="ibiza", default=True),
    st.Page("views/mallorca.py", title="Mallorca", icon="🌊", url_path="mallorca"),
]

st.navigation(PAGES).run()
