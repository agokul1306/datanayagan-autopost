"""Run ONCE on your own computer to get the YouTube refresh token.

  pip install google-auth-oauthlib
  python scripts/get_youtube_token.py path/to/client_secret.json

A browser opens; sign in with the Google account that owns @datanayagan and allow access.
Copy the three printed values into GitHub secrets.
"""
import sys, json
from google_auth_oauthlib.flow import InstalledAppFlow

flow = InstalledAppFlow.from_client_secrets_file(sys.argv[1], ["https://www.googleapis.com/auth/youtube"])
creds = flow.run_local_server(port=0, prompt="consent", access_type="offline")
cfg = json.load(open(sys.argv[1]))
cfg = cfg.get("installed") or cfg.get("web")
print("\nYT_CLIENT_ID     =", cfg["client_id"])
print("YT_CLIENT_SECRET =", cfg["client_secret"])
print("YT_REFRESH_TOKEN =", creds.refresh_token)
