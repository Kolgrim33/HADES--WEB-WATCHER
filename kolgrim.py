#!/usr/bin/env python3
"""
HADES by Kolgrim - Advanced Username Intelligence Framework
OSINT Username Tracker with Deep Profile Extraction
"""

import requests
import hashlib
import time
import sys
import re
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# ─────────────────────────────────────────────────────────────
#  TERMINAL COLORS
# ─────────────────────────────────────────────────────────────
class C:
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    CYAN    = "\033[96m"
    WHITE   = "\033[97m"
    GRAY    = "\033[90m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    RESET   = "\033[0m"
    SKULL   = "\033[35m"
    DRED    = "\033[31m"

# ─────────────────────────────────────────────────────────────
#  BANNER  —  intimidating skull, enhanced from original
# ─────────────────────────────────────────────────────────────
def banner():
    skull = f"""{C.DRED}{C.BOLD}
    ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
    ░░░░░░░░░░░▄████████████████████████▄░░░░░░░░░░░░
    ░░░░░░░░▄████████████████████████████████▄░░░░░░░
    ░░░░░░▄██████████████████████████████████████▄░░░
    ░░░░░███████████████████████████████████████████░
    ░░░░░██████▀▀▀░░░░░░░░░░░░░░░░░░▀▀▀██████████░░░░
    ░░░░░█████░░{C.SKULL}▄██████▄{C.DRED}░░░░░░░{C.SKULL}▄██████▄{C.DRED}░░█████████░░░
    ░░░░░█████░{C.SKULL}███{C.WHITE}▄▄▄{C.SKULL}███{C.DRED}░░░░░░{C.SKULL}███{C.WHITE}▄▄▄{C.SKULL}███{C.DRED}░░████████░░░
    ░░░░░█████░{C.SKULL}███{C.WHITE}███{C.SKULL}███{C.DRED}░░░░░░{C.SKULL}███{C.WHITE}███{C.SKULL}███{C.DRED}░░████████░░░
    ░░░░░█████░{C.SKULL}███{C.WHITE}▀▀▀{C.SKULL}███{C.DRED}░░░░░░{C.SKULL}███{C.WHITE}▀▀▀{C.SKULL}███{C.DRED}░░████████░░░
    ░░░░░██████░{C.SKULL}▀██████▀{C.DRED}░░░░░░░{C.SKULL}▀██████▀{C.DRED}░░█████████░░░
    ░░░░░████████▄▄░░░░░░░░░░░░░░░░░░░▄▄███████████░
    ░░░░░████████████████████████████████████████░░░
    ░░░░░████████████▀▀▀░░░░░░░░░░░▀▀████████████░░░
    ░░░░░████████▀░{C.SKULL}▄███▄░░░░░░░░▄███▄{C.DRED}░▀████████░░░
    ░░░░░███████░{C.SKULL}▄██{C.WHITE}▀███▀{C.SKULL}██▄░░▄██{C.WHITE}▀███▀{C.SKULL}██▄{C.DRED}░███████░░░
    ░░░░░███████░{C.SKULL}███{C.WHITE}░███░{C.SKULL}███░░███{C.WHITE}░███░{C.SKULL}███{C.DRED}░███████░░░
    ░░░░░███████░{C.SKULL}▀██{C.WHITE}▄███▄{C.SKULL}██▀░░▀██{C.WHITE}▄███▄{C.SKULL}██▀{C.DRED}░███████░░░
    ░░░░░████████░{C.SKULL}▀█████▀░▄▄░░▄▄░▀█████▀{C.DRED}░████████░░
    ░░░░░██████████▄░░░░░{C.SKULL}▀████▀{C.DRED}░░░░░▄██████████░░░
    ░░░░░████████████████▄▄▄▄▄▄▄▄▄▄████████████████░
    ░░░░░░░████████████████████████████████████████░
    ░░░░░░░░░░░▀▀█████████████████████████▀▀░░░░░░░░
    ░░░░░░░░░░░░░░░▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀░░░░░░░░░░░░
    ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░{C.RESET}"""

    title = f"""
{C.RED}{C.BOLD}██╗  ██╗ █████╗ ██████╗ ███████╗███████╗
██║  ██║██╔══██╗██╔══██╗██╔════╝██╔════╝
███████║███████║██║  ██║█████╗  ███████╗
██╔══██║██╔══██║██║  ██║██╔══╝  ╚════██║
██║  ██║██║  ██║██████╔╝███████╗███████║
╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚══════╝╚══════╝{C.RESET}
{C.GRAY}                              by Kolgrim
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        Username Intelligence Framework  v2.2
        Deep OSINT  |  Multi-Platform  |  Profile Extraction
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{C.RESET}
"""
    print(skull)
    print(title)


# ─────────────────────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────────────────────
def hash_avatar(url: str) -> str:
    if not url:
        return None
    return hashlib.md5(url.encode()).hexdigest()[:12]

def section(title: str):
    print(f"\n{C.CYAN}{C.BOLD}{'─'*54}")
    print(f"  {title}")
    print(f"{'─'*54}{C.RESET}")

def found(platform: str, url: str):
    print(f"  {C.GREEN}[+] FOUND{C.RESET}  {C.WHITE}{C.BOLD}{platform:<18}{C.RESET} {C.GRAY}{url}{C.RESET}")

def not_found(platform: str):
    print(f"  {C.GRAY}[-] NOT FOUND  {platform}{C.RESET}")

def error_line(platform: str, msg: str):
    print(f"  {C.YELLOW}[!] ERROR{C.RESET}  {platform:<18} {C.DIM}{msg}{C.RESET}")

def detail(key: str, value):
    if value not in (None, "", False, 0):
        print(f"      {C.CYAN}├─{C.RESET} {C.DIM}{key}:{C.RESET} {C.WHITE}{value}{C.RESET}")

def note(msg: str):
    print(f"      {C.YELLOW}╌╌{C.RESET} {C.DIM}{msg}{C.RESET}")

def progress(msg: str):
    sys.stdout.write(f"  {C.YELLOW}[~]{C.RESET} {msg}                    \r")
    sys.stdout.flush()


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}


