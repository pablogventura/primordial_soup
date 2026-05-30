#!/usr/bin/env python3
"""Muestrea colores dominantes de img/background.png → tools/palette.json"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
IMG = ROOT / "img" / "background.png"
OUT = ROOT / "tools" / "palette.json"


def bucket(rgb: tuple[int, int, int], step: int = 8) -> tuple[int, int, int]:
    return tuple(min(255, (c // step) * step + step // 2) for c in rgb)


def luminance(rgb: tuple[int, int, int]) -> float:
    r, g, b = rgb
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def hex_rgb(rgb: tuple[int, int, int] | list[int]) -> str:
    r, g, b = rgb
    return "#{:02x}{:02x}{:02x}".format(r, g, b)


def derive_accent(base: list[int]) -> list[int]:
    r, g, b = base
    return [min(255, r + 30), min(255, g + 95), min(255, b + 155)]


def derive_light(base: list[int]) -> list[int]:
    r, g, b = base
    return [min(255, r + 18), min(255, g + 35), min(255, b + 55)]


def main() -> None:
    img = Image.open(IMG).convert("RGB")
    w, h = img.size
    pixels = list(img.getdata())

    counts = Counter(bucket(p) for p in pixels)
    ranked = [c for c, _ in counts.most_common(16)]
    dark = min(ranked, key=luminance)
    base = sorted(ranked, key=luminance)[min(1, len(ranked) - 1)]

    blueish = [bucket(p) for p in pixels if p[2] > p[0] + 8]
    if blueish:
        accent = Counter(blueish).most_common(1)[0][0]
    else:
        accent = tuple(derive_accent(list(base)))

    if luminance(accent) < 70:
        accent = tuple(derive_accent(list(base)))

    light = tuple(derive_light(list(base)))
    if luminance(light) <= luminance(base):
        light = tuple(derive_light(list(accent)))

    palette = {
        "source": str(IMG.relative_to(ROOT)),
        "image_size": [w, h],
        "dark": list(dark),
        "base": list(base),
        "light": list(light),
        "accent": list(accent),
        "dark_hex": hex_rgb(dark),
        "base_hex": hex_rgb(base),
        "light_hex": hex_rgb(light),
        "accent_hex": hex_rgb(accent),
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(palette, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUT}")
    print(json.dumps(palette, indent=2))


if __name__ == "__main__":
    main()
