#!/bin/bash
set -euo pipefail

export PATH="$HOME/.local/bin:/usr/local/bin:/opt/homebrew/bin:$PATH"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
APP_NAME="MenuBarGuard"
VERSION="1.0"
DMG_NAME="$APP_NAME-$VERSION.dmg"
APP_PATH="$SCRIPT_DIR/dist/$APP_NAME.app"
DEST_APP="$HOME/Applications/$APP_NAME.app"
DEST_DMG="$REPO_ROOT/$DMG_NAME"

echo "=== $APP_NAME build ==="

cd "$SCRIPT_DIR"
uv sync
uv run python make_icon.py

rm -rf "$SCRIPT_DIR/build" "$SCRIPT_DIR/dist"
uv run pyinstaller \
  --noconfirm \
  --clean \
  --windowed \
  --name "$APP_NAME" \
  --icon "$SCRIPT_DIR/icon.icns" \
  --osx-bundle-identifier "com.zhuchichi.menubarguard" \
  "$SCRIPT_DIR/main.py"

plutil -replace LSUIElement -bool YES "$APP_PATH/Contents/Info.plist"
plutil -replace CFBundleShortVersionString -string "$VERSION" "$APP_PATH/Contents/Info.plist"
plutil -replace CFBundleVersion -string "1" "$APP_PATH/Contents/Info.plist"
plutil -replace NSHighResolutionCapable -bool YES "$APP_PATH/Contents/Info.plist"

codesign --force --deep --sign - "$APP_PATH"

mkdir -p "$HOME/Applications"
rm -rf "$DEST_APP"
cp -R "$APP_PATH" "$DEST_APP"

/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister \
  -f "$DEST_APP" 2>/dev/null || true

rm -f "$DEST_DMG"
hdiutil create \
  -volname "$APP_NAME $VERSION" \
  -srcfolder "$APP_PATH" \
  -ov \
  -format UDZO \
  "$DEST_DMG"

echo ""
echo "Built app: $APP_PATH"
echo "Installed app: $DEST_APP"
echo "Built dmg: $DEST_DMG"