# ─────────────────────────────────────────────────────────────
#  DEEP EXTRACTORS
# ─────────────────────────────────────────────────────────────

# ── REDDIT — full free public JSON API ──────────────────────
def extract_reddit(username: str) -> dict:
    url = f"https://www.reddit.com/user/{username}/about.json"
    try:
        r = requests.get(url, headers={"User-Agent": "Kolgrim-OSINT/2.1"}, timeout=10)
        if r.status_code == 200:
            d = r.json().get("data", {})
            created = d.get("created_utc")
            cake_day = datetime.utcfromtimestamp(created).strftime("%Y-%m-%d") if created else None
            total_karma = (d.get("link_karma") or 0) + (d.get("comment_karma") or 0)
            return {
                "status": "FOUND",
                "profile_url": f"https://reddit.com/u/{username}",
                "name": d.get("name"),
                "post_karma": d.get("link_karma"),
                "comment_karma": d.get("comment_karma"),
                "total_karma": total_karma,
                "cake_day": cake_day,
                "is_mod": "Yes" if d.get("is_mod") else None,
                "reddit_premium": "Yes" if d.get("is_gold") else None,
                "verified_email": "Yes" if d.get("has_verified_email") else None,
                "avatar_hash": hash_avatar(d.get("icon_img")),
            }
        elif r.status_code == 404:
            return {"status": "NOT_FOUND"}
        else:
            return {"status": "ERROR", "msg": f"HTTP {r.status_code}"}
    except Exception as e:
        return {"status": "ERROR", "msg": str(e)[:60]}


