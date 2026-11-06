# kaggle-competitions

A Hermes Agent plugin that turns your agent into a Kaggle competition assistant:
**live submission tracking, score history, personal-best watch, leaderboards, and a
desktop pane** — for any number of competitions at once.

> Not a guru. Just ships. — built by an active Kaggle competitor, for active Kaggle competitors.

![desktop pane placeholder — screenshots below](assets/pane.png)

## Why

Every competitor knows the loop: submit on Kaggle, refresh the submissions page
every ten minutes, scroll the leaderboard, lose the history of what you actually
tried. This plugin puts all of it inside your agent:

- **Ask, don't check** — "any new scores?" or "how did my score move this week?" in plain language
- **Watch pending submissions** — the agent polls and tells you the moment a
  `PENDING` run completes with a score
- **Keep the whole log** — every submission with date, score, and description,
  stored locally (your experiment history becomes queryable)
- **See it live** — a desktop pane showing best score + recent runs for every
  tracked competition, refreshing automatically

## Install

```bash
hermes plugins install landenjackson/hermes-kaggle-plugin
hermes plugins enable kaggle-competitions
```

Requirements:
- Hermes Agent ≥ 0.23.0
- A Kaggle account with API access — `KAGGLE_API_TOKEN` in your environment, or in
  `~/.hermes/kaggle/.env` / any path you point the plugin at. **The token is never
  logged or echoed by this plugin.**
- The `kaggle` CLI on PATH (`pip install kaggle`) — or the plugin will find it in
  `~/.local/bin`

## Configure

Add the competitions you want to track in **Settings → Plugins → Kaggle
Competitions** (or via config):

```yaml
plugins:
  entries:
    kaggle-competitions:
      settings:
        competitions:
          - titanic
          - google-verifiable-quantum-circuit-compilation
        poll_minutes: 30
```

You can also skip configuration and just ask the agent about a specific
competition — it will start tracking whatever you mention.

## The agent tools

| Tool | What it does |
|---|---|
| `kaggle_list_submissions` | Recent submissions + best score for one or all tracked competitions |
| `kaggle_score_history` | Full chronological history — dates, scores, descriptions |
| `kaggle_watch` | Poll now; report only **new** completed scores since the last check |
| `kaggle_leaderboard` | Public leaderboard top-N ("where do I stand?") |

Example session:

```
you:  any new scores?
hermes: v15 on the quantum comp just completed — 23.90712. That's a new PB (+0.0003).

you:  how has my score moved this week?
hermes: 14 submissions since Monday. Best 23.90679 (v14). Two timeouts,
        one regression to 23.87 from the C40 change. Full log in the pane.
```

## Desktop pane

The plugin ships a desktop surface: one pane, every tracked competition, best
score prominent, the five most recent runs under each. Updates every 2 minutes.
Requires the Desktop app (or the Webapp) — it talks to the plugin's dashboard API
endpoint, which is protected by your dashboard's own auth.

## Scheduled watching (optional)

Pair `kaggle_watch` with a Hermes scheduled job to get pushed notifications when
a score lands:

```
hermes cronjob create --name kaggle-watch --schedule "*/30 * * * *" \
  --prompt "Run the kaggle_watch tool and tell me about any new results."
```

## Privacy & security

- Your API token is read from the environment or a local `.env` file — **never
  logged, echoed, or included in tool output**
- Submission data is stored locally in the plugin's data directory
- No third-party services; everything talks to kaggle.com directly

## Compatibility

- Hermes Agent ≥ 0.23.0 (v0.22.x works with minor tool-registration warnings)
- Python 3.10+
- No pandas/numpy — stdlib + `requests` only

## License

MIT — see [LICENSE](LICENSE).

## Author

Built by [Landen Jackson](https://landenjackson.com) — researcher, agent operator,
and active Kaggle competitor. The tool I needed, so I shipped it.
