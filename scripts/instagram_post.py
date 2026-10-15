"""Post today's video as an Instagram Reel (Instagram API with Instagram Login).

Secrets: IG_USER_ID, IG_ACCESS_TOKEN (long-lived token, refreshed automatically by the workflow)
The video must be reachable at a public URL; the workflow uses the raw GitHub URL of the file
(the repository must be public) unless meta.json gives "video_url".
"""
import os, time, json, urllib.request, urllib.parse
from common import load_post, mark_done, already_done

API = "https://graph.instagram.com/v21.0"


def call(method, path, **params):
    params["access_token"] = os.environ["IG_ACCESS_TOKEN"]
    data = urllib.parse.urlencode(params).encode()
    if method == "GET":
        req = urllib.request.Request(f"{API}/{path}?{data.decode()}")
    else:
        req = urllib.request.Request(f"{API}/{path}", data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        raise SystemExit(f"Instagram API error {e.code}: {e.read().decode()}")


def main():
    meta = load_post()
    if already_done(meta, "instagram"):
        print("Instagram already done for this day.")
        return
    ig = meta["instagram"]
    user = os.environ["IG_USER_ID"]
    video_url = ig.get("video_url") or meta.get("video_url")
    if not video_url:
        repo = os.environ["GITHUB_REPOSITORY"]
        branch = os.environ.get("GITHUB_REF_NAME", "main")
        rel = os.path.relpath(meta["_video"], os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        video_url = f"https://raw.githubusercontent.com/{repo}/{branch}/{urllib.parse.quote(rel)}"
    print("Video URL:", video_url)

    c = call("POST", f"{user}/media", media_type="REELS", video_url=video_url,
             caption=ig["caption"], share_to_feed="true")
    cid = c["id"]
    for _ in range(60):  # up to ~10 minutes of processing
        st = call("GET", cid, fields="status_code,status")
        print("container:", st)
        if st.get("status_code") == "FINISHED":
            break
        if st.get("status_code") == "ERROR":
            raise SystemExit(f"Instagram could not process the video: {st}")
        time.sleep(10)
    else:
        raise SystemExit("Timed out waiting for Instagram to process the video.")
    pub = call("POST", f"{user}/media_publish", creation_id=cid)
    info = call("GET", pub["id"], fields="permalink")
    print("Published:", info.get("permalink"))
    mark_done(meta, "instagram", {"media_id": pub["id"], "permalink": info.get("permalink")})


if __name__ == "__main__":
    main()
