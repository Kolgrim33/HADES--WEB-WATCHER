# ☠ HADES by Kolgrim
### Username Intelligence Framework — Linux Setup Guide

> Searches the web for a username across 34 platforms and extracts deep profile intelligence from Reddit, GitHub, Instagram, Twitter/X, TikTok, Snapchat, Facebook, Discord, Dev.to, and HackerNews.

---

## Requirements

- Linux (any distro — tested on Ubuntu/Debian/Kali)
- Python 3.6 or higher
- pip3
- Internet connection

---

## Step 1 — Check Python is installed

Open a terminal and run:

```bash
python3 --version
```

You should see something like `Python 3.10.12`. If you get `command not found`, install it:

```bash
sudo apt update && sudo apt install python3 python3-pip -y
```

---

## Step 2 — Download the script

If you cloned from GitHub:

```bash
git clone https://github.com/Kolgrim/HADES-WEB-WATCHER.git
cd HADES-WEB-WATCHER
```

Or if you just have the file, move it to a folder:

```bash
mkdir ~/hades
mv kolgrim.py ~/hades/
cd ~/hades
```

---

## Step 3 — Install the dependency

HADES only needs one external library — `requests`. Install it with:

```bash
pip3 install requests
```

If you get a permissions error, use:

```bash
pip3 install requests --user
```

Or if your system requires it (newer Ubuntu/Kali):

```bash
pip3 install requests --break-system-packages
```

---

## Step 4 — Run HADES

```bash
python3 kolgrim.py
```

You will see the skull banner load, then it will prompt:

```
  Enter target username  (or 'quit' to exit)
  ▶ 
```

Type any username and press Enter. HADES will scan 34 platforms automatically.

---

## Step 5 — (Optional) Make it executable globally

So you can run it from anywhere as a command:

```bash
chmod +x kolgrim.py
sudo mv kolgrim.py /usr/local/bin/hades
```

Now you can launch it from anywhere just by typing:

```bash
hades
```

---

## What HADES scans

| Mode | Platforms | What it extracts |
|---|---|---|
| Deep Extract | Reddit | Karma, cake day, mod status, verified email |
| Deep Extract | GitHub | Bio, location, repos, followers, join date |
| Deep Extract | Instagram | Display name, followers, following, post count |
| Deep Extract | Twitter/X | Display name, bio |
| Deep Extract | TikTok | Display name, followers, total likes |
| Deep Extract | Snapchat | Display name |
| Deep Extract | Facebook | Display name (presence confirm) |
| Deep Extract | Discord | Display name, servers, Discord ID |
| Deep Extract | Dev.to | Name, location, followers, join date |
| Deep Extract | HackerNews | Karma, about, join date, submission count |
| Presence Scan | 24 others | Pinterest, LinkedIn, Twitch, YouTube, Steam, Chess.com, Kaggle, Replit, Codepen, Medium, Tumblr, SoundCloud, Spotify, Pastebin, Wattpad, HuggingFace, Dribbble, Behance, Fiverr, Linktree, Hashnode, Keybase, ProductHunt, Lichess |

---

## Saving a report

After every scan, HADES will ask:

```
  Export full report to file? (y/N):
```

Press `y` and Enter. It saves a `.txt` file in your current directory named:

```
kolgrim_<username>_<timestamp>.txt
```

---

## Notes

- Some platforms (Instagram, Twitter/X, Facebook, TikTok) may return a login wall depending on your IP and their rate limiting. HADES will still confirm the account exists and note that detailed data was blocked.
- Discord extraction relies on public third-party indexes (DISBOARD, lookup.guru) since Discord has no unauthenticated public API.
- A full scan takes roughly 20–50 seconds depending on your internet speed.
- To exit at the username prompt, type `quit` and press Enter, or press `Ctrl+C` at any time.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: No module named 'requests'` | Run `pip3 install requests` |
| Colors not showing in terminal | Make sure you're using a proper terminal emulator (gnome-terminal, xterm, kitty, alacritty) — not a basic TTY |
| All platforms returning OFFLINE | Check your internet connection |
| Instagram/Twitter always blocked | Normal behaviour — these platforms aggressively block scrapers. Presence is still confirmed. |
| `Permission denied` when running | Run `chmod +x kolgrim.py` first |

---

*HADES by Kolgrim — for educational and lawful OSINT use only.*