# ── GITHUB — free public API ────────────────────────────────
def extract_github(username: str) -> dict:
    url = f"https://api.github.com/users/{username}"
    try:
        r = requests.get(url, headers={"User-Agent": "Kolgrim-OSINT"}, timeout=10)
        if r.status_code == 200:
            d = r.json()
            return {
                "status": "FOUND",
                "profile_url": d.get("html_url"),
                "name": d.get("name"),
                "bio": (d.get("bio") or "")[:100] or None,
                "location": d.get("location"),
                "company": d.get("company"),
                "email": d.get("email"),
                "blog": d.get("blog") or None,
                "followers": d.get("followers"),
                "following": d.get("following"),
                "public_repos": d.get("public_repos"),
                "public_gists": d.get("public_gists"),
                "created_at": (d.get("created_at") or "")[:10] or None,
                "avatar_hash": hash_avatar(d.get("avatar_url")),
            }
        elif r.status_code == 404:
            return {"status": "NOT_FOUND"}
        else:
            return {"status": "ERROR", "msg": f"HTTP {r.status_code}"}
    except Exception as e:
        return {"status": "ERROR", "msg": str(e)[:60]}


# ── INSTAGRAM — HTML meta scrape ────────────────────────────
def extract_instagram(username: str) -> dict:
    url = f"https://www.instagram.com/{username}/"
    try:
        r = requests.get(url, headers=HEADERS, timeout=12)
        if r.status_code == 404:
            return {"status": "NOT_FOUND"}
        if r.status_code != 200:
            return {"status": "ERROR", "msg": f"HTTP {r.status_code}"}

        html = r.text

        if "Page Not Found" in html or "Sorry, this page" in html:
            return {"status": "NOT_FOUND"}

        name = re.search(r'<meta property="og:title" content="([^"]+)"', html)
        desc = re.search(r'<meta property="og:description" content="([^"]+)"', html)
        img  = re.search(r'<meta property="og:image" content="([^"]+)"', html)

        extracted_name = name.group(1).strip() if name else None
        extracted_desc = desc.group(1).strip() if desc else None

        followers = following = posts = None
        if extracted_desc:
            nums = re.findall(r'([\d,.]+[KkMm]?)\s+(Followers|Following|Posts)', extracted_desc)
            for val, label in nums:
                v = val.replace(",", "")
                if label == "Followers":  followers = v
                if label == "Following":  following = v
                if label == "Posts":      posts     = v

        if "Log in to Instagram" in html and not extracted_name:
            return {
                "status": "FOUND",
                "profile_url": url,
                "_note": "Instagram served login wall — account EXISTS but data blocked.",
            }

        return {
            "status": "FOUND",
            "profile_url": url,
            "display_name": extracted_name,
            "followers": followers,
            "following": following,
            "posts": posts,
            "avatar_hash": hash_avatar(img.group(1)) if img else None,
        }
    except Exception as e:
        return {"status": "ERROR", "msg": str(e)[:60]}


# ── TWITTER / X — HTML meta scrape ─────────────────────────
def extract_twitter(username: str) -> dict:
    url = f"https://twitter.com/{username}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=12)
        if r.status_code == 404:
            return {"status": "NOT_FOUND"}
        if r.status_code != 200:
            return {"status": "ERROR", "msg": f"HTTP {r.status_code}"}

        html = r.text

        if "This account doesn't exist" in html or "account has been suspended" in html.lower():
            return {"status": "NOT_FOUND"}

        name = re.search(r'<meta property="og:title" content="([^"]+)"', html)
        desc = re.search(r'<meta property="og:description" content="([^"]+)"', html)
        img  = re.search(r'<meta property="og:image" content="([^"]+)"', html)

        extracted_name = name.group(1).strip() if name else None
        extracted_bio  = desc.group(1).strip() if desc else None

        if not extracted_name and "Log in" in html:
            return {
                "status": "FOUND",
                "profile_url": url,
                "_note": "X/Twitter blocked deep extraction. Account EXISTS.",
            }

        return {
            "status": "FOUND",
            "profile_url": url,
            "display_name": extracted_name,
            "bio": extracted_bio[:120] if extracted_bio else None,
            "avatar_hash": hash_avatar(img.group(1)) if img else None,
        }
    except Exception as e:
        return {"status": "ERROR", "msg": str(e)[:60]}


