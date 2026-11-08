# RECORDING DAY — THE STORY VERSION

**What you're making:** a <90s video that shows judges three things —
1. **The problem is real:** you compete on Kaggle, scores trickle in, checking them manually sucks.
2. **The plugin solves it:** one install, and your AGENT watches the scoreboard for you.
3. **It's real and it ships:** live board on your own site, public repo.

The video is a story, not a feature list. Each shot = one beat of the story.
If a shot doesn't move the story, cut it.

---

## PHASE 1 — SETUP (15 min)

### 1. Why these three windows
- **Browser → `landenjackson.com/kaggle`** — the PROOF. A public board anyone can visit.
- **Terminal** — the MECHANISM. Where installation happens (what judges will do).
- **Telegram (@BigLandoBot)** — the EXPERIENCE. This is what "having an agent" feels like.

Arrange: browser left, terminal right-top, Telegram right-bottom (or full-screen
each shot — cleaner for mobile viewers).

### 2. Make text readable (judges watch on phones)
- Terminal: `Ctrl` + `+` twice. Big font, dark background.
- Browser: `Ctrl` + `+` once. The green 23.90679 must be legible on a phone screen.
- Record at 1920×1080 if Game Bar asks.

### 3. Mic check (60 seconds)
- Win + G → capture → record 5 seconds saying "testing, one two".
- Play back. If your voice sounds distant, move the mic or speak up.
- Phone viewers forgive imperfect video. They do NOT forgive inaudible audio.

### 4. Read the story once
The lines below are the script. Read them out loud ONCE. Don't memorize —
make them yours. Stumble? Cut it in the edit. Clipchamp trims everything.

---

## PHASE 2 — THE STORY (5 shots, ~30 min)

### Shot 1 — THE HOOK (10 sec) · [Browser: the board]
**Why this shot:** judges need the problem in one glance. The board IS the
problem — 15 rows of submissions you'd otherwise check by hand.

Start recording. Hold on the board for 2 seconds of silence (let them read it),
then:

> "I compete on Kaggle. Every submission, every score, every miss — tracked
> by hand. So I built something that tracks them for me. For my agent."

Stop.

### Shot 2 — THE INSTALL (15 sec) · [Terminal]
**Why this shot:** judges install plugins. Show them it's one command, from
scratch, with nothing pre-staged. This is the trust shot.

Run it LIVE (the plugin's already on your machine, so uninstall first —
that's the honest from-scratch flow):

```
hermes plugins uninstall kaggle-competitions
hermes plugins install landenjackson/hermes-kaggle-plugin
```

> "One command. It reads your Kaggle credentials from the standard spot —
> ~/.kaggle/kaggle.json — never logs them, never shows them. And that's it.
> Installed."

(After recording: `hermes plugins enable kaggle-competitions` to switch it
back on.)

**Note for you, not the camera:** on a fresh install, the first poll builds a
baseline — the agent correctly reports nothing "new". That's honest behavior
and it's covered in Shot 3's line.

### Shot 3 — THE ASK (20 sec) · [Telegram]
**Why this shot:** this is the whole product. You don't open Kaggle. You don't
check a dashboard. You just ASK — like asking a person.

Start recording on the Telegram window. Send:

> any new scores?

Let it work. Don't narrate the wait — silence is fine, or just watch the
screen like you would. When the reply lands:

> "Now I just ask. It watches every competition I track — and only tells me
> what changed. On a fresh install that's nothing yet — it's building its
> baseline. The moment one of my runs completes, it tells me that one."

Stop.

### Shot 4 — THE HISTORY (20 sec) · [Telegram]
**Why this shot:** the depth. A scoreboard tells you today's number. This
tells you the TREND — including the failures, which is the brand.

Send:

> how has my score moved this week?

When it replies:

> "The whole log. Best score, regressions, the runs that timed out —
> misses included. That's the brand. Raw builds, real numbers."

Stop.

### Shot 5 — THE CLOSE (15 sec) · [Browser: the board, then slow scroll]
**Why this shot:** land the plane on something judges can visit themselves.
The board proves it runs outside the demo — on your own infrastructure,
in public.

Hold on the board, then slowly scroll down it as you say:

> "And the board lives on my own site — landenjackson.com/kaggle —
> auto-refreshed every thirty minutes. Built in public, running on the
> agent platform itself. Links below."

Stop.

---

## PHASE 3 — EDIT (20 min, Clipchamp)

Clipchamp is built into Windows (search "Clipchamp" in Start). It's simpler
than CapCut for this job — trim, caption, export. That's all we need.

1. **New video → Import** all 5 clips. Drag them onto the timeline in order
   (1→5). The timeline IS the story.
2. **Trim:** click each clip → drag the edges. Cut dead air at the starts
   and the flubs. Target: hook 10s, install 15s, ask 20s, history 20s,
   close 15s = **80 seconds total** (under the 90s limit).
3. **Captions** (Text → "Plain text", 3 of them, at these moments):
   - During install: `hermes plugins install landenjackson/hermes-kaggle-plugin`
   - During the ask: `kaggle_watch — polls every tracked competition`
   - During history: `kaggle_score_history — the whole submission log`
   Style: white, medium size, bottom third. Don't decorate.
4. **End card** (Text, last 5 seconds, two lines):
   ```
   github.com/landenjackson/hermes-kaggle-plugin
   landenjackson.com/kaggle
   ```
5. **Export → 1080p.** Save somewhere easy (Desktop is fine).

---

## PHASE 4 — PUBLISH (10 min)

1. Post on X with the video attached:

   > Built a Hermes plugin that tracks my Kaggle competitions — live board
   > on my own domain, the agent reports new scores before I check the site.
   >
   > $20K hackathon entry. 7 days. Built in public, running on the agent itself.
   >
   > github.com/landenjackson/hermes-kaggle-plugin
   > landenjackson.com/kaggle
   >
   > #buildinpublic #AI #agents

2. Tag @NousResearch in the post.
3. Send me the X link → I open the catalog PR (pre-written, 10 min).
4. Submit the form: video link + PR link.
5. Done. Three days before deadline.

---

## IF SOMETHING GOES WRONG
- **Agent slow in Shot 3/4** → the wait is normal (a Kaggle API roundtrip).
  Keep rolling; trim it in Clipchamp.
- **Flubbed a line** → stop, redo ONLY that shot. Clips are independent.
- **Board looks stale** → it auto-refreshes every 30 min; wait 10 sec, keep rolling.
- **Terminal text tiny on playback** → re-record that shot after Ctrl+Plus.
- **Clipchamp confusing?** → the only tools you need are: import, drag to
  timeline, trim edges, add text, export. Nothing else. Ignore the rest.
