"""Refresh the long-lived Instagram token (valid 60 days) and print the new one."""
import os, json, urllib.request
url = ("https://graph.instagram.com/refresh_access_token?grant_type=ig_refresh_token&access_token="
       + os.environ["IG_ACCESS_TOKEN"])
with urllib.request.urlopen(url, timeout=30) as r:
    print(json.load(r)["access_token"])
