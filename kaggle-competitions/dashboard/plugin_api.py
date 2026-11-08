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
    base = os.environ.get("HERMES_HOME") or str(Path.home() / ".hermes")
    return Path(base) / "plugin-data" / "kaggle-competitions"


def _tracked() -> list[str]:
    cfg = Path(os.environ.get("HERMES_HOME") or Path.home() / ".hermes") / "config.yaml"
    try:
        import yaml
        doc = yaml.safe_load(cfg.read_text()) or {}
        comps = (((doc.get("plugins") or {}).get("entries") or {})
                 .get("kaggle-competitions", {}).get("settings", {}) or {}).get("competitions") or []
        return [str(c) for c in comps]
    except Exception:
        state = load_state(_data_dir())
        return list(state.get("competitions", {}).keys())


def _is_fresh(ts) -> bool:
    return (time.time() - (ts or 0)) < _CACHE_TTL_SECONDS


def _kaggle_env() -> dict:
    """Kaggle CLI env: the CLI reads ~/.kaggle/kaggle.json itself. We only inject
    KAGGLE_API_TOKEN from a local .env when present. Never logs the token."""
    env = dict(os.environ)
    if env.get("KAGGLE_API_TOKEN"):
        return env
    for cand in ("~/.hermes/kaggle/.env",):
        p = Path(os.path.expanduser(cand))
        if p.is_file():
            try:
                for line in p.read_text().splitlines():
                    if line.startswith("KAGGLE_API_TOKEN="):
                        env["KAGGLE_API_TOKEN"] = line.split("=", 1)[1].strip()
                        break
            except OSError:
                pass
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
