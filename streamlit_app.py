"""
Mallorca · A Fortnight for Two — a Streamlit wrapper around the
self-contained itinerary page.

The itinerary is a bespoke, hand-designed HTML page (custom fonts, sticky
nav, scroll-reveal animations, inline base64 photos). Rather than rebuild
all of that with Streamlit widgets and lose the design, we render the page
exactly as-is inside a full-viewport iframe and hide Streamlit's own chrome
so the result reads as a single, polished web page.

The page also lives in ./static, so with `server.enableStaticServing` on
(see .streamlit/config.toml) it's reachable directly — handy for sharing the
raw page on its own: <app-url>/app/static/itinerary.html
"""

from pathlib import Path

import streamlit as st

PAPER = "#f6efe1"  # matches the itinerary's --paper background (no white flash)
ITINERARY = Path(__file__).parent / "static" / "itinerary.html"

st.set_page_config(
    page_title="Mallorca · A Fortnight for Two",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="collapsed",
)


@st.cache_data(show_spinner=False)
def load_itinerary() -> str:
    return ITINERARY.read_text(encoding="utf-8")


# Strip Streamlit's chrome and all padding so the itinerary fills the window.
# The page is designed to live in a scrolling viewport (sticky nav, fixed
# grain overlay, reveal-on-scroll), so we give the iframe the full viewport
# height and let it scroll internally — that reproduces the original exactly.
st.markdown(
    f"""
    <style>
      #MainMenu {{visibility: hidden;}}
      header[data-testid="stHeader"] {{display: none;}}
      [data-testid="stToolbar"] {{display: none;}}
      [data-testid="stDecoration"] {{display: none;}}
      footer {{visibility: hidden;}}

      .stApp,
      [data-testid="stAppViewContainer"],
      [data-testid="stMain"] {{background: {PAPER};}}

      .block-container,
      [data-testid="stMainBlockContainer"] {{
          padding: 0 !important;
          margin: 0 !important;
          max-width: 100% !important;
      }}
      [data-testid="stMain"] {{padding: 0 !important;}}
      [data-testid="stVerticalBlock"],
      [data-testid="element-container"] {{gap: 0 !important;}}

      /* The itinerary iframe fills the viewport and scrolls internally. */
      [data-testid="stAppViewContainer"] iframe {{
          height: 100vh !important;
          width: 100% !important;
          border: none !important;
          display: block;
      }}

      html, body {{overflow: hidden;}}  /* outer page is fixed; iframe scrolls */
    </style>
    """,
    unsafe_allow_html=True,
)

# Render the page as the iframe's srcdoc. `st.iframe` is the modern API;
# older Streamlit versions use the (now-deprecated) components.html. Either
# way the height is just a fallback — the CSS above forces the iframe to fill
# the viewport, and the itinerary scrolls internally.
itinerary = load_itinerary()
if hasattr(st, "iframe"):
    st.iframe(itinerary, height=900)
else:  # Streamlit < ~1.49
    import streamlit.components.v1 as components

    components.html(itinerary, height=900, scrolling=True)
