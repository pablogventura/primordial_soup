#!/usr/bin/env python3
"""Escribe colores del tema en manifest.json a partir de tools/palette.json."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifest.json"
PALETTE = ROOT / "tools" / "palette.json"


def rgba(rgb: list[int] | tuple[int, int, int], alpha: float) -> str:
    r, g, b = rgb
    return f"rgba({r}, {g}, {b}, {alpha})"


def accent_light(accent: list[int]) -> str:
    r, g, b = accent
    return "#{:02x}{:02x}{:02x}".format(
        min(255, r + 30), min(255, g + 25), min(255, b + 20)
    )


def build_colors(p: dict) -> dict[str, str]:
    dark, base, light, accent = p["dark"], p["base"], p["light"], p["accent"]
    accent_hex = p["accent_hex"]
    loading = accent_light(accent)

    return {
        "button_background_active": rgba(light, 0.78),
        "button_background_hover": rgba(base, 0.72),
        "bookmark_text": "rgba(255, 255, 255, 0.88)",
        "frame": rgba(base, 0.52),
        "frame_inactive": rgba(dark, 0.38),
        "icons": "rgba(255, 255, 255, 0.88)",
        "icons_attention": accent_hex,
        "ntp_background": rgba(dark, 0.94),
        "ntp_card_background": rgba(light, 0.76),
        "ntp_text": "rgba(255, 255, 255, 0.88)",
        "popup": rgba(base, 0.90),
        "popup_border": rgba(light, 0.78),
        "popup_highlight": rgba(accent, 0.30),
        "popup_highlight_text": "#ffffff",
        "popup_text": "rgba(255, 255, 255, 0.88)",
        "sidebar": rgba(base, 0.90),
        "sidebar_border": rgba(light, 0.78),
        "sidebar_highlight": rgba(accent, 0.30),
        "sidebar_highlight_text": "#ffffff",
        "sidebar_text": "rgba(255, 255, 255, 0.88)",
        "tab_background_separator": "rgba(255, 255, 255, 0.12)",
        "tab_background_text": "#8a9bb0",
        "tab_loading": loading,
        "tab_selected": rgba(light, 0.72),
        "tab_text": "#ffffff",
        "tab_line": accent_hex,
        "toolbar": rgba(light, 0.46),
        "toolbar_bottom_separator": rgba(dark, 0.40),
        "toolbar_field": rgba(dark, 0.55),
        "toolbar_field_border": "transparent",
        "toolbar_field_border_focus": accent_hex,
        "toolbar_field_focus": rgba(base, 0.68),
        "toolbar_field_highlight": rgba(light, 0.72),
        "toolbar_field_highlight_text": "#ffffff",
        "toolbar_field_separator": rgba(dark, 0.40),
        "toolbar_field_text": "rgba(255, 255, 255, 0.88)",
        "toolbar_field_text_focus": "#ffffff",
        "toolbar_top_separator": rgba(light, 0.0),
        "toolbar_vertical_separator": "rgba(255, 255, 255, 0.12)",
    }


def main() -> None:
    palette = json.loads(PALETTE.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    manifest["theme"]["colors"] = build_colors(palette)
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Updated colors in {MANIFEST}")


if __name__ == "__main__":
    main()
