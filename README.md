# Mac Applications

A collection of small macOS apps and installers. Each app has its own section, release artifact, and source notes when source code is available.

## Projects

| App | Version | Type | Download |
|-----|---------|------|----------|
| [WakeKeeper](#wakekeeper) | 1.0 | Menu bar utility | [WakeKeeper-1.0.dmg](https://github.com/zhuchichi56/Mac-Applications/releases/download/v1.0/WakeKeeper-1.0.dmg) |
| [MenuBarGuard](#menubarguard) | 1.0 | Menu bar spacer | [MenuBarGuard-1.0.dmg](https://github.com/zhuchichi56/Mac-Applications/releases/download/menubarguard-v1.0/MenuBarGuard-1.0.dmg) |
| [Clash Verge Rev](#clash-verge-rev) | 2.5.1 | Proxy client | [Clash.Verge_2.5.1_aarch64.dmg](https://github.com/zhuchichi56/Mac-Applications/releases/download/clash-verge-rev-v2.5.1/Clash.Verge_2.5.1_aarch64.dmg) |
| [FastLink Lite](#fastlink-lite) | 3.0.3 | macOS installer | [flapp-lite.pkg](https://github.com/zhuchichi56/Mac-Applications/releases/download/fastlink-lite-v3.0.3/flapp-lite.pkg) |

## WakeKeeper

A simple Amphetamine-style keep-awake utility for macOS.

![macOS](https://img.shields.io/badge/macOS-10.15%2B-blue?logo=apple)
![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)

### Download

[Download WakeKeeper-1.0.dmg](https://github.com/zhuchichi56/Mac-Applications/releases/download/v1.0/WakeKeeper-1.0.dmg)

### Features

| Feature | Detail |
|---------|--------|
| Timed sessions | 15 min / 30 min / 1 h / 2 h / 4 h, auto-stops when done |
| Indefinite mode | Stay awake until manually stopped |
| Screen-sleep mode | Keep system awake while allowing the screen to dim or lock |
| Menu bar only | `LSUIElement = true`, no Dock icon or App Switcher entry |
| Zero permissions | Uses macOS built-in `caffeinate` |

### Quick Start

Requirements: Python 3.11+, [uv](https://docs.astral.sh/uv/), macOS 10.15+

```bash
git clone https://github.com/zhuchichi56/Mac-Applications.git
cd Mac-Applications/WakeKeeper
uv sync
bash run.sh
```

### Build

```bash
cd Mac-Applications/WakeKeeper
bash build_app.sh
```

The build script installs `WakeKeeper.app` to `~/Applications`.

### Implementation

| Mode | Command |
|------|---------|
| Keep display on | `caffeinate -d [-t seconds]` |
| Allow screen sleep | `caffeinate -i [-t seconds]` |

## MenuBarGuard

A lightweight menu bar helper for Mac notch/menu-bar crowding. It creates an adjustable empty status item, so you can reserve space near the notch and keep important menu bar icons visible.

![macOS](https://img.shields.io/badge/macOS-11.0%2B-blue?logo=apple)
![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?logo=python&logoColor=white)
![Version](https://img.shields.io/badge/version-1.0-green)
![Architecture](https://img.shields.io/badge/arch-arm64-lightgrey)

### Download

[Download MenuBarGuard-1.0.dmg](https://github.com/zhuchichi56/Mac-Applications/releases/download/menubarguard-v1.0/MenuBarGuard-1.0.dmg)

### Features

| Feature | Detail |
|---------|--------|
| Adjustable guard gap | 0 to 640 px, with presets and 20 px fine tuning |
| Notch estimate | Uses macOS safe-area APIs when available, otherwise falls back to 220 px |
| Menu bar only | No Dock icon or normal app window |
| Persistence | Remembers enabled state and width |
| Public APIs | Uses AppKit `NSStatusItem`; no private menu-bar control APIs |

### Usage

1. Open `MenuBarGuard.app`.
2. Click `MBG` in the menu bar.
3. Turn on the blank guard area and tune the width.
4. Hold Command and drag menu bar icons around the guard area.

macOS does not allow a normal third-party app to directly move or hide other apps' menu bar items. MenuBarGuard reserves space instead.

### App Info

| Field | Value |
|-------|-------|
| App bundle | `MenuBarGuard.app` |
| Bundle ID | `com.zhuchichi.menubarguard` |
| Version | `1.0` |
| Architecture | `arm64` |
| Code signing | Ad-hoc signed |
| SHA-256 | `ab844eb304fad205d58985f28f0919ae7456c425a8e170e27f1f0a3fdb259ac4` |

## Clash Verge Rev

Clash Verge Rev macOS Apple Silicon client.

![macOS](https://img.shields.io/badge/macOS-11.0%2B-blue?logo=apple)
![Version](https://img.shields.io/badge/version-2.5.1-green)
![Architecture](https://img.shields.io/badge/arch-arm64-lightgrey)

### Download

[Download Clash.Verge_2.5.1_aarch64.dmg](https://github.com/zhuchichi56/Mac-Applications/releases/download/clash-verge-rev-v2.5.1/Clash.Verge_2.5.1_aarch64.dmg)

### App Info

| Field | Value |
|-------|-------|
| App bundle | `Clash Verge.app` |
| Bundle ID | `io.github.clash-verge-rev.clash-verge-rev` |
| Version | `2.5.1` |
| Minimum macOS | `11.0` |
| Architecture | `arm64` |
| Code signing | Signed, Team ID `JPH3Z7PPBB` |
| SHA-256 | `a2016a77922b67ac058b6c247aad7809893b429f238ee7aeee1fee6e3bf70e2b` |

## FastLink Lite

FastLink Lite macOS installer package.

![macOS](https://img.shields.io/badge/macOS-10.15%2B-blue?logo=apple)
![Version](https://img.shields.io/badge/version-3.0.3-green)

### Download

[Download flapp-lite.pkg](https://github.com/zhuchichi56/Mac-Applications/releases/download/fastlink-lite-v3.0.3/flapp-lite.pkg)

### Package Info

| Field | Value |
|-------|-------|
| App bundle | `FastLink_Lite.app` |
| Bundle ID | `com.flclient.app` |
| Version | `3.0.3` |
| Build | `2026043013` |
| Minimum macOS | `10.15` |
| Install location | `/Applications/` |
| Package signature | Unsigned |
| SHA-256 | `6e67b03f0478e645010439f639eeea8ffb1a237a623e7c636c631e3f908361eb` |

## License

Source code in this repository is MIT licensed unless an app section notes otherwise. See [LICENSE](LICENSE).
