"""Deployment shim — not where the app lives.

The Streamlit Cloud app for this repo (ibiza-itinerary.streamlit.app) was
created with its **main module** set to `views/ibiza.py`, and Cloud fixes that
path at creation time. When this file was removed, Cloud could no longer start
the app at all:

    ❗️ The main module file does not exist: /mount/src/itinerary-playbook/views/ibiza.py

So this file stays, purely to keep that deployment alive, and simply runs the
real app at the repo root.

`runpy` (rather than `import streamlit_app`) is deliberate: an imported module
is cached in sys.modules and would not re-execute on rerun, so the app would
render once and then go blank. run_path executes it fresh every rerun, and sets
__file__ to the root script, so `STATIC = Path(__file__).parent / "static"`
still resolves to the repo root.

To retire this file: point the Cloud app's main file at `streamlit_app.py`
(Streamlit Cloud requires deleting and re-deploying the app to change it) and
delete `views/`. That also restores the raw `/app/static/<name>.html` URLs,
which Streamlit resolves relative to the main module's directory and which
therefore do not work while the entry point is in this subfolder.
"""

import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

runpy.run_path(str(ROOT / "streamlit_app.py"), run_name="__main__")
