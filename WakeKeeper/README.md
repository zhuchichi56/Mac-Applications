# ☕ WakeKeeper

A lightweight macOS menu bar app to prevent your Mac from sleeping —  
inspired by [Amphetamine](https://apps.apple.com/app/amphetamine/id937984704), built with Python + [rumps](https://github.com/jaredks/rumps).

![macOS](https://img.shields.io/badge/macOS-10.15%2B-blue?logo=apple)
![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)

---

## Features

- **Timed sessions** — 15 min / 30 min / 1 h / 2 h / 4 h, auto-stops when time is up
- **Indefinite mode** — starts automatically; stay awake until you click to stop
- **Screen-sleep mode (default)** — keep the system awake while allowing the screen to dim / lock
- **Single instance** — opening the app repeatedly does not create duplicate icons
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
| Keep display on | `caffeinate -di -w <app-pid> [-t <seconds>]` |
| Allow screen sleep | `caffeinate -i -w <app-pid> [-t <seconds>]` |

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

## Auto-launch at login

After building the app, run:

```bash
bash install_autostart.sh
```

This installs one `com.user.wakekeeper` LaunchAgent. Login startup and manual
launch both use the maintained project path and start indefinite system
keep-awake, with display sleep allowed. Choosing Quit stops the app until the
next login or manual launch. The app requires this project and its uv environment
to remain installed.

The menu bar entry may be listed as **Python** in macOS Menu Bar settings because
this app uses the Python runtime. Enable that entry to show its coffee/lightning
icon. Clicking the application in Finder opens a menu bar tool, not a window;
click the menu bar icon to change the active session.

This prevents **idle system sleep**. It does not override lid-close sleep,
explicit Sleep commands, shutdown, or critical battery behavior. Screen locking
and screen sleep remain available in the default mode.

---

## License

MIT
