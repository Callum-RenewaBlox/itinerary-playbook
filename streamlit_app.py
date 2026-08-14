"""Itinerary Playbook — a small collection of hand-designed trip itineraries.

Each itinerary is a self-contained HTML page in ./static with its own art
direction. Rather than rebuild any of that with Streamlit widgets and lose the
design, each page is rendered as-is inside a full-viewport iframe, with
Streamlit's chrome stripped back to just the sidebar nav.

Deliberately a SINGLE file with no local imports. Streamlit Cloud executes
page scripts without the app root on sys.path, so a `from shared import ...`
inside a pages/ file raises ModuleNotFoundError on deploy even though it works
locally. Defining the pages as callables here avoids that failure mode
entirely — see the `st.Page(...)` calls at the bottom.

With `server.enableStaticServing` on (see .streamlit/config.toml) every page is
also reachable raw, with no Streamlit chrome at all, at:
    <app-url>/app/static/<name>.html
"""

from pathlib import Path

import streamlit as st

STATIC = Path(__file__).parent / "static"

st.set_page_config(
    page_title="Itinerary Playbook",
    page_icon="🌅",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data(show_spinner=False)
def _read(path: str, _mtime: float) -> str:
    return Path(path).read_text(encoding="utf-8")


def load_page(filename: str) -> str:
    """Read an itinerary from ./static.

    Cached on (path, mtime) rather than path alone, so editing the HTML is
    picked up on the next rerun instead of serving a stale copy forever.
    """
    page = STATIC / filename
    return _read(str(page), page.stat().st_mtime)


def render_itinerary(filename: str, bg: str, accent: str = "#FF2E8B") -> None:
    """Render a self-contained itinerary page full-bleed.

    `bg` should match the page's own background colour so the surrounding
    Streamlit chrome blends into it instead of flashing a different shade.
    """
    st.markdown(
        f"""
        <style>
          /* --- strip Streamlit chrome, keep the sidebar nav usable ---
             The button that re-opens a collapsed sidebar lives *inside* the
             header toolbar, so the header cannot simply be display:none or
             collapsing the sidebar would strand you with no way back. Instead
             the header becomes a zero-height, click-through overlay and only
             the chrome inside it is hidden. */
          #MainMenu, footer,
          [data-testid="stDecoration"], [data-testid="stStatusWidget"],
          [data-testid="stToolbarActions"], [data-testid="stAppDeployButton"],
          [data-testid="stMainMenu"], [data-testid="stMainMenuButton"] {{
              display: none !important;
          }}
          header[data-testid="stHeader"] {{
              background: transparent !important;
              height: 0 !important;
              min-height: 0 !important;
              pointer-events: none !important;
              z-index: 1000 !important;
          }}

          /* ...but the re-open control stays visible and clickable */
          [data-testid="stExpandSidebarButton"] {{
              display: flex !important;
              pointer-events: auto !important;
              position: fixed !important;
              top: .55rem !important;
              left: .55rem !important;
              z-index: 1002 !important;
              background: rgba(0, 0, 0, .45) !important;
              color: #fff !important;
              border: 1px solid rgba(255, 255, 255, .22) !important;
              border-radius: 8px !important;
              backdrop-filter: blur(8px);
          }}

          .stApp,
          [data-testid="stAppViewContainer"],
          [data-testid="stMain"] {{background: {bg};}}

          /* full bleed: no padding, no max width, no gaps */
          .block-container,
          [data-testid="stMainBlockContainer"] {{
              padding: 0 !important;
              margin: 0 !important;
              max-width: 100% !important;
          }}
          [data-testid="stMain"] {{padding: 0 !important;}}
          [data-testid="stVerticalBlock"],
          [data-testid="element-container"] {{gap: 0 !important;}}

          /* the itinerary fills the viewport and scrolls internally */
          [data-testid="stAppViewContainer"] iframe {{
              height: 100vh !important;
              width: 100% !important;
              border: none !important;
              display: block;
          }}
          html, body {{overflow: hidden;}}

          /* --- sidebar, themed to the itinerary on screen --- */
          [data-testid="stSidebar"] {{
              background: {bg};
              border-right: 1px solid rgba(255, 255, 255, .10);
          }}
          [data-testid="stSidebarNav"] a[aria-current="page"] {{
              border-left: 2px solid {accent};
          }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.iframe(load_page(filename), height=900)


def ibiza() -> None:
    """Ibiza · 2–9 September 2026."""
    render_itinerary("ibiza.html", bg="#06050A", accent="#FF2E8B")


def mallorca() -> None:
    """Mallorca · 2–14 July 2026."""
    render_itinerary("mallorca.html", bg="#f6efe1", accent="#c2562f")


PAGES = [
    st.Page(ibiza, title="Ibiza", icon="🌴", url_path="ibiza", default=True),
    st.Page(mallorca, title="Mallorca", icon="🌊", url_path="mallorca"),
]

st.navigation(PAGES).run()
