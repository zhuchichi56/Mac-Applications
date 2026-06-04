# ☕ WakeKeeper

A lightweight macOS menu bar app to prevent your Mac from sleeping —  
inspired by [Amphetamine](https://apps.apple.com/app/amphetamine/id937984704), built with Python + [rumps](https://github.com/jaredks/rumps).

![macOS](https://img.shields.io/badge/macOS-10.15%2B-blue?logo=apple)
![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)

---

## Features

- **Timed sessions** — 15 min / 30 min / 1 h / 2 h / 4 h, auto-stops when time is up
- **Indefinite mode** — stay awake until you click to stop
- **Screen-sleep mode** — keep the system awake while allowing the screen to dim / lock
- **Menu bar only** — no Dock icon, no App Switcher clutter (`LSUIElement = true`)
- **Zero permissions** — uses macOS built-in `caffeinate`; no privacy prompts required

---

## Requirements

| Dependency | Version |
|-----------|---------|
| macOS | 10.15 Catalina or later |
| Python | 3.11+ |
| [uv](https://docs.astral.sh/uv/) | any recent version |

---

## Installation

### Option A — Run directly

```bash
git clone https://github.com/zhuchichi56/Mac-Applications.git
cd Mac-Applications/WakeKeeper

uv sync          # install Python deps into .venv
bash run.sh      # launch the menu bar app
```

### Option B — Build a clickable .app

```bash
cd Mac-Applications/WakeKeeper
bash build_app.sh
```

This will:
1. Render a `☕` emoji icon via macOS AppKit and package it as `icon.icns`
2. Build `WakeKeeper.app` (standard macOS `.app` bundle)
3. Install it to `~/Applications`

Then just **double-click WakeKeeper** in Finder / Launchpad.

---

## Usage

| Menu item | Action |
|-----------|--------|
| **状态: 关闭** | Click to start indefinite keep-awake |
| **状态: 开启 ✓** | Click to stop the current session |
| **定时防休眠 → N 分钟/小时** | Start a timed session |
| **无限期防休眠** | Start indefinite keep-awake |
| **允许屏幕休眠** | Toggle: keep system awake but let screen dim |
| **退出** | Stop caffeinate and quit |

Menu bar icon: `☕` = idle, `⚡` = keeping awake.

---

## How it works

WakeKeeper calls the macOS built-in `caffeinate` command as a subprocess:

| Mode | Command |
|------|---------|
| Keep display on | `caffeinate -d [-t <seconds>]` |
| Allow screen sleep | `caffeinate -i [-t <seconds>]` |

A `rumps.Timer` (fires on the main thread every 2 s) monitors timed sessions and  
updates the menu bar UI when a session ends.

---

## Project structure

```
WakeKeeper/
├── main.py          # App logic — WakeKeeperApp(rumps.App)
├── make_icon.py     # Icon generator (AppKit emoji render → .icns)
├── build_app.sh     # Builds & installs WakeKeeper.app
├── run.sh           # Quick-launch script (no .app needed)
├── pyproject.toml   # uv project config + dependencies
└── icon.icns        # Pre-built app icon (regenerate with make_icon.py)
```

---

## Auto-launch at login (optional)

Save the following as `~/Library/LaunchAgents/com.user.wakekeeper.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>       <string>com.user.wakekeeper</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/bash</string>
    <string>/Users/YOUR_USERNAME/Mac-Applications/WakeKeeper/run.sh</string>
  </array>
  <key>RunAtLoad</key>   <true/>
</dict>
</plist>
```

Then run:
```bash
launchctl load ~/Library/LaunchAgents/com.user.wakekeeper.plist
```

---

## License

MIT
