# Mallorca · A Fortnight for Two

A Streamlit app that serves the hand-designed Mallorca itinerary (2–14 July 2026)
as a shareable web page.

The itinerary itself lives in [`static/itinerary.html`](static/itinerary.html) —
a single, self-contained page (custom fonts, sticky nav, scroll-reveal
animations, and all photos inlined as base64, so there are no external image
assets to ship). [`streamlit_app.py`](streamlit_app.py) serves that page as a
static file and renders it full-screen in an iframe, hiding Streamlit's own
chrome so it reads as one polished site.

> This is a standalone repo, intentionally separate from the Eunice Platform.

## Run it locally

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Then open the URL it prints (usually http://localhost:8501).

## Deploy to Streamlit Community Cloud

1. Push this folder to its **own** GitHub repository (see below).
2. Go to https://share.streamlit.io → **New app**.
3. Pick the repo, branch `main`, and main file `streamlit_app.py`.
4. Deploy. No secrets or environment variables are required.

## Push to a new GitHub repo

This folder is already a git repo with an initial commit. To publish it:

```bash
# with the GitHub CLI
gh repo create mallorca-itinerary --private --source . --push

# or manually
git remote add origin https://github.com/<you>/mallorca-itinerary.git
git push -u origin main
```

## Editing the itinerary

Edit `static/itinerary.html` directly — it's plain HTML/CSS/JS. After saving,
reload the browser tab to see changes. To swap a photo, replace the
corresponding `data:image/...;base64,...` value in the relevant `<figure>`.
