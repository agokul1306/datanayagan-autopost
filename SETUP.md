# Datanayagan Autopost – one-time setup (about 1 hour)

After this, every video placed in `posts/YYYY-MM-DD/` (a `video.mp4` + `meta.json`) is
**scheduled on YouTube for 7:30 PM** (uploaded at 9:00 AM) and **posted to Instagram at 7:45 PM**, automatically, free.

---
## Part A – GitHub (10 min)
1. Create a free account at github.com (skip if you have one).
2. New repository → name `datanayagan-autopost` → **Public** (Instagram needs a public link to the video) → Create.
3. Upload every file from this folder (keep the folders: `scripts/`, `.github/workflows/`, `posts/`).
   Tip: on the repo page, "Add file → Upload files", drag the whole folder in.
4. Repo → **Settings → Actions → General → Workflow permissions → Read and write** → Save.

## Part B – YouTube API (25 min)
1. Go to console.cloud.google.com, sign in with the **Gmail that owns @datanayagan**.
2. Create project `datanayagan-autopost`.
3. **APIs & Services → Library →** search "YouTube Data API v3" → **Enable**.
4. **OAuth consent screen →** External → app name "Datanayagan Autopost", your email → Save.
   - Add scope `.../auth/youtube`.
   - **Publishing status → "Publish app" (In production).** Important: in "Testing" mode the login expires every 7 days.
5. **Credentials → Create credentials → OAuth client ID → Desktop app** → Download JSON (`client_secret.json`).
6. On your laptop (Python installed):
   ```
   pip install google-auth-oauthlib
   python scripts/get_youtube_token.py client_secret.json
   ```
   Browser opens → choose the @datanayagan account → you'll see "Google hasn't verified this app" → Advanced → Continue (it's your own app) → Allow.
   It prints three values.
7. GitHub repo → **Settings → Secrets and variables → Actions → New repository secret**, add:
   `YT_CLIENT_ID`, `YT_CLIENT_SECRET`, `YT_REFRESH_TOKEN`.

> **YouTube rule for new API projects:** videos uploaded by an *unaudited* project are kept **Private**.
> Apply (free) via the "YouTube API Services – Audit and Quota Extension Form" (search that name).
> Describe it as: "Personal tool to schedule my own channel's educational Shorts." Approval can take a few weeks.
> Until approved, keep scheduling YouTube in YouTube Studio; Instagram works fully right away.

## Part C – Instagram API (20 min)
Your Instagram must be a **Professional (Creator) account**.
1. developers.facebook.com → My Apps → **Create app** → use case **"Manage messaging & content on Instagram"** → name "Datanayagan Autopost".
2. In the app: **Instagram → API setup with Instagram login → Generate access tokens → Add account** → log in as @datanayagan → allow.
   (If asked, accept the tester invite in Instagram: Settings → Website permissions / Apps and websites → Tester invites.)
3. Copy the **access token** and the **Instagram user ID** shown there.
4. Add GitHub secrets: `IG_ACCESS_TOKEN`, `IG_USER_ID`.
5. Optional (keeps the token alive past 60 days automatically): GitHub → Settings → Developer settings →
   Fine-grained token for this repo with **Secrets: Read and write** → add it as secret `GH_PAT`.

## Part D – Test (5 min)
1. Repo → **Actions → "Post today's Instagram Reel" → Run workflow** → date `2026-10-16` (after Ep 3's `video.mp4` is in that folder).
2. Check the log; it prints the Reel link. Then do the same for "Schedule today's YouTube Short".
3. `done.json` appears in the post folder so nothing is ever posted twice.

---
## Every week after setup
Claude gives you, for each day, a folder `posts/YYYY-MM-DD/` with `video.mp4` + `meta.json`.
Upload those folders to the repo (Add file → Upload files). That's it.

Times: YouTube upload 9:00 AM (scheduled live at 7:30 PM), Instagram 7:45 PM. GitHub can start scheduled jobs a few minutes late.
