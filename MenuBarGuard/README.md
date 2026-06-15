# MenuBarGuard

MenuBarGuard is a small macOS menu bar helper for notch/menu-bar crowding.

It creates an adjustable empty status item in the menu bar. Use it as a guard
gap near the notch or crowded area, then Command-drag menu bar items around it
so frequently used icons remain visible.

## What It Can Do

| Feature | Detail |
|---------|--------|
| Adjustable guard gap | 0 to 640 px, with presets and 20 px fine tuning |
| Notch estimate | Uses macOS safe-area APIs when available, otherwise falls back to 220 px |
| Menu bar only | No Dock icon or normal app window |
| Persistence | Remembers enabled state and width |
| Public APIs | Uses AppKit `NSStatusItem`; no private menu-bar control APIs |

## Limitations

macOS does not allow a normal third-party app to directly move, hide, or manage
other apps' menu bar items. MenuBarGuard works by reserving space; for best
results, hold Command and drag menu bar icons to arrange them around the guard.

## Run From Source

```bash
cd Mac-Applications/MenuBarGuard
uv sync
bash run.sh
```

## Build

```bash
cd Mac-Applications/MenuBarGuard
bash build_app.sh
```

The build script creates a standalone `MenuBarGuard.app`, installs it to
`~/Applications`, and writes `MenuBarGuard-1.0.dmg` to the repository root.
