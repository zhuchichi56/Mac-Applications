"""
生成 WakeKeeper 的应用图标 (icon.icns)

原理：
  1. 用 AppKit / PyObjC 将 ☕ emoji 渲染成真彩 PNG（1024×1024）
  2. 用 Pillow 合成圆角矩形背景 + emoji 层
  3. 用 macOS 内置 iconutil 打包成 .icns
"""

import io
import os
import shutil
import subprocess
import sys

from PIL import Image, ImageDraw


# ── 1. 用 AppKit 渲染 emoji（真彩，含阴影）──────────────────────

def render_emoji_native(emoji: str, canvas: int) -> Image.Image:
    """通过 AppKit/PyObjC 在透明背景上渲染彩色 emoji，返回 PIL.Image。"""
    from AppKit import (
        NSImage, NSBitmapImageRep, NSGraphicsContext,
        NSColor, NSFont, NSAttributedString,
        NSFontAttributeName, NSBezierPath,
    )
    from Foundation import NSMakeSize, NSMakePoint, NSMakeRect

    ns_img = NSImage.alloc().initWithSize_(NSMakeSize(canvas, canvas))
    ns_img.lockFocus()

    # 透明背景
    NSColor.clearColor().set()
    NSBezierPath.fillRect_(NSMakeRect(0, 0, canvas, canvas))

    # 绘制 emoji（字号约为画布 58%）
    font_size = int(canvas * 0.58)
    font = NSFont.fontWithName_size_("Apple Color Emoji", font_size)
    attrs = {NSFontAttributeName: font}
    astr = NSAttributedString.alloc().initWithString_attributes_(emoji, attrs)

    # 垂直偏移：AppKit 坐标系 y 轴朝上，稍微向上抬一点
    x = int(canvas * 0.21)
    y = int(canvas * 0.14)
    astr.drawAtPoint_(NSMakePoint(x, y))

    ns_img.unlockFocus()

    # 转 PNG → PIL
    tiff = ns_img.TIFFRepresentation()
    bitmap = NSBitmapImageRep.imageRepWithData_(tiff)
    png_bytes = bytes(bitmap.representationUsingType_properties_(4, {}))
    return Image.open(io.BytesIO(png_bytes)).convert("RGBA")


# ── 2. 合成最终图标 ──────────────────────────────────────────────

def compose_icon(size: int) -> Image.Image:
    """圆角矩形背景 + 真彩 emoji，输出 RGBA PIL.Image。"""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 圆角背景（深咖啡色 #4A3120）
    pad = max(int(size * 0.03), 2)
    radius = int(size * 0.22)
    draw.rounded_rectangle(
        [pad, pad, size - pad, size - pad],
        radius=radius,
        fill=(74, 49, 32, 255),
    )

    # 叠加 emoji 层
    try:
        emoji_layer = render_emoji_native("☕", size)
        img.alpha_composite(emoji_layer)
        print("   ✓ 使用 AppKit 渲染真彩 emoji")
    except Exception as e:
        print(f"   ⚠ AppKit 渲染失败，改用手绘: {e}")
        _draw_cup_fallback(draw, size)

    return img


def _draw_cup_fallback(draw: ImageDraw.ImageDraw, s: int) -> None:
    """备用手绘风格，当 AppKit 不可用时使用。"""
    cream = (240, 218, 190, 255)
    espresso = (44, 26, 12, 255)
    steam_c = (255, 255, 255, 140)
    cx = s // 2
    tw, bw = int(s * 0.42), int(s * 0.36)
    ty, by = int(s * 0.33), int(s * 0.71)

    draw.polygon(
        [(cx - tw // 2, ty), (cx + tw // 2, ty),
         (cx + bw // 2, by), (cx - bw // 2, by)],
        fill=cream,
    )
    m = int(s * 0.035)
    draw.polygon(
        [(cx - tw // 2 + m, ty + m), (cx + tw // 2 - m, ty + m),
         (cx + bw // 2 - m, by - m), (cx - bw // 2 + m, by - m)],
        fill=espresso,
    )
    sw2, sh = int(s * 0.52), int(s * 0.08)
    draw.ellipse([cx - sw2 // 2, by - sh // 2, cx + sw2 // 2, by + sh // 2], fill=cream)
    hx, hw = cx + bw // 2 - int(s * 0.015), int(s * 0.14)
    hy = ty + int((by - ty) * 0.18)
    hh = int((by - ty) * 0.57)
    draw.arc([hx, hy, hx + hw, hy + hh], start=-90, end=90,
             fill=cream, width=max(int(s * 0.042), 3))
    st = max(int(s * 0.025), 2)
    for xo in (-int(s * 0.09), 0, int(s * 0.09)):
        draw.line([(cx + xo, ty - int(s * 0.02)),
                   (cx + xo + int(s * 0.02), ty - int(s * 0.13))],
                  fill=steam_c, width=st)


# ── 3. 生成 iconset → .icns ─────────────────────────────────────

SPECS = [
    ("icon_16x16.png",       16),
    ("icon_16x16@2x.png",    32),
    ("icon_32x32.png",       32),
    ("icon_32x32@2x.png",    64),
    ("icon_128x128.png",    128),
    ("icon_128x128@2x.png", 256),
    ("icon_256x256.png",    256),
    ("icon_256x256@2x.png", 512),
    ("icon_512x512.png",    512),
    ("icon_512x512@2x.png",1024),
]


def build_icns(output_dir: str = ".") -> str:
    iconset_dir = os.path.join(output_dir, "icon.iconset")
    os.makedirs(iconset_dir, exist_ok=True)

    print("🖌  合成图标各尺寸…")
    base = compose_icon(1024)

    for fname, px in SPECS:
        resized = base.resize((px, px), Image.LANCZOS)
        resized.save(os.path.join(iconset_dir, fname))
        print(f"   ✓ {fname:28s} ({px}×{px})")

    icns_path = os.path.join(output_dir, "icon.icns")
    print("🔨 运行 iconutil 生成 .icns…")
    r = subprocess.run(
        ["iconutil", "-c", "icns", iconset_dir, "-o", icns_path],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        print(f"[error] iconutil: {r.stderr}")
        sys.exit(1)

    shutil.rmtree(iconset_dir)
    print(f"✅ 图标已生成: {icns_path}  ({os.path.getsize(icns_path) // 1024} KB)")
    return icns_path


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    build_icns(script_dir)
