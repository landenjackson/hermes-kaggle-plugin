"""Tool handlers — the code that runs when the agent calls each tool.

ctx is captured once in register() (the gateway does not pass ctx per call).
Secrets resolve through Hermes's secret scope; the CLI child gets a minimal env.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
from pathlib import Path

from hermes_constants import get_hermes_home

from . import kaggle_core

_SECRET_NAME = "KAGGLE_API_TOKEN"
_SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,100}$")
_CTX = None  # PluginContext, set by register()


def set_ctx(ctx) -> None:
    global _CTX
    _CTX = ctx


def data_dir() -> Path:
    return get_hermes_home() / "plugin-data" / "kaggle-competitions"


def _child_env() -> dict:
    """Minimal, explicit environment for the kaggle CLI child process — never the
    inherited environment. Auth: KAGGLE_API_TOKEN via Hermes's secret scope
    (declared secret in plugin.yaml). If absent, the CLI reads
    ~/.kaggle/kaggle.json itself. The token value is never logged or echoed."""
    env: dict[str, str] = {}
    for key in ("PATH", "HOME", "LANG", "LC_ALL",
                "HTTP_PROXY", "HTTPS_PROXY", "NO_PROXY",
                "http_proxy", "https_proxy", "no_proxy"):
        value = os.environ.get(key)
        if value:
            env[key] = value
    try:
        from agent.secret_scope import get_secret
        token = get_secret(_SECRET_NAME)
    except Exception:
        token = None
    if token:
        env[_SECRET_NAME] = token
    return env


def _tracked() -> list[str]:
    comps = (_CTX.get_config("competitions") if _CTX is not None else None) or []
    if comps:
        return [str(c) for c in comps]
    state = kaggle_core.load_state(data_dir())
    return list(state.get("competitions", {}).keys())


def _validate_slug(comp: str) -> str | None:
    """Returns an error message if the slug is invalid, else None."""
    if not comp:
        return "competition=<slug> required"
    if not _SLUG_RE.match(comp):
        return (f"invalid competition slug {comp[:40]!r}: must match "
                "^[a-z0-9][a-z0-9-]{0,100}$ (a leading '-' would become a CLI option)")
    return None


def _validate_top(top) -> int:
    try:
        value = int(top)
    except (TypeError, ValueError):
        return 10
    return max(1, min(100, value))


def kaggle_list_submissions(args: dict, **kwargs) -> str:
    """List submissions for a competition (or all tracked ones)."""
    comp = (args.get("competition") or "").strip()
    comps = [comp] if comp else _tracked()
    if not comps:
        return json.dumps({"error": "No competition given and none tracked. "
                                    "Set plugins.entries.kaggle-competitions.settings.competitions "
                                    "to a list of slugs, or pass competition=<slug>."})
    out = {}
    for c in comps:
        if err := _validate_slug(c):
            out[c] = {"error": err}
            continue
        try:
            res = kaggle_core.poll_once(c, data_dir(), _child_env())
            rows = res["rows"]
            out[c] = {"best": kaggle_core.best_score(rows), "count": len(rows), "recent": rows[:10]}
        except Exception as e:
            out[c] = {"error": str(e)[:200]}
    return json.dumps(out)


def kaggle_score_history(args: dict, **kwargs) -> str:
    """Full score history for one competition, oldest first."""
    comp = (args.get("competition") or "").strip()
    if not comp:
        tracked = _tracked()
        if not tracked:
            return json.dumps({"error": "No competition given and none tracked."})
        comp = tracked[0]
    if err := _validate_slug(comp):
        return json.dumps({"error": err})
    try:
        res = kaggle_core.poll_once(comp, data_dir(), _child_env())
    except Exception as e:
        return json.dumps({"error": str(e)[:200]})
    rows = sorted(res["rows"], key=lambda r: r["date"])
    scores = [float(r["score"]) for r in rows if r.get("score")]
    return json.dumps({
        "competition": comp,
        "best": max(scores) if scores else None,
        "n": len(rows),
        "history": [{"date": r["date"], "score": r["score"], "desc": r["desc"]} for r in rows],
    })


def kaggle_watch(args: dict, **kwargs) -> str:
    """Poll all tracked competitions now; report NEW completed scores since last check."""
    out: dict = {"new_results": [], "checked": [], "errors": []}
    for c in _tracked():
        if err := _validate_slug(c):
            out["errors"].append({"competition": c, "error": err})
            continue
        try:
            res = kaggle_core.poll_once(c, data_dir(), _child_env())
            out["checked"].append(c)
            for r in res["new_results"]:
                out["new_results"].append({"competition": c, **r})
            if res.get("initialized"):
                out.setdefault("initialized", []).append(c)
        except Exception as e:
            out["errors"].append({"competition": c, "error": str(e)[:120]})
    return json.dumps(out)


def kaggle_leaderboard(args: dict, **kwargs) -> str:
    """Fetch the public leaderboard top-N for a competition."""
    comp = (args.get("competition") or "").strip()
    if err := _validate_slug(comp):
        return json.dumps({"error": err})
    top = _validate_top(args.get("top") or 10)
    try:
        r = subprocess.run(
            [kaggle_core.KAGGLE_BIN, "competitions", "leaderboard", "-c", comp,
             "--show", "--top", str(top)],
            capture_output=True, text=True, timeout=90, env=_child_env())
        return json.dumps({"competition": comp, "top": top,
                           "leaderboard": (r.stdout or r.stderr)[:3000]})
    except Exception as e:
        return json.dumps({"error": str(e)[:200]})


def register_ctx(ctx) -> None:
    """Called from __init__.register(): capture ctx via partial-bound handlers."""
    set_ctx(ctx)