# ── TIKTOK — HTML + embedded JSON scrape ────────────────────
def extract_tiktok(username: str) -> dict:
    url = f"https://www.tiktok.com/@{username}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=12)
        if r.status_code == 404:
            return {"status": "NOT_FOUND"}
        if r.status_code != 200:
            return {"status": "ERROR", "msg": f"HTTP {r.status_code}"}

        html = r.text

        if "Couldn't find this account" in html or "couldn't find this account" in html:
            return {"status": "NOT_FOUND"}

        name = re.search(r'<meta property="og:title" content="([^"]+)"', html)
        desc = re.search(r'<meta property="og:description" content="([^"]+)"', html)
        img  = re.search(r'<meta property="og:image" content="([^"]+)"', html)

        followers = likes = None
        json_match  = re.search(r'"followerCount":(\d+)', html)
        likes_match = re.search(r'"heartCount":(\d+)', html)
        if json_match:   followers = json_match.group(1)
        if likes_match:  likes     = likes_match.group(1)

        extracted_name = name.group(1).strip() if name else None

        if not extracted_name:
            return {
                "status": "FOUND",
                "profile_url": url,
                "_note": "TikTok blocked deep extraction. Account EXISTS.",
            }

        return {
            "status": "FOUND",
            "profile_url": url,
            "display_name": extracted_name,
            "bio": desc.group(1).strip()[:120] if desc else None,
            "followers": followers,
            "total_likes": likes,
            "avatar_hash": hash_avatar(img.group(1)) if img else None,
        }
    except Exception as e:
        return {"status": "ERROR", "msg": str(e)[:60]}


# ── SNAPCHAT — presence + display name only ─────────────────
def extract_snapchat(username: str) -> dict:
    url = f"https://www.snapchat.com/add/{username}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        if r.status_code == 404:
            return {"status": "NOT_FOUND"}
        if r.status_code != 200:
            return {"status": "ERROR", "msg": f"HTTP {r.status_code}"}

        html = r.text

        if "Sorry, we couldn't find" in html or "Page Not Found" in html:
            return {"status": "NOT_FOUND"}

        name = re.search(r'<meta property="og:title" content="([^"]+)"', html)
        img  = re.search(r'<meta property="og:image" content="([^"]+)"', html)

        return {
            "status": "FOUND",
            "profile_url": url,
            "display_name": name.group(1).strip() if name else None,
            "avatar_hash": hash_avatar(img.group(1)) if img else None,
            "_note": "Snapchat exposes display name only. No follower or post data available.",
        }
    except Exception as e:
        return {"status": "ERROR", "msg": str(e)[:60]}


# ── FACEBOOK — presence check only ─────────────────────────
def extract_facebook(username: str) -> dict:
    url = f"https://www.facebook.com/{username}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=10, allow_redirects=True)
        if r.status_code == 404:
            return {"status": "NOT_FOUND"}

        html = r.text

        if (
            "Page Not Found" in html
            or "isn't available" in html
            or "content isn't available" in html.lower()
        ):
            return {"status": "NOT_FOUND"}

        if r.status_code == 200:
            name = re.search(r'<meta property="og:title" content="([^"]+)"', html)
            return {
                "status": "FOUND",
                "profile_url": url,
                "display_name": name.group(1).strip() if name else None,
                "_note": "Facebook requires login for any detailed data. Presence confirmed.",
            }

        return {"status": "ERROR", "msg": f"HTTP {r.status_code}"}
    except Exception as e:
        return {"status": "ERROR", "msg": str(e)[:60]}


