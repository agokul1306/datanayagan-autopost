"""Shared helpers: find today's post folder (IST) and read its metadata."""
import json, os, sys, datetime as dt

IST = dt.timezone(dt.timedelta(hours=5, minutes=30))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def today_ist():
    return dt.datetime.now(IST).date()


def post_dir(day=None):
    """posts/YYYY-MM-DD for the given day (default: today in India)."""
    day = day or os.environ.get("POST_DATE") or today_ist().isoformat()
    return os.path.join(ROOT, "posts", str(day))


def load_post(day=None):
    d = post_dir(day)
    meta_path = os.path.join(d, "meta.json")
    if not os.path.exists(meta_path):
        print(f"No post scheduled for {os.path.basename(d)} - nothing to do.")
        sys.exit(0)
    with open(meta_path, encoding="utf-8") as f:
        meta = json.load(f)
    meta["_dir"] = d
    meta["_video"] = os.path.join(d, meta.get("video", "video.mp4"))
    return meta


def mark_done(meta, key, value):
    """Record what was posted so a re-run never posts twice."""
    path = os.path.join(meta["_dir"], "done.json")
    done = {}
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            done = json.load(f)
    done[key] = value
    with open(path, "w", encoding="utf-8") as f:
        json.dump(done, f, indent=2)


def already_done(meta, key):
    path = os.path.join(meta["_dir"], "done.json")
    if not os.path.exists(path):
        return False
    with open(path, encoding="utf-8") as f:
        return key in json.load(f)
