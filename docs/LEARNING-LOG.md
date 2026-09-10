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

## 2026-09-08: a bot opened the finish-pass PR before the session started

**Expected.** MOO-786 would be open in Linear and the finish pass would start
from a clean main, as the handoff said.

**Happened.** A PostHog Desktop "self-driving" agent had opened PR #12 at
20:06 CDT against an older main, claiming the MOO-786 work, and a Linear
automation had flipped the issue to Done at 21:46 CDT with no evidence comment
and no merge. The PR carried three usable ideas (a print block, provider names
in link labels, a vendor never-list) and two we would not take (the count line
turned into a second heading; the print rule left the week strip on paper).
The session rebuilt the work on a branch off the current main, borrowed the
good ideas by hand, moved the issue back to In Progress, and left PR #12 for
Tarik to close.

**Now believe.** A tracker status set by automation is a claim, not evidence;
check for the closing comment before trusting Done. Any tool with write access
to the repo or the tracker needs to be on the handoff's list of who does what,
or its output will collide with the human-run loop. Reading before building
caught this in minutes; building first would have produced a second PR for the
same ticket.
