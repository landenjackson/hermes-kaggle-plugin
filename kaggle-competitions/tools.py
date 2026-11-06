"""Tool handlers — the code that runs when the agent calls each tool."""
from __future__ import annotations

import json
import os

from . import kaggle_core


def _data_dir(ctx):
    try:
        return ctx.plugin_data_dir()
    except Exception:
        from pathlib import Path
        return Path.home() / ".hermes" / "plugin-data" / "kaggle-competitions"


def _kaggle_env(ctx) -> dict | None:
    """Find KAGGLE_API_TOKEN without ever logging its value."""
    env = dict(os.environ)
    if env.get("KAGGLE_API_TOKEN"):
        return env
    for cand in ("~/.hermes/kaggle/.env", "~/projects/quantum-comp/.env"):
        p = os.path.expanduser(cand)
        if os.path.isfile(p):
            try:
                for line in open(p):
                    if line.startswith("KAGGLE_API_TOKEN="):
                        env["KAGGLE_API_TOKEN"] = line.split("=", 1)[1].strip()
                        return env
            except OSError:
                pass
    return env


def _tracked(ctx) -> list[str]:
    try:
        cfg = ctx.get_config() or {}
        comps = cfg.get("competitions") or []
        if comps:
            return [str(c) for c in comps]
    except Exception:
        pass
    # fallback: whatever is already in state
    state = kaggle_core.load_state(_data_dir(ctx))
    return list(state.get("competitions", {}).keys())


def kaggle_list_submissions(args: dict, ctx=None, **kwargs) -> str:
    """List submissions for a competition (or all tracked ones)."""
    comp = (args.get("competition") or "").strip()
    comps = [comp] if comp else _tracked(ctx)
    if not comps:
        return json.dumps({"error": "No competition given and none tracked. "
                                    "Set plugins.entries.kaggle-competitions.settings.competitions "
                                    "to a list of slugs, or pass competition=<slug>."})
    out = {}
    for c in comps:
        try:
            res = kaggle_core.poll_once(c, _data_dir(ctx), _kaggle_env(ctx))
            rows = res["rows"]
            out[c] = {
                "best": kaggle_core.best_score(rows),
                "count": len(rows),
                "recent": rows[:10],
            }
        except Exception as e:
            out[c] = {"error": str(e)[:200]}
    return json.dumps(out)


def kaggle_score_history(args: dict, ctx=None, **kwargs) -> str:
    """Full score history for one competition, oldest first."""
    comp = (args.get("competition") or "").strip()
    if not comp:
        tracked = _tracked(ctx)
        if not tracked:
            return json.dumps({"error": "No competition given and none tracked."})
        comp = tracked[0]
    try:
        res = kaggle_core.poll_once(comp, _data_dir(ctx), _kaggle_env(ctx))
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


def kaggle_watch(args: dict, ctx=None, **kwargs) -> str:
    """Poll all tracked competitions now; report any NEW completed scores since last check."""
    out = {"new_results": [], "checked": []}
    for c in _tracked(ctx):
        try:
            res = kaggle_core.poll_once(c, _data_dir(ctx), _kaggle_env(ctx))
            out["checked"].append(c)
            for r in res["new_results"]:
                out["new_results"].append({"competition": c, **r})
        except Exception as e:
            out["checked"].append(f"{c}: error {str(e)[:120]}")
    return json.dumps(out)


def kaggle_leaderboard(args: dict, ctx=None, **kwargs) -> str:
    """Fetch the public leaderboard top-N for a competition."""
    comp = (args.get("competition") or "").strip()
    if not comp:
        return json.dumps({"error": "competition=<slug> required"})
    top = int(args.get("top") or 10)
    try:
        r = __import__("subprocess").run(
            [kaggle_core.KAGGLE_BIN, "competitions", "leaderboard", "-c", comp, "--show", "--top", str(top)],
            capture_output=True, text=True, timeout=90, env=_kaggle_env(ctx))
        return json.dumps({"competition": comp, "leaderboard": (r.stdout or r.stderr)[:3000]})
    except Exception as e:
        return json.dumps({"error": str(e)[:200]})
