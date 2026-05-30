#!/usr/bin/env python3
"""Genera iconos del tema (burbujas primordiales sobre fondo azul oscuro)."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
ICONS = ROOT / "icons"
PALETTE = ROOT / "tools" / "palette.json"
SIZES = (32, 48, 96, 128)


def load_palette() -> dict:
    if PALETTE.exists():
        return json.loads(PALETTE.read_text(encoding="utf-8"))
    return {
        "dark": [10, 14, 28],
        "base": [14, 20, 36],
        "light": [36, 52, 82],
        "accent": [58, 143, 217],
    }


def render_icon(size: int, palette: dict) -> Image.Image:
    dark = tuple(palette["dark"])
    base = tuple(palette["base"])
    accent = tuple(palette["accent"])
    light = tuple(palette["light"])

    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    pad = max(2, size // 16)
    draw.ellipse([pad, pad, size - pad, size - pad], fill=base + (255,))

    blobs = [
        (0.38, 0.42, 0.28, accent + (235,)),
        (0.62, 0.34, 0.22, light + (220,)),
        (0.52, 0.68, 0.24, accent + (200,)),
        (0.24, 0.58, 0.16, (100, 170, 230, 190)),
        (0.74, 0.62, 0.14, (70, 130, 200, 180)),
    ]
    for cx, cy, radius, color in blobs:
        r = int(size * radius)
        x = int(size * cx)
        y = int(size * cy)
        draw.ellipse([x - r, y - r, x + r, y + r], fill=color)

    # brillo sutil arriba
    glow_r = size // 3
    draw.ellipse(
        [size // 2 - glow_r, pad, size // 2 + glow_r, size // 2],
        fill=accent + (40,),
    )

    # borde
    draw.ellipse([pad, pad, size - pad, size - pad], outline=dark + (255,), width=max(1, size // 32))
    return img


def main() -> None:
    palette = load_palette()
    ICONS.mkdir(parents=True, exist_ok=True)
    master = render_icon(128, palette)
    for size in SIZES:
        out = ICONS / f"icon-{size}.png"
        icon = master if size == 128 else master.resize((size, size), Image.Resampling.LANCZOS)
        icon.save(out, optimize=True)
        print(f"Wrote {out}")


if __name__ == "__main__":
    main()
