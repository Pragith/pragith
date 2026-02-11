"""Bulk-replace old color classes with semantic tokens in all HTML templates."""
import re
from pathlib import Path

TEMPLATES = Path(__file__).resolve().parent.parent / "app" / "templates"

# Ordered replacements (most specific first to avoid partial matches)
REPLACEMENTS = [
    # Borders
    ("border-black/20", "border-line/20"),
    ("border-black/10", "border-line/10"),
    ("border-black", "border-line"),
    # Backgrounds
    ("bg-white", "bg-surface"),
    # Text
    ("text-black/80", "text-ink/80"),
    ("text-black/70", "text-ink/70"),
    ("text-black/60", "text-ink/60"),
    ("text-black/50", "text-ink/50"),
    ("text-black/40", "text-ink/40"),
    ("text-black/20", "text-ink/20"),
    ("text-black/10", "text-ink/10"),
    ("text-black/5", "text-ink/5"),
    ("text-black", "text-ink"),
    # Buttons
    ("bg-black text-white", "bg-ink text-page"),
    ("hover:bg-black hover:text-white", "hover:bg-ink hover:text-page"),
]

# Files to skip (already converted)
SKIP = {"base.html", "index.html", "agents.html", "work.html", "work_detail.html",
        "blog_list.html", "blog_detail.html", "contact.html"}

count = 0
for f in sorted(TEMPLATES.glob("*.html")):
    if f.name in SKIP:
        continue
    original = f.read_text(encoding="utf-8")
    updated = original
    for old, new in REPLACEMENTS:
        updated = updated.replace(old, new)
    if updated != original:
        f.write_text(updated, encoding="utf-8")
        count += 1
        print(f"  ✓ {f.name}")
    else:
        print(f"  - {f.name} (no changes)")

print(f"\nUpdated {count} files.")
