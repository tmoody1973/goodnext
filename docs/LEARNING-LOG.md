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

## 2026-09-13: hosting day, three things the local run never showed

**Expected.** The API that had run fine on the laptop for a week would run
the same inside a container, and the first public visit would just work.

**Happened.** Three surprises, all caught by checks rather than by luck.
First, the container crashed on start: the help-routes loader walked three
folders up from its own file at import time, which works in the repo and
fails when the package sits two levels below root. A local smoke test of the
image caught it before deploy; a reviewer agent found it independently. Second,
the first visit from a Chromium browser hung: modern browsers try https before
http, and a load balancer with no listener on 443 drops the packet, so the
browser waits out its whole timeout before falling back. A security-group rule
did nothing; a plain-HTTP listener on 443 that answers with a fixed 400 makes
the TLS attempt fail in 0.12 seconds and the fallback is instant. Third, both
on-screen browsers on the Mac stopped producing screenshots at the same time
(one hung on capture, the other reported a zero-size viewport), while the pages
themselves rendered and the text came back fine.

**Now believe.** Run the image locally before the first deploy, every time; the
container is a different filesystem, not just a different machine. A public
address is only proven by a real browser's first visit, because browsers add
behavior (https-first) that curl never shows. And keep text evidence separate
from screenshots: when the capture tool fails, the text proof still stands and
the deadline does not move.
