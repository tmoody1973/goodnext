# 211 API portal: do-it-yourself verification guide

For Tarik. About 30 to 45 minutes. No coding. You will click through the
211 developer portal, run two test searches, and save what comes back.

**Why this matters:** everything we have written about 211 so far came from
the public pages. The real field names, whether Milwaukee is in the data,
and the reuse rules are only visible once you're logged in. Your answers
decide whether GoodNext can use live 211 data or stays on the synthetic list.

**Ground rules:** never paste your API key into chat, a doc, or a commit.
Keep it in `agentcore/.env.local` (that file is ignored by git). Trial keys
are for development and testing only.

---

## Step 1: Sign in and confirm the trial subscription (5 min)

1. Go to https://apiportal.211.org and click **Sign in** (top right).
2. After signing in, click **Products** in the top menu.
3. Open **Trial - V2**. If it still says "You don't have subscriptions yet,"
   type a name like `goodnext-trial`, tick **I agree to the Terms of Use**,
   and click **Subscribe**. If it already shows a subscription, skip this.
4. Before you tick the box, click **Show** next to Terms of Use. Read for
   these words: *redistribute*, *display*, *cache*, *store*, *attribution*,
   *non-commercial*. Copy the paragraph(s) that contain them into a text file
   called `211-terms-excerpt.txt` on your Desktop.

**Write down:** the subscription name, and whether the terms mention
non-commercial use or attribution.

## Step 2: Find your key (2 min)

1. Click your name or **Profile** (top right).
2. Under **Subscriptions** find `goodnext-trial`. Click **Show** next to
   *Primary key*. That long string is your API key.
3. Open `agentcore/.env.local` in the repo (create it if missing) and add one
   line:
   ```
   NDP_211_API_KEY=paste-the-key-here
   ```
   Save. Do not put it anywhere else.

## Step 3: Read the Search V2 documentation (5 min)

1. Click **APIs** in the top menu, then **Search V2**.
2. You'll see a list of operations on the left (they look like
   `GET /search/...`). Click the one that searches by keyword and location.
3. Note the **exact parameter names**. We are looking for ones that mean:
   - the search words (something like `keyword` or `q`)
   - the ZIP or location (`location`, `zip`, `postalCode`)
   - a distance or radius (`distance`, `radius`, `miles`)
   - page size and page (`size`, `skip`, `page`)
   - a filter for active records (`includeInactive`)

**Write down:** the operation name and those parameter names exactly as
spelled. If there is no distance/radius parameter, write "none."

## Step 4: Run the Milwaukee search (10 min)

1. On that same operation page, click **Try it** (right side).
2. Fill in: keyword `food pantry`, location `53206`, and if there is a
   distance field, `10`. Leave the rest at defaults.
3. Under **Authorization** or **Subscription key**, choose your
   `goodnext-trial` key from the dropdown (the portal fills it in).
4. Click **Send**.
5. Look at the **Response** box at the bottom.

**What the result tells us:**

| You see | What it means | What to do |
| --- | --- | --- |
| Status 200 and a list of Milwaukee services | Milwaukee is in the trial data | Continue to Step 5 |
| Status 200 but an empty list or only non-Wisconsin results | Trial data does not cover Milwaukee | Stop after Step 6; tell me "no Milwaukee" |
| Status 401 or 403 | Key not attached or product not active | Re-check Step 2 and 3 |
| Status 429 | Rate limit (10 per minute) | Wait a minute, try once |

6. If you got results: click **Copy** on the response (or select all and
   copy), paste into a file on your Desktop called `211-search-53206.json`.

**Write down:** how many results came back, and whether you can see fields
that look like hours, service area, eligibility, cost, languages, or
"last updated." Just the field names as spelled.

## Step 5: Fetch one record with Query V2 (5 min)

1. In the search response, find an **id** on the first result. There may be
   several ids (service id, location id, service-at-location id). Copy the
   one that looks like a service-at-location id, or any id if unsure.
2. Click **APIs** → **Query V2**. Pick the operation that returns one
   service-at-location (or one service) by id.
3. **Try it**, paste the id, pick your key, **Send**.
4. Copy the response to `211-query-record.json` on your Desktop.

**Write down:** whether the detailed record has hours as structured fields
(open/close times per day) or as free text, and whether it has a service
area, eligibility text, cost, languages, and a last-updated date.

## Step 6: Note the non-trial product (3 min)

1. Click **Products** again.
2. List every product besides Trial. For each: its name, what it says about
   who can use it, and whether it says "request access" or "subscribe."
3. **Do not request or subscribe** to anything else yet.

**Write down:** the product names and what each requires.

## Step 7: Hand it back (2 min)

Put these in a folder and tell me where, or drag them into the chat:

- `211-terms-excerpt.txt`
- `211-search-53206.json`
- `211-query-record.json` (if Step 5 worked)
- your notes from the "Write down" lines above

I will strip anything sensitive, save the sanitized samples under
`docs/research/211-samples/`, update the 211 integration plan with the real
field names, and tell you whether the live adapter can be specced.

## If you get stuck

- "Try it" button missing: you're not signed in, or the product isn't
  subscribed. Go back to Step 1.
- Response is HTML instead of JSON: the wrong operation was chosen. Pick one
  whose path starts with `/search` or `/query`.
- Nothing makes sense: stop, screenshot the page, send it to me. Nothing
  here can break anything.
