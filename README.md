# Itinerary Playbook

A small Streamlit app that serves hand-designed trip itineraries as shareable web pages.

| Itinerary | When | Page |
|---|---|---|
| **Ibiza** — a week of it | 2–9 September 2026 | [`static/ibiza.html`](static/ibiza.html) |
| **Mallorca** — a fortnight for two | 2–14 July 2026 | [`static/mallorca.html`](static/mallorca.html) |

Each itinerary is a single **self-contained HTML page** with its own art direction — its own
fonts, palette, layout and motion. [`streamlit_app.py`](streamlit_app.py) wires them up as
navigable pages and [`shared.py`](shared.py) renders each one full-bleed, hiding Streamlit's
chrome so the itinerary itself is all you see.

> Deliberately a standalone repo, separate from the Eunice Platform.

## Run it locally

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Deploy

On [share.streamlit.io](https://share.streamlit.io) → **Create app**, pick this repo, branch
`main`, main file `streamlit_app.py`. No secrets required.

Because `server.enableStaticServing` is on, every itinerary is *also* reachable raw, with no
Streamlit chrome at all — handy for sharing a single page on its own:

```
<app-url>/app/static/ibiza.html
<app-url>/app/static/mallorca.html
```

## The Ibiza page — "the 20:15 line"

The page is lit by one sunset. A single scalar `--sunpos` runs `1 → 0` with scroll depth and is
warped so the sun touches the water *exactly* when the beaches section reaches the middle of the
screen — which is where the real 20:15 sunset lives in the itinerary. The sun is never faded out
to fake depth: the sea and Es Vedrà are painted on top of it, so the occlusion is real.

Around that: an eclipse that takes the daylight away over the big-nights and hard-truths
sections, a 6am dawn under the footer, a follow spot that tracks the centred club card, a
split-flap departure board in the sticky bar, scroll reveals, and a time spine that fills down
each day's schedule as it arrives.

**The invariant.** The light system may only ever write `--sunpos`, `--k-*` and `--ecl`. It may
never write `--ink`, `--muted`, `--panel` or `--line`, and never lays light behind body copy —
the whole layer sits at `z-index:-1`. Text contrast is therefore identical at every scroll
position, by construction. This is a document two people read on a phone at 4am; information
always beats decoration.

Practical consequences of that rule:

- **`--sunpos`, not `--sun`** — `--sun` is already the amber colour token in `:root`.
- **Reduced motion** — `prefers-reduced-motion: reduce` stops everything and defaults the house
  lights to off. There is also a **LIGHTS** switch in the bar that kills the system outright; the
  choice is remembered.
- **No idle cost** — one rAF-throttled scroll listener, quantised to 20 steps. Stop scrolling and
  it stops doing anything at all.
- **Nothing gets stuck invisible** — reveal classes are added *by* JavaScript, so if scripting
  fails the page is simply fully visible, and a failsafe un-hides everything regardless.
- **No fake clocks.** The only times on the page are ones you can catch a bus with.

## Editing an itinerary

Edit the HTML in `static/` directly — it's plain HTML/CSS/JS with no build step. The loader is
cached on file mtime, so a save is picked up on the next rerun.
