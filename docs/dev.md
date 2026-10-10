# Development Log

## 2026-10-10 — WakeKeeper startup and duplicate app repair

- Question: Three WakeKeeper app entries, unresponsive launch, and default login keep-awake requested.
- Analysis/Root Cause: All three shell app launchers pointed to the legacy ~/wake-keeper directory; Python menu bar display was disabled. The running legacy app had no caffeinate process, startup default was off, and no login LaunchAgent existed.
- Solution: Use the maintained project path, start indefinitely by default, hold system idle-sleep assertions while allowing display sleep by default (as requested in the follow-up), use a singleton lock, preserve timed sessions when changing display mode, and install one login LaunchAgent. Archive duplicate app bundles locally without deleting source/history.
- Files Changed: WakeKeeper/main.py, WakeKeeper/build_app.sh, WakeKeeper/install_autostart.sh, WakeKeeper/README.md, README.md, docs/dev.md.
- Validation: Syntax checks passed; login LaunchAgent is running; real `caffeinate -i -w <app-pid>` system idle-sleep assertion verified; duplicate launch exits successfully without another instance; start/stop, timed display-mode changes and expiry tested with real subprocesses and stub menu objects. macOS Python menu bar display is enabled. Direct menu interaction could not be verified because the computer-use server timed out on the windowless Python app. The orphan legacy display-sleep assertion was terminated after confirming its working directory. Current WeChat activity independently requests display wakefulness. Independent GPT-5.5/xhigh Codex review was attempted through the configured gateway and the documented local proxy; both returned HTTP 502, so no independent review result is claimed.
- Commit Hash: Recorded in the Git commit containing this entry.
