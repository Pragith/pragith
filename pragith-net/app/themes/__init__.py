"""
Modular Theme Service

Loads theme configuration from app/themes/<theme_name>/ directories.
Each theme directory contains:
  - theme.json  : metadata (name, description, fonts, palette docs)
  - variables.css : CSS custom property definitions (:root + .dark)

Usage:
  from app.themes import ThemeService
  theme = ThemeService("dubai")
  theme.css       # raw CSS string for inline <style> injection
  theme.fonts_url # Google Fonts URL to load
  theme.name      # display name
"""

import json
from pathlib import Path
from typing import Optional


class ThemeService:
    """Reads and exposes a theme's CSS variables and metadata."""

    def __init__(self, theme_name: str = "default"):
        self.themes_dir = Path(__file__).parent
        self.theme_name = theme_name
        self._meta: dict = {}
        self._css: str = ""
        self._load()

    # ── loading ──────────────────────────────────────────────

    def _load(self):
        theme_dir = self.themes_dir / self.theme_name

        if not theme_dir.exists():
            available = ", ".join(self.available_themes())
            raise ValueError(
                f"Theme '{self.theme_name}' not found. "
                f"Available themes: {available}"
            )

        # Metadata
        meta_path = theme_dir / "theme.json"
        if meta_path.exists():
            with open(meta_path, "r", encoding="utf-8") as f:
                self._meta = json.load(f)
        else:
            self._meta = {"name": self.theme_name}

        # CSS variables
        css_path = theme_dir / "variables.css"
        if css_path.exists():
            with open(css_path, "r", encoding="utf-8") as f:
                self._css = f.read()

    # ── public properties ────────────────────────────────────

    @property
    def name(self) -> str:
        return self._meta.get("name", self.theme_name)

    @property
    def description(self) -> str:
        return self._meta.get("description", "")

    @property
    def css(self) -> str:
        """Raw CSS string containing :root / .dark variable definitions,
        plus font-family custom properties."""
        font_vars = (
            f":root {{\n"
            f"    --font-display: {self.font_display};\n"
            f"    --font-body: {self.font_body};\n"
            f"    --font-mono: {self.font_mono};\n"
            f"}}\n"
        )
        return self._css + "\n" + font_vars

    @property
    def fonts_url(self) -> str:
        """Google Fonts stylesheet URL for this theme."""
        return self._meta.get("fonts", {}).get("google_fonts_url", "")

    @property
    def font_display(self) -> str:
        return self._meta.get("fonts", {}).get("display", "DM Sans")

    @property
    def font_body(self) -> str:
        return self._meta.get("fonts", {}).get("body", "Inter")

    @property
    def font_mono(self) -> str:
        return self._meta.get("fonts", {}).get("mono", "JetBrains Mono")

    @property
    def meta(self) -> dict:
        """Full theme metadata dict."""
        return self._meta

    # ── class methods ────────────────────────────────────────

    @classmethod
    def available_themes(cls) -> list[str]:
        """Returns list of installed theme directory names."""
        themes_dir = Path(__file__).parent
        return sorted([
            d.name for d in themes_dir.iterdir()
            if d.is_dir()
            and not d.name.startswith("_")
            and not d.name.startswith(".")
            and (d / "variables.css").exists()
        ])
