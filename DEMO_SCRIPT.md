# Kaggle Competitions Plugin — 90-Second Demo Script

Total runtime target: 80–90 seconds. Record at 1920×1080 or your phone screen if
showing mobile. Keep every cut under 6 seconds. Speak casually — this is a build
log, not a keynote.

---

## SHOT LIST

### Shot 1 — The hook (0:00–0:10)
**Screen:** landenjackson.com loaded in browser.
**Say:**
> "I compete on Kaggle. Every submission, every score, every miss — I track all of it.
> So I built the thing I needed: a Hermes plugin that tracks competitions for me."

### Shot 2 — The install (0:10–0:20)
**Screen:** terminal.
**Action:** type `hermes plugins install landenjackson/hermes-kaggle-plugin`, hit enter,
show the install output briefly.
**Say:**
> "One command installs it. It reads your Kaggle API token from your environment —
> it never logs it, never echoes it."

### Shot 3 — The ask (0:20–0:38)
**Screen:** chat with the agent (Telegram or desktop).
**Action:** type "any new scores?" → agent runs `kaggle_watch` → reply shows results.
**Say:**
> "Now I just ask. 'Any new scores?' — it polls every competition I track and only
> reports what changed since the last check."

### Shot 4 — The history (0:38–0:55)
**Screen:** same chat.
**Action:** type "how has my score moved this week?" → agent runs `kaggle_score_history`.
**Say:**
> "Ask for the trend and it gives me the whole log — best score, regressions,
> the timeouts I'd rather forget. The full log is the brand. Misses included."

### Shot 5 — The leaderboard (0:55–1:05)
**Screen:** same chat.
**Action:** type "where do I stand on [competition]?" → `kaggle_leaderboard` output.
**Say:**
> "And it pulls the public leaderboard, so I know exactly where I stand."

### Shot 6 — The desktop pane (1:05–1:20)
**Screen:** Hermes Desktop or Webapp with the pane visible, refreshing.
**Say:**
> "It also ships a desktop pane — every tracked competition, best score, recent runs,
> live. No tab refreshing. Ever."

### Shot 7 — The close (1:20–1:30)
**Screen:** the pane one more time, or the GitHub repo.
**Say:**
> "It's open source, it's in the catalog, and it just ships.
> Link's below."

---

## CAPTIONS TO ADD IN EDITING
- 0:10 → `hermes plugins install landenjackson/hermes-kaggle-plugin`
- 0:20 → `kaggle_watch — polls all tracked competitions`
- 0:38 → `kaggle_score_history — the whole log`
- 1:05 → `desktop pane · live · 2-min refresh`

## PRE-RECORD CHECKLIST
- [ ] Gateway restarted (you) → plugin enabled → tools live
- [ ] Track at least 2 competitions so the pane looks multi-competition
- [ ] One PENDING submission running on Kaggle BEFORE recording shot 3,
      so "any new scores?" catches a real result mid-demo (the money shot)
- [ ] Desktop pane visible in Hermes Desktop or Webapp
- [ ] Mic level checked; record in one take per shot, cut between shots

## THE MONEY SHOT
If the quantum rebuild finishes and v15 verifies before recording:
run the demo with the quantum competition as the star — the agent reports the
score that beat the shipped benchmark's own default config, live on camera.
That's the clip that gets reposted.
