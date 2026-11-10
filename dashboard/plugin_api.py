"""Dashboard API — mounted under /api/plugins/kaggle-competitions/ by the web server.

Exposes a FastAPI ``router`` (the contract the web server's importer expects).
Returns submission snapshots for all tracked competitions. Auth is enforced by the
server's auth wall before this router runs. Never logs tokens.
"""
from __future__ import annotations

import os
import sys
import time
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_PLUGIN_ROOT = _HERE.parent  # kaggle_core.py lives at the plugin root, beside dashboard/
for _p in (str(_HERE), str(_PLUGIN_ROOT)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from fastapi import APIRouter  # noqa: E402

from kaggle_core import _run_kaggle, best_score, load_state  # noqa: E402

router = APIRouter()

_CACHE_TTL_SECONDS = 600


def _data_dir() -> Path:
    from hermes_constants import get_hermes_home
    return get_hermes_home() / "plugin-data" / "kaggle-competitions"


def _tracked() -> list[str]:
    """Tracked slugs from Hermes's config loader (same source the settings form
    writes), falling back to competitions already present in plugin state."""
    try:
        from hermes_cli.config import load_config
        doc = load_config() or {}
        comps = (((doc.get("plugins") or {}).get("entries") or {})
                 .get("kaggle-competitions", {}).get("settings", {}) or {}).get("competitions") or []
        if comps:
            return [str(c) for c in comps]
    except Exception:
        pass
    state = load_state(_data_dir())
    return list(state.get("competitions", {}).keys())


def _is_fresh(ts) -> bool:
    return (time.time() - (ts or 0)) < _CACHE_TTL_SECONDS


def _kaggle_env() -> dict:
    """Minimal, explicit environment for the kaggle CLI child process — never the
    inherited environment. Auth: KAGGLE_API_TOKEN via Hermes's secret scope
    (declared secret in plugin.yaml); if absent the CLI reads
    ~/.kaggle/kaggle.json itself. Never logs the token."""
    env: dict[str, str] = {}
    for key in ("PATH", "HOME", "LANG", "LC_ALL",
                "HTTP_PROXY", "HTTPS_PROXY", "NO_PROXY",
                "http_proxy", "https_proxy", "no_proxy"):
        value = os.environ.get(key)
        if value:
            env[key] = value
    try:
        from agent.secret_scope import get_secret
        token = get_secret("KAGGLE_API_TOKEN")
    except Exception:
        token = None
    if token:
        env["KAGGLE_API_TOKEN"] = token
    return env


@router.get("/submissions")
def submissions():
    out = {}
    env = _kaggle_env()
    state = load_state(_data_dir())
    for comp in _tracked():
        cached = state.get("competitions", {}).get(comp) or {}
        rows = cached.get("rows", [])
        if not _is_fresh(cached.get("last_poll", 0)):
            try:
                rows = _run_kaggle(comp, env)
                state.setdefault("competitions", {}).setdefault(comp, {})
                state["competitions"][comp] = {"rows": rows, "last_poll": time.time()}
                try:
                    import json
                    _data_dir().mkdir(parents=True, exist_ok=True)
                    (_data_dir() / "state.json").write_text(json.dumps(state, indent=1))
                except Exception:
                    pass
            except Exception as e:
                out[comp] = {"error": str(e)[:150]}
                continue
        out[comp] = {"best": best_score(rows), "count": len(rows), "recent": rows[:10]}
    return out