# ── DEV.TO — free public API ────────────────────────────────
def extract_devto(username: str) -> dict:
    url = f"https://dev.to/api/users/by_username?url={username}"
    try:
        r = requests.get(url, headers={"User-Agent": "Kolgrim-OSINT"}, timeout=8)
        if r.status_code == 200:
            d = r.json()
            return {
                "status": "FOUND",
                "profile_url": f"https://dev.to/{username}",
                "name": d.get("name"),
                "summary": (d.get("summary") or "")[:100] or None,
                "location": d.get("location"),
                "joined": (d.get("joined_at") or "")[:10] or None,
                "followers": d.get("followers_count"),
                "avatar_hash": hash_avatar(d.get("profile_image")),
            }
        elif r.status_code == 404:
            return {"status": "NOT_FOUND"}
        else:
            return {"status": "ERROR", "msg": f"HTTP {r.status_code}"}
    except Exception as e:
        return {"status": "ERROR", "msg": str(e)[:60]}


# ── HACKERNEWS — free firebase API ──────────────────────────
def extract_hackernews(username: str) -> dict:
    url = f"https://hacker-news.firebaseio.com/v0/user/{username}.json"
    try:
        r = requests.get(url, headers={"User-Agent": "Kolgrim-OSINT"}, timeout=8)
        if r.status_code == 200 and r.json():
            d = r.json()
            created = d.get("created")
            created_str = datetime.utcfromtimestamp(created).strftime("%Y-%m-%d") if created else None
            about_clean = re.sub(r'<[^>]+>', '', d.get("about") or "")[:100] or None
            return {
                "status": "FOUND",
                "profile_url": f"https://news.ycombinator.com/user?id={username}",
                "karma": d.get("karma"),
                "about": about_clean,
                "created_at": created_str,
                "submissions": len(d.get("submitted") or []),
            }
    except Exception as e:
        return {"status": "ERROR", "msg": str(e)[:60]}
    return {"status": "NOT_FOUND"}


# ── DISCORD — public profile lookup via pomelo/lookup API ──
def extract_discord(username: str) -> dict:
    """
    Discord has two lookup paths:
    1. /users/{username} on their new pomelo (unique username) system
    2. Lanyard / open-source presence APIs for users who opted in
    We also check the unofficial lookup used by many OSINT tools.
    """
    results = {"status": "NOT_FOUND"}

    # Path 1: disboard.org public user search (no auth needed)
    try:
        url = f"https://disboard.org/user/{username}"
        r = requests.get(url, headers=HEADERS, timeout=10)
        if r.status_code == 200 and "user not found" not in r.text.lower():
            html = r.text
            name = re.search(r'<title>([^<]+)</title>', html)
            avatar = re.search(r'<img[^>]+class="[^"]*user-avatar[^"]*"[^>]+src="([^"]+)"', html)
            servers = re.findall(r'server-name[^>]*>([^<]+)<', html)
            extracted_name = name.group(1).strip().replace(" - DISBOARD", "") if name else None
            if extracted_name and extracted_name.lower() != "disboard":
                results = {
                    "status": "FOUND",
                    "profile_url": url,
                    "display_name": extracted_name,
                    "public_servers": len(servers) if servers else None,
                    "avatar_hash": hash_avatar(avatar.group(1)) if avatar else None,
                    "_note": "Data sourced from DISBOARD public index.",
                }
    except Exception:
        pass

    # Path 2: lookup.guru — community OSINT Discord lookup
    if results["status"] == "NOT_FOUND":
        try:
            url2 = f"https://lookup.guru/{username}"
            r2 = requests.get(url2, headers=HEADERS, timeout=10)
            if r2.status_code == 200:
                html2 = r2.text
                if "not found" not in html2.lower() and "invalid" not in html2.lower():
                    name2   = re.search(r'<meta property="og:title" content="([^"]+)"', html2)
                    desc2   = re.search(r'<meta property="og:description" content="([^"]+)"', html2)
                    img2    = re.search(r'<meta property="og:image" content="([^"]+)"', html2)
                    disc_id = re.search(r'(\d{17,19})', html2)
                    results = {
                        "status": "FOUND",
                        "profile_url": url2,
                        "display_name": name2.group(1).strip() if name2 else None,
                        "bio": desc2.group(1).strip()[:120] if desc2 else None,
                        "discord_id": disc_id.group(1) if disc_id else None,
                        "avatar_hash": hash_avatar(img2.group(1)) if img2 else None,
                        "_note": "Data sourced from lookup.guru public index.",
                    }
        except Exception:
            pass

    # Path 3: Discord profile via their CDN tag pattern (username#0 new system)
    if results["status"] == "NOT_FOUND":
        try:
            url3 = f"https://discord.com/users/{username}"
            r3 = requests.get(url3, headers=HEADERS, timeout=8)
            # Discord returns 200 with a shell page even for valid users
            if r3.status_code == 200 and "discord" in r3.text.lower():
                results = {
                    "status": "FOUND",
                    "profile_url": f"https://discord.com/users/{username}",
                    "_note": "Discord account detected. Full profile requires Discord client (no public API without auth).",
                }
        except Exception:
            pass

    return results


