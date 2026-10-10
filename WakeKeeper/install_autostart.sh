#!/bin/bash
# Install login startup for the canonical WakeKeeper app.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
export PATH="$HOME/.local/bin:/opt/homebrew/bin:$PATH"
cd "$SCRIPT_DIR"
uv run python - <<'PY'
from pathlib import Path
import plistlib

home = Path.home()
app = home / "Applications/WakeKeeper.app/Contents/MacOS/WakeKeeper"
if not app.is_file():
    raise SystemExit("Build WakeKeeper.app before installing login startup.")
logs = home / "Library/Logs/WakeKeeper"
logs.mkdir(parents=True, exist_ok=True)
agent = home / "Library/LaunchAgents/com.user.wakekeeper.plist"
agent.parent.mkdir(parents=True, exist_ok=True)
if agent.exists():
    raise SystemExit("Existing login agent found; back it up before replacing it.")
agent.write_bytes(plistlib.dumps({
    "Label": "com.user.wakekeeper",
    "ProgramArguments": ["/bin/bash", str(app)],
    "RunAtLoad": True,
    "LimitLoadToSessionType": "Aqua",
    "StandardOutPath": str(logs / "stdout.log"),
    "StandardErrorPath": str(logs / "stderr.log"),
}))
PY
launchctl bootstrap "gui/$(id -u)" "$HOME/Library/LaunchAgents/com.user.wakekeeper.plist"
