#!/usr/bin/env python3
from __future__ import annotations

import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


SCRIPT_DIR = Path(__file__).resolve().parent
ICONSET = SCRIPT_DIR / "icon.iconset"
ICNS = SCRIPT_DIR / "icon.icns"

SIZES = [16, 32, 64, 128, 256, 512]


def font(size: int):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/SFNS.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


def draw_icon(size: int) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    radius = int(size * 0.22)
    bg = (22, 25, 32, 255)
    border = (72, 187, 255, 255)
    accent = (255, 202, 88, 255)
    text = (245, 247, 250, 255)

    inset = int(size * 0.08)
    draw.rounded_rectangle(
        [inset, inset, size - inset, size - inset],
        radius=radius,
        fill=bg,
        outline=border,
        width=max(2, size // 36),
    )

    notch_w = int(size * 0.26)
    notch_h = int(size * 0.13)
    notch_x = (size - notch_w) // 2
    notch_y = inset
    draw.rounded_rectangle(
        [notch_x, notch_y, notch_x + notch_w, notch_y + notch_h],
        radius=max(2, notch_h // 2),
        fill=(0, 0, 0, 255),
    )

    bar_y = int(size * 0.34)
    draw.rounded_rectangle(
        [int(size * 0.2), bar_y, int(size * 0.8), bar_y + max(3, size // 18)],
        radius=max(2, size // 40),
        fill=accent,
    )

    fnt = font(max(10, int(size * 0.22)))
    label = "MBG"
    bbox = draw.textbbox((0, 0), label, font=fnt)
    x = (size - (bbox[2] - bbox[0])) / 2
    y = int(size * 0.52)
    draw.text((x, y), label, fill=text, font=fnt)

    return img


def main():
    if ICONSET.exists():
        for file in ICONSET.iterdir():
            file.unlink()
    else:
        ICONSET.mkdir()

    for size in SIZES:
        draw_icon(size).save(ICONSET / f"icon_{size}x{size}.png")
        draw_icon(size * 2).save(ICONSET / f"icon_{size}x{size}@2x.png")

    if ICNS.exists():
        ICNS.unlink()
    subprocess.run(["iconutil", "-c", "icns", str(ICONSET), "-o", str(ICNS)], check=True)
    print(f"wrote {ICNS}")


if __name__ == "__main__":
    main()