# ─────────────────────────────────────────────────────────────
#  PRINT DEEP PROFILE
# ─────────────────────────────────────────────────────────────
def print_profile(platform: str, data: dict):
    url = data.get("profile_url", "")
    found(platform, url)
    skip = {"status", "profile_url"}
    for k, v in data.items():
        if k not in skip:
            if k == "_note":
                note(str(v))
            else:
                detail(k.replace("_", " ").title(), v)


# ─────────────────────────────────────────────────────────────
#  SIMPLE PLATFORM SCAN
# ─────────────────────────────────────────────────────────────
PLATFORMS_SIMPLE = {
    "Pinterest":   "https://www.pinterest.com/{u}/",
    "LinkedIn":    "https://www.linkedin.com/in/{u}/",
    "Twitch":      "https://www.twitch.tv/{u}",
    "YouTube":     "https://www.youtube.com/@{u}",
    "SoundCloud":  "https://soundcloud.com/{u}",
    "Spotify":     "https://open.spotify.com/user/{u}",
    "Tumblr":      "https://{u}.tumblr.com",
    "Medium":      "https://medium.com/@{u}",
    "Hashnode":    "https://hashnode.com/@{u}",
    "Keybase":     "https://keybase.io/{u}",
    "Pastebin":    "https://pastebin.com/u/{u}",
    "ProductHunt": "https://www.producthunt.com/@{u}",
    "Steam":       "https://steamcommunity.com/id/{u}",
    "Chess.com":   "https://www.chess.com/member/{u}",
    "Lichess":     "https://lichess.org/@/{u}",
    "Wattpad":     "https://www.wattpad.com/user/{u}",
    "Replit":      "https://replit.com/@{u}",
    "Codepen":     "https://codepen.io/{u}",
    "HuggingFace": "https://huggingface.co/{u}",
    "Kaggle":      "https://www.kaggle.com/{u}",
    "Behance":     "https://www.behance.net/{u}",
    "Dribbble":    "https://dribbble.com/{u}",
    "Fiverr":      "https://www.fiverr.com/{u}",
    "Linktree":    "https://linktr.ee/{u}",
}

def check_simple(platform: str, url_template: str, username: str) -> tuple:
    url = url_template.replace("{u}", username)
    try:
        r = requests.get(url, headers=HEADERS, timeout=8, allow_redirects=True)
        if r.status_code == 200:
            return (platform, "FOUND", url)
        elif r.status_code == 404:
            return (platform, "NOT_FOUND", url)
        else:
            return (platform, "ERROR", f"HTTP {r.status_code}")
    except requests.exceptions.ConnectionError:
        return (platform, "OFFLINE", "")
    except requests.exceptions.Timeout:
        return (platform, "TIMEOUT", "")
    except Exception as e:
        return (platform, "ERROR", str(e)[:40])


