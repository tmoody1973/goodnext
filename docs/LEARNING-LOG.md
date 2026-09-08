# Learning log

Dated entries. Each answers: what did we expect, what happened, what do we now
believe. Claude drafts; Tarik edits in his own voice.

## 2026-09-08: the first browser run of the website

**Expected.** The Next.js dev server would pass a request to the API and wait
for the plan, since the API already worked from the command line.

**Happened.** The browser reported "could not reach the service" after two and
a half minutes, and the API never logged the request. The dev server's built-in
proxy (the piece that forwards `/api/*` to the API during development) gives up
after 30 seconds by default, and a plan takes 60 to 105 seconds. Raising its
timeout to three minutes fixed it; the next run returned a real plan in 99
seconds. Two smaller lessons from the same hour: the automated browser's click
missed a button that sat half below the bottom edge of the window, and a
password-manager extension injected an icon into the ZIP field before React
attached, producing a warning that looked like an app bug and was not.

**Now believe.** Every hop between the browser and the agent needs to be told
how long a plan takes: the dev proxy today, the edge routing rule at hosting
time. The 30-second delayed status is not just a courtesy; it is also the
point at which infrastructure defaults start cutting the cord. Verify with the
real path, not the shortcut, or the shortcut hides exactly this.
