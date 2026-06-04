#!/bin/bash
# build_app.sh — 构建 WakeKeeper.app 并安装到 ~/Applications
set -euo pipefail

export PATH="$HOME/.local/bin:/usr/local/bin:/opt/homebrew/bin:$PATH"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
APP_NAME="WakeKeeper"
APP_BUNDLE="$SCRIPT_DIR/$APP_NAME.app"

echo "=== WakeKeeper.app 构建脚本 ==="
echo ""

# ── 1. 生成图标 ──────────────────────────────────────────────
echo "① 生成图标 (icon.icns)…"
cd "$SCRIPT_DIR"
uv run python make_icon.py
echo ""

# ── 2. 创建 .app 目录结构 ────────────────────────────────────
echo "② 创建 $APP_NAME.app 目录结构…"
rm -rf "$APP_BUNDLE"
mkdir -p "$APP_BUNDLE/Contents/MacOS"
mkdir -p "$APP_BUNDLE/Contents/Resources"

# ── 3. 写入 Info.plist ───────────────────────────────────────
echo "③ 写入 Info.plist…"
cat > "$APP_BUNDLE/Contents/Info.plist" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>CFBundleExecutable</key>
  <string>WakeKeeper</string>

  <key>CFBundleIconFile</key>
  <string>icon</string>

  <key>CFBundleIdentifier</key>
  <string>com.user.wakekeeper</string>

  <key>CFBundleName</key>
  <string>WakeKeeper</string>

  <key>CFBundleDisplayName</key>
  <string>WakeKeeper</string>

  <key>CFBundlePackageType</key>
  <string>APPL</string>

  <key>CFBundleShortVersionString</key>
  <string>1.0</string>

  <key>CFBundleVersion</key>
  <string>1</string>

  <!-- 纯菜单栏应用：不在 Dock 和 App Switcher 显示 -->
  <key>LSUIElement</key>
  <true/>

  <!-- Retina 高分辨率支持 -->
  <key>NSHighResolutionCapable</key>
  <true/>
</dict>
</plist>
EOF

# ── 4. 写入启动可执行文件 ─────────────────────────────────────
echo "④ 写入启动脚本 Contents/MacOS/WakeKeeper…"
cat > "$APP_BUNDLE/Contents/MacOS/WakeKeeper" << LAUNCHER
#!/bin/bash
# 确保能找到 uv（已安装在 ~/.local/bin/）
export PATH="\$HOME/.local/bin:/usr/local/bin:/opt/homebrew/bin:\$PATH"

# 进入项目目录并运行
cd "\$HOME/wake-keeper"
exec uv run python main.py
LAUNCHER
chmod +x "$APP_BUNDLE/Contents/MacOS/WakeKeeper"

# ── 5. 复制图标 ──────────────────────────────────────────────
echo "⑤ 复制 icon.icns 到 Resources…"
cp "$SCRIPT_DIR/icon.icns" "$APP_BUNDLE/Contents/Resources/icon.icns"

# ── 6. 安装到 ~/Applications ─────────────────────────────────
echo "⑥ 安装到 ~/Applications…"
mkdir -p "$HOME/Applications"
DEST="$HOME/Applications/$APP_NAME.app"
rm -rf "$DEST"
cp -r "$APP_BUNDLE" "$DEST"

# 刷新 LaunchServices（让 Spotlight/Finder 识别）
/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister \
  -f "$DEST" 2>/dev/null || true

echo ""
echo "✅ 完成！WakeKeeper.app 已安装到:"
echo "   $DEST"
echo ""
echo "▶  直接双击打开，或通过 Launchpad 搜索 'WakeKeeper'"
echo "   图标: ☕（未激活）→ ⚡（防休眠中）"
