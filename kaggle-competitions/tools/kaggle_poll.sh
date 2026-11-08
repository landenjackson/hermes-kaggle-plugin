#!/usr/bin/env bash
# Kaggle competition poller — writes fresh submission rows into the
# kaggle-competitions plugin's state file (plugin_data_dir).
# Runs from system crontab, OUTSIDE the serve process, so the plugin's
# dashboard route never needs the Kaggle CLI or token itself.
# Install: crontab entry every 30 min. No LLM, no network exposure.
/home/jacks/.hermes/tools/python-3.14.9+202****1021-linux-arm64/bin/python3.14 - <<'PYEOF'
import json, os, re, subprocess, time
from pathlib import Path

HOME = Path.home()
STATE_DIR = HOME / ".hermes/plugin-data/kaggle-competitions"
STATE = STATE_DIR / "state.json"
TOKEN_FILE = HOME / "projects/quantum-comp/.env"
KAGGLE = HOME / ".local/bin/kaggle"
COMPETITIONS = ["google-verifiable-quantum-circuit-compilation"]

env = dict(os.environ)
if TOKEN_FILE.is_file():
    for line in TOKEN_FILE.read_text().splitlines():
        if line.startswith("KAGGLE_API_TOKEN="):
            env["KAGGLE_API_TOKEN"] = line.split("=", 1)[1].strip()

def run_kaggle(comp):
    r = subprocess.run([str(KAGGLE), "competitions", "submissions", "-c", comp],
                       capture_output=True, text=True, timeout=120, env=env)
    rows = []
    for line in (r.stdout or "").splitlines():
        cols = [c.strip() for c in re.split(r"  +", line.strip()) if c.strip()]
        if len(cols) < 5 or cols[0].lower() == "ref" or set(cols[0]) <= {"-"}:
            continue
        status = next((c.split(".")[-1] for c in cols if "SubmissionStatus." in c), "UNKNOWN")
        score = next((c for c in cols if re.fullmatch(r"-?\d+\.\d+", c)), "")
        desc = cols[3] if len(cols) > 4 else ""
        rows.append({"ref": cols[0], "date": cols[1] if len(cols) > 1 else "",
                     "status": status, "score": score, "desc": desc[:120]})
    return rows

def best(rows):
    scores = [float(r["score"]) for r in rows if r.get("score")]
    return max(scores) if scores else None

state = json.loads(STATE.read_text()) if STATE.is_file() else {"competitions": {}, "pushes": []}
now = time.time()
for comp in COMPETITIONS:
    try:
        rows = run_kaggle(comp)
    except Exception as e:
        print(f"{comp}: poll failed {e}")
        continue
    prev = {r["ref"]: r for r in state.get("competitions", {}).get(comp, {}).get("rows", [])}
    for r in rows:
        old = prev.get(r["ref"])
        if (old and old["status"] == "PENDING" and r["status"] == "COMPLETE" and r["score"]) or \
           (not old and r["status"] == "COMPLETE" and r["score"]):
            state.setdefault("pushes", []).append({"ts": now, "competition": comp,
                                                   "desc": r["desc"], "score": r["score"]})
    state.setdefault("competitions", {})[comp] = {
        "rows": rows, "last_poll": now, "best": best(rows)}
    print(f"{comp}: {len(rows)} rows, best {best(rows)}")

STATE_DIR.mkdir(parents=True, exist_ok=True)
STATE.write_text(json.dumps(state, indent=1))
print("state written")
PYEOF

# publish snapshot to the public site (landenjackson.com/kaggle)
cp /home/jacks/.hermes/plugin-data/kaggle-competitions/state.json /home/jacks/projects/landooutthere/site/kaggle_state.json 2>/dev/null
