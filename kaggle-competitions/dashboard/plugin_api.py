"""Dashboard API — GET /api/plugins/kaggle-competitions/submissions

Returns submission snapshots for all tracked competitions. Auth is handled by the
dashboard's own gate before this handler runs. Never logs tokens.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

# make kaggle_core importable regardless of how the dashboard imports us
_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from kaggle_core import _run_kaggle, best_score, load_state  # noqa: E402


def _data_dir() -> Path:
    base = os.environ.get("HERMES_HOME") or str(Path.home() / ".hermes")
    return Path(base) / "plugin-data" / "kaggle-competitions"


def _tracked() -> list[str]:
    import json
    cfg = Path(os.environ.get("HERMES_HOME") or Path.home() / ".hermes") / "config.yaml"
    try:  # light parse — just the competitions list under plugins.entries
        import yaml
        doc = yaml.safe_load(cfg.read_text()) or {}
        comps = (((doc.get("plugins") or {}).get("entries") or {})
                 .get("kaggle-competitions", {}).get("settings", {}) or {}).get("competitions") or []
        return [str(c) for c in comps]
    except Exception:
        pass
    state = load_state(_data_dir())
    return list(state.get("competitions", {}).keys())


def register(api):  # dashboard plugin API hook
    @api.get("/api/plugins/kaggle-competitions/submissions")
    def submissions(req):
        out = {}
        state = load_state(_data_dir())
        for comp in _tracked():
            cached = state.get("competitions", {}).get(comp)
            if cached and time.fresh(cached.get("last_poll", 0), minutes=10):
                rows = cached.get("rows", [])
            else:
                try:
                    rows = _run_kaggle(comp)
                except Exception as e:
                    out[comp] = {"error": str(e)[:150]}
                    continue
            out[comp] = {"best": best_score(rows), "count": len(rows), "recent": rows[:10]}
        return out


import time  # noqa: E402  (kept at bottom so register() stays at top for readers)


def fresh(ts: float, minutes: int) -> bool:  # helper referenced above
    return (time.time() - (ts or 0)) < minutes * 60
