# RECORDING DAY — STEP BY STEP

Follow this top to bottom. Total time: ~45 min setup + recording.

---

## PHASE 1 — SETUP (15 min)

### 1. Open the three windows
- **Window A (browser):** `landenjackson.com/kaggle` — the board, scrolled to the top
- **Window B (terminal):** any terminal, clean prompt
- **Window C (Telegram):** chat with your bot (@BigLandoBot), empty-ish so the reply is visible

### 2. Test the install command works
In the terminal, run:
```
hermes plugins list | grep kaggle
```
Confirm `kaggle-competitions` shows enabled. (You won't record this — you'll
record a simulated install instead, see Shot 2 note.)

### 3. Mic + screen record check
- Win+G (Game Bar) or CapCut → start a 5-second test recording of the board
- Play it back: can you read the green "23.90679"? Is your voice clear?
- Fix either before recording anything real

### 4. Read the spoken lines ONCE out loud
They're in DEMO_RECORDING_CARD.md. Don't memorize — just make them familiar.
Speak casually. Flubbed words are fixed by cuts.

---

## PHASE 2 — RECORD (30 min)

### Shot 1 — Hook (10 sec) [Window A: the board]
- Start recording, hold on the board 2 seconds, then speak:
- "I compete on Kaggle. Every submission, every score, every miss — tracked.
  So I built a plugin that does the tracking for me. For my agent."
- Stop recording.

### Shot 2 — Install (10 sec) [Window B: terminal]
- NOTE: the plugin is already installed on your machine. So for the demo:
  run `hermes plugins uninstall kaggle-competitions` then
  `hermes plugins install landenjackson/hermes-kaggle-plugin`
  while recording. That's the REAL install flow, from scratch.
- (After recording: re-enable it — `hermes plugins enable kaggle-competitions`)
- Say: "One command installs it. It reads your Kaggle token from the
  environment — never logs it, never shows it."
- Stop recording.

### Shot 3 — The ask (18 sec) [Window C: Telegram]
- Start recording on the Telegram window.
- Send: "any new scores?"
- Let the agent work — don't narrate the wait. When the reply lands, read it
  aloud if it's short, or just say:
- "Now I just ask. It polls every competition I track and only reports
  what changed."
- Stop recording.

### Shot 4 — History (17 sec) [Window C: Telegram]
- Send: "how has my score moved this week?"
- When it replies:
- "The whole log — best score, regressions, the timeouts I'd rather forget.
  Misses included. That's the brand."
- Stop recording.

### Shot 5 — Close (15 sec) [Window A: the board again]
- Hold on the board, then:
- "And the board lives on my own site — landenjackson.com/kaggle —
  auto-refreshed every thirty minutes. Built in public, running on the
  agent platform itself. Link's below."
- Stop recording.

---

## PHASE 3 — EDIT (20 min, CapCut)

1. Import all clips in order. Trim each to the timing on the card.
2. Add captions at shot starts:
   - 0:10 `hermes plugins install landenjackson/hermes-kaggle-plugin`
   - 0:20 `kaggle_watch — polls all tracked competitions`
   - 0:38 `kaggle_score_history — the whole log`
3. End card (last 5 sec, static):
   ```
   github.com/landenjackson/hermes-kaggle-plugin
   landenjackson.com/kaggle
   ```
4. Export 1080p.

---

## PHASE 4 — PUBLISH (10 min)

1. Post on X: attach video + this caption:

   Built a Hermes plugin that tracks my Kaggle competitions — live board on
   my own domain, the agent reports new scores before I check the site.

   $20K hackathon entry. 7 days. Built in public, running on the agent itself.

   github.com/landenjackson/hermes-kaggle-plugin
   landenjackson.com/kaggle

   #buildinpublic #AI #agents

2. Tag @NousResearch in the post (reply or in the caption)
3. Send me the X post link → I open the catalog PR with the yaml + description
4. Submit the form: video link + PR link
5. Done.

---

## FAILURE MODES (don't panic)
- Agent slow in Shot 3/4 → the wait is fine, cut in editing
- Terminal font too small → Ctrl+Plus before recording
- Flubbed a line → stop, redo THAT shot only
- Board didn't load → it auto-refreshes; wait 10 sec and keep rolling
