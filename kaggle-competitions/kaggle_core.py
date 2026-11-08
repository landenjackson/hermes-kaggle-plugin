"""kaggle-competitions — core data layer.

Reads Kaggle submissions through the kaggle CLI when available, falling back to
the public leaderboard API shape. All state lives in the plugin data dir
(plugin_data_dir) so it survives updates.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import time
from pathlib import Path

KAGGLE_BIN = shutil.which("kaggle") or str(Path.home() / ".local/bin/kaggle")


def _run_kaggle(competition: str, env: dict | None = None, timeout: int = 90) -> list[dict]:
    """Pull the submission list for one competition. Returns [{ref, date, status, score, desc}]."""
    cmd = [KAGGLE_BIN, "competitions", "submissions", "-c", competition]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, env=env)
    rows = []
    for line in (r.stdout or "").splitlines():
        cols = [c.strip() for c in re.split(r"  +", line.strip()) if c.strip()]
        if len(cols) < 5 or cols[0].lower() == "ref" or set(cols[0]) <= {"-"}:
            continue
        status = next((c.split(".")[-1] for c in cols if "SubmissionStatus." in c), "UNKNOWN")
        score = next((c for c in cols if re.fullmatch(r"-?\d+\.\d+", c)), "")
        desc = cols[4] if len(cols) > 4 else ""
        rows.append({"ref": cols[0], "date": cols[1] if len(cols) > 1 else "",
                     "status": status, "score": score, "desc": desc[:120]})
    return rows


def load_state(data_dir: Path) -> dict:
    f = data_dir / "state.json"
    if f.is_file():
        try:
            return json.loads(f.read_text())
        except Exception:
            pass
    return {"competitions": {}, "pushes": []}


def save_state(data_dir: Path, state: dict) -> None:
    """Atomic write: temp file + os.replace so concurrent pane/cron polls never corrupt state."""
    import tempfile
    data_dir.mkdir(parents=True, exist_ok=True)
    tmp = data_dir / "state.json.tmp"
    tmp.write_text(json.dumps(state, indent=1))
    os.replace(tmp, data_dir / "state.json")


def poll_once(competition: str, data_dir: Path, env: dict | None = None) -> dict:
    """Poll one competition; returns {rows, new_results: [...]} where new_results are
    submissions that flipped PENDING -> COMPLETE since the last poll."""
    state = load_state(data_dir)
    rows = _run_kaggle(competition, env)
    prev = state.setdefault("competitions", {}).setdefault(competition, {}).get("rows", [])
    prev_by_ref = {r["ref"]: r for r in prev}
    new_results = []
    initialized = bool(prev)  # first poll after install: history is baseline, not news
    for r in rows:
        old = prev_by_ref.get(r["ref"])
        if old and old["status"] == "PENDING" and r["status"] == "COMPLETE" and r["score"]:
            new_results.append(r)  # a submission WE were waiting on just completed
        # first-seen COMPLETE rows are baseline on a fresh install — not news
    state["competitions"][competition] = {"rows": rows, "last_poll": time.time()}
    save_state(data_dir, state)
    return {"rows": rows, "new_results": new_results, "initialized": initialized}


def best_score(rows: list[dict]) -> float | None:
    scores = [float(r["score"]) for r in rows if r.get("score")]
    return max(scores) if scores else None
