# HACKATHON SUBMISSION — COPY-PASTE PACK
# Everything below is ready to use the moment the demo video is recorded.

## 1. CATALOG PR — file to add: plugin-catalog/kaggle-competitions.yaml

```yaml
id: kaggle-competitions
name: Kaggle Competitions
description: >-
  Track Kaggle competitions from your agent: live submission status, score
  history, personal-best watch, leaderboards, and a public live board on your
  own domain. Multi-competition — track any number of slugs.
category: Tools
tier: community
repo: https://github.com/landenjackson/hermes-kaggle-plugin
subdir: kaggle-competitions
commit: acc343bc9d85cbb5ee72aca675ce51e444b1bccd
version: 0.1.0
author: landenjackson
license: MIT
tags: [kaggle, competitions, tracking, desktop, board]
screenshots:
  - assets/mobile-board.jpg
```

(Re-pin `commit:` to the final HEAD after the last commit — I'll do that.)

## 2. PR DESCRIPTION (paste into the PR body on NousResearch/hermes-agent)

**What it does:** kaggle-competitions gives the agent four tools over the live
Kaggle API (submissions, score history, watch-for-new-results, leaderboard),
a desktop pane, and — the part I use daily — a public live board served from
your own domain (landenjackson.com/kaggle for mine), auto-refreshed by an
external 30-minute poller so the server never touches tokens or the CLI.

**Surfaces used:** agent tools (ctx.register_tool), desktop pane (plugin-sdk
ctx.register area panes), full page + sidebar nav (ROUTES_AREA +
SIDEBAR_NAV_AREA), dashboard API (dashboard/plugin_api.py, FastAPI router).

**Disclosures (rule 13):** reads KAGGLE_API_TOKEN from the environment or
~/.hermes/kaggle/.env; the token is never logged or echoed. State is stored
locally in the plugin data directory. No telemetry, no third-party services.

**Validation:** `hermes plugins validate` passes all checks (security scan:
safe). Demo video linked in the form. Built and dogfooded during the 2026
Gemma 4 / quantum competition season — the board is live with real data.

## 3. HACKATHON FORM ANSWERS (draft)

**Plugin name/link:** kaggle-competitions
**PR link:** (the PR URL once opened)
**Demo video:** (the X post URL once posted)

## 4. X POST CAPTION (for the demo video)

```
Built a Hermes plugin that tracks my Kaggle competitions — live board on my
own domain, the agent reports new scores before I check the site.

$20K hackathon entry. 7 days. Built in public, running on the agent itself.

github.com/landenjackson/hermes-kaggle-plugin
landenjackson.com/kaggle

#buildinpublic #AI #agents
```

## 5. DEMO SHOT LIST
See DEMO_RECORDING_CARD.md in the repo — 7 shots, spoken lines, editing notes.

## 6. FINAL SEQUENCE (after recording)
1. Post video on X, tag @NousResearch
2. Open PR on NousResearch/hermes-agent with plugin-catalog/kaggle-competitions.yaml
   (pin the final commit SHA)
3. Submit the form with both links
4. Done — catalog CI runs when a maintainer picks it up