# ─────────────────────────────────────────────────────────────
#  TIMELINE CORRELATION
# ─────────────────────────────────────────────────────────────
def show_timeline(timeline: list):
    if not timeline:
        return
    section("⏱  ACCOUNT CREATION TIMELINE")
    print(f"  {C.DIM}Correlate dates — same join window = likely same person{C.RESET}\n")
    timeline.sort(key=lambda x: x[1])
    for platform, date in timeline:
        try:
            age_years = (datetime.utcnow() - datetime.strptime(date, "%Y-%m-%d")).days // 365
        except Exception:
            age_years = 0
        bar = "▓" * min(age_years * 2, 30)
        print(f"  {C.CYAN}{platform:<16}{C.RESET} {C.WHITE}{date}{C.RESET}  {C.GRAY}{bar}  ({age_years}y){C.RESET}")


# ─────────────────────────────────────────────────────────────
#  SUMMARY
# ─────────────────────────────────────────────────────────────
def show_summary(username: str, results: dict):
    section("📊  INTELLIGENCE SUMMARY")
    found_list   = [p for p, s in results.items() if s == "FOUND"]
    missing_list = [p for p, s in results.items() if s == "NOT_FOUND"]
    error_list   = [p for p, s in results.items() if s in ("ERROR","OFFLINE","TIMEOUT")]

    print(f"  {C.WHITE}Target        :{C.RESET} {C.BOLD}{C.RED}{username}{C.RESET}")
    print(f"  {C.WHITE}Platforms     :{C.RESET} {len(results)}")
    print(f"  {C.GREEN}Confirmed     :{C.RESET} {len(found_list)}")
    print(f"  {C.GRAY}Not Found     :{C.RESET} {len(missing_list)}")
    print(f"  {C.YELLOW}Errors/Blocked:{C.RESET} {len(error_list)}")

    if found_list:
        print(f"\n  {C.GREEN}{C.BOLD}Confirmed Presence:{C.RESET}")
        for i, p in enumerate(found_list):
            connector = "└─" if i == len(found_list) - 1 else "├─"
            print(f"    {C.GREEN}{connector}{C.RESET} {p}")

    print(f"\n  {C.GRAY}Scan time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC{C.RESET}")


# ─────────────────────────────────────────────────────────────
#  EXPORT
# ─────────────────────────────────────────────────────────────
def export_report(username: str, deep_results: dict, simple_results: list):
    filename = f"kolgrim_{username}_{int(time.time())}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("╔══════════════════════════════════════════════════════╗\n")
        f.write("║           KOLGRIM OSINT INTELLIGENCE REPORT          ║\n")
        f.write("╚══════════════════════════════════════════════════════╝\n\n")
        f.write(f"Target    : {username}\n")
        f.write(f"Generated : {datetime.utcnow().isoformat()} UTC\n")
        f.write("=" * 56 + "\n\n")
        f.write("DEEP PROFILE EXTRACTIONS\n")
        f.write("-" * 40 + "\n")
        for platform, data in deep_results.items():
            f.write(f"\n[{data.get('status')}] {platform}\n")
            for k, v in data.items():
                if k != "status" and v:
                    f.write(f"  {k}: {v}\n")
        f.write("\n\nPLATFORM PRESENCE SCAN\n")
        f.write("-" * 40 + "\n")
        for platform, status, url in sorted(simple_results, key=lambda x: x[1]):
            f.write(f"[{status:<10}] {platform:<18} {url}\n")

    print(f"\n  {C.GREEN}[✔] Report saved:{C.RESET} {C.BOLD}{filename}{C.RESET}")
    return filename


