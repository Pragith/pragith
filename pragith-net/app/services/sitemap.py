from datetime import date
from html import escape

from app.content.site import INDEXABLE_PATHS


def generate_sitemap(base_url: str = "https://pragith.net") -> str:
    today = date.today().isoformat()
    rows = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for path in INDEXABLE_PATHS:
        priority = "1.0" if path == "/" else "0.8"
        rows.extend([
            "  <url>",
            f"    <loc>{escape(base_url + path)}</loc>",
            f"    <lastmod>{today}</lastmod>",
            "    <changefreq>monthly</changefreq>",
            f"    <priority>{priority}</priority>",
            "  </url>",
        ])
    rows.append("</urlset>")
    return "\n".join(rows)
