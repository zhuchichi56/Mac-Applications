# 🍎 Mac Applications

A collection of lightweight macOS utilities I built for daily use.  
All apps live in the menu bar — no Dock icon, no bloat.

---

## 📦 Projects

| App | Description | Tech |
|-----|-------------|------|
| [☕ WakeKeeper](#-wakekeeper) | Prevent your Mac from sleeping | Python · rumps · caffeinate |

---

## ☕ WakeKeeper

> A simple, free Amphetamine-style keep-awake utility for macOS.

![macOS](https://img.shields.io/badge/macOS-10.15%2B-blue?logo=apple)
![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)

### Features

| Feature | Detail |
|---------|--------|
| ⏱ Timed sessions | 15 min / 30 min / 1 h / 2 h / 4 h — auto-stops when done |
| ♾ Indefinite mode | Stay awake until you manually turn it off |
| 🌙 Screen-sleep mode | Keep system awake while allowing screen to dim / lock |
| 🔔 Menu bar only | `LSUIElement = true` — no Dock icon, no App Switcher |
| 🛠 Zero permissions | Uses macOS built-in `caffeinate` — no SIP, no privacy prompts |

### How it looks

```
Menu bar:  ☕  (idle)   →   ⚡  (keeping awake)

☕ Menu
─────────────────────────
  状态: 关闭              ← click to toggle (indefinite mode)
─────────────────────────
  ▶ 定时防休眠
      15 分钟
      30 分钟
      1 小时
      2 小时
      4 小时
  无限期防休眠
─────────────────────────
  ☐ 允许屏幕休眠          ← screen can dim, system stays awake
─────────────────────────
  退出
```

### Quick Start

**Requirements:** Python 3.11+, [uv](https://docs.astral.sh/uv/), macOS 10.15+

```bash
# 1. Clone
git clone https://github.com/zhuchichi56/Mac-Applications.git
cd Mac-Applications/WakeKeeper

# 2. Install deps
uv sync

# 3. Run directly
bash run.sh
```

### Build .app (optional)

To get a clickable app icon in your Applications folder:

```bash
cd Mac-Applications/WakeKeeper
bash build_app.sh
# → Installs WakeKeeper.app to ~/Applications
```

Double-click **WakeKeeper.app** — it will appear in your menu bar with a ☕ icon.

### How it works

| Mode | Command |
|------|---------|
| Keep display on | `caffeinate -d [-t seconds]` |
| Allow screen sleep | `caffeinate -i [-t seconds]` |

`caffeinate` is a macOS built-in tool; no additional permissions are needed.

---

## License

MIT — free to use, modify, and distribute.
