"""Upload today's Short to YouTube and schedule it for the time in meta.json (default 19:30 IST).

Secrets (GitHub Actions -> Settings -> Secrets and variables -> Actions):
  YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN   (from scripts/get_youtube_token.py)
"""
import os, datetime as dt
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from common import load_post, mark_done, already_done, IST

SCOPES = ["https://www.googleapis.com/auth/youtube"]


def youtube():
    creds = Credentials(
        None,
        refresh_token=os.environ["YT_REFRESH_TOKEN"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.environ["YT_CLIENT_ID"],
        client_secret=os.environ["YT_CLIENT_SECRET"],
        scopes=SCOPES,
    )
    return build("youtube", "v3", credentials=creds, cache_discovery=False)


def main():
    meta = load_post()
    if already_done(meta, "youtube"):
        print("YouTube already done for this day.")
        return
    yt_meta = meta["youtube"]
    hh, mm = map(int, yt_meta.get("publish_time_ist", "19:30").split(":"))
    day = dt.date.fromisoformat(os.path.basename(meta["_dir"]))
    publish_at = dt.datetime(day.year, day.month, day.day, hh, mm, tzinfo=IST)
    now = dt.datetime.now(IST)

    status = {"selfDeclaredMadeForKids": False, "embeddable": True}
    if publish_at > now + dt.timedelta(minutes=15):
        # YouTube publishes it at publish_at
        status.update(privacyStatus="private", publishAt=publish_at.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    else:
        status.update(privacyStatus="public")

    body = {
        "snippet": {
            "title": yt_meta["title"][:100],
            "description": yt_meta.get("description", ""),
            "tags": yt_meta.get("tags", []),
            "categoryId": "27",  # Education
            "defaultLanguage": "ta",
            "defaultAudioLanguage": "ta",
        },
        "status": status,
    }
    yt = youtube()
    req = yt.videos().insert(part="snippet,status", body=body,
                             media_body=MediaFileUpload(meta["_video"], mimetype="video/mp4", chunksize=-1, resumable=True))
    resp = None
    while resp is None:
        _, resp = req.next_chunk()
    vid = resp["id"]
    print(f"Uploaded: https://youtube.com/shorts/{vid}  status={status}")

    playlist = yt_meta.get("playlist_id")
    if playlist:
        yt.playlistItems().insert(part="snippet", body={"snippet": {
            "playlistId": playlist, "resourceId": {"kind": "youtube#video", "videoId": vid}}}).execute()
        print("Added to playlist", playlist)

    mark_done(meta, "youtube", {"video_id": vid, "publish_at": status.get("publishAt", "now")})


if __name__ == "__main__":
    main()