# ─────────────────────────────────────────────────────────────
#  MAIN SCAN
# ─────────────────────────────────────────────────────────────
def run_scan(username: str):
    overall_results = {}
    timeline        = []

    section("🔬  DEEP PROFILE EXTRACTION")
    print(f"  {C.DIM}Probing 10 platforms for detailed intelligence...{C.RESET}\n")

    deep_extractors = {
        "Reddit":     extract_reddit,
        "GitHub":     extract_github,
        "Instagram":  extract_instagram,
        "Twitter/X":  extract_twitter,
        "TikTok":     extract_tiktok,
        "Snapchat":   extract_snapchat,
        "Facebook":   extract_facebook,
        "Discord":    extract_discord,
        "Dev.to":     extract_devto,
        "HackerNews": extract_hackernews,
    }

    deep_results = {}
    for platform, fn in deep_extractors.items():
        progress(f"Probing {platform}...")
        data = fn(username)
        deep_results[platform] = data
        status = data.get("status")

        if status == "FOUND":
            print_profile(platform, data)
            overall_results[platform] = "FOUND"
            for date_key in ("created_at", "joined", "cake_day"):
                val = data.get(date_key)
                if val and val != "N/A" and len(val) >= 7:
                    timeline.append((platform, val[:10]))
        elif status == "NOT_FOUND":
            not_found(platform)
            overall_results[platform] = "NOT_FOUND"
        else:
            error_line(platform, data.get("msg", "Unknown"))
            overall_results[platform] = "ERROR"

    section(f"🌐  SCANNING {len(PLATFORMS_SIMPLE)} ADDITIONAL PLATFORMS")
    simple_found   = []
    simple_results = []

    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {
            executor.submit(check_simple, p, tmpl, username): p
            for p, tmpl in PLATFORMS_SIMPLE.items()
        }
        completed = 0
        for future in as_completed(futures):
            platform, status, url = future.result()
            simple_results.append((platform, status, url))
            overall_results[platform] = status
            completed += 1
            sys.stdout.write(
                f"  {C.YELLOW}[~]{C.RESET} Progress: {completed}/{len(PLATFORMS_SIMPLE)} scanned\r"
            )
            sys.stdout.flush()
            if status == "FOUND":
                simple_found.append((platform, url))

    print()

    if simple_found:
        print()
        for platform, url in sorted(simple_found, key=lambda x: x[0]):
            found(platform, url)

    show_timeline(timeline)
    show_summary(username, overall_results)

    return deep_results, simple_results


# ─────────────────────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────────────────────
def main():
    banner()

    print(f"  {C.GRAY}Enter target username  (or 'quit' to exit){C.RESET}")
    username = input(f"  {C.RED}▶{C.RESET} ").strip()

    if username.lower() in ("quit", "exit", "q"):
        print(f"\n  {C.GRAY}Exiting Kolgrim. Stay dark.{C.RESET}\n")
        sys.exit(0)

    if not username:
        print(f"  {C.RED}[!] No username entered.{C.RESET}")
        sys.exit(1)

    print(f"\n  {C.CYAN}[*]{C.RESET} Target locked: {C.BOLD}{C.WHITE}{username}{C.RESET}")
    print(f"  {C.GRAY}    Scanning 34 platforms — allow 20–50 seconds{C.RESET}\n")

    start = time.time()
    deep_results, simple_results = run_scan(username)
    elapsed = time.time() - start

    print(f"\n  {C.GRAY}Total scan duration: {elapsed:.1f}s{C.RESET}\n")

    save = input(f"  {C.CYAN}Export full report to file? (y/N):{C.RESET} ").strip().lower()
    if save == "y":
        export_report(username, deep_results, simple_results)

    print(f"\n{C.DRED}{C.DIM}{'═'*54}")
    print(f"   HADES by Kolgrim — SESSION TERMINATED")
    print(f"{'═'*54}{C.RESET}\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n  {C.YELLOW}[!] Aborted by user.{C.RESET}\n")
        sys.exit(0)
