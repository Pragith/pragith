from typing import List
from datetime import datetime
from pydantic import BaseModel


class SitemapURL(BaseModel):
    loc: str
    lastmod: str = datetime.now().strftime("%Y-%m-%d")
    changefreq: str = "weekly"
    priority: float = 0.5


class SitemapService:
    """Generate XML sitemap for the website."""
    
    def __init__(self, base_url: str = "https://pragith.net"):
        self.base_url = base_url
        self._urls: List[SitemapURL] = []
    
    def add_url(self, path: str, priority: float = 0.5, changefreq: str = "weekly"):
        """Add a URL to the sitemap."""
        self._urls.append(SitemapURL(
            loc=f"{self.base_url}{path}",
            priority=priority,
            changefreq=changefreq
        ))
    
    def generate_static_urls(self):
        """Add all static pages to the sitemap."""
        # High priority pages
        self.add_url("/", priority=1.0, changefreq="weekly")
        self.add_url("/work", priority=0.9, changefreq="weekly")
        self.add_url("/blog", priority=0.9, changefreq="daily")
        
        # Business pages
        self.add_url("/business", priority=0.8, changefreq="monthly")
        self.add_url("/business/automation", priority=0.8, changefreq="monthly")
        self.add_url("/business/whatsapp-automation", priority=0.8, changefreq="monthly")
        self.add_url("/business/dashboards", priority=0.8, changefreq="monthly")
        
        # Method pages
        self.add_url("/agents", priority=0.7, changefreq="monthly")
        self.add_url("/build", priority=0.7, changefreq="monthly")
        self.add_url("/stack", priority=0.7, changefreq="monthly")
        
        # Other pages
        self.add_url("/contact", priority=0.6, changefreq="monthly")
        self.add_url("/legal", priority=0.3, changefreq="yearly")
        self.add_url("/privacy", priority=0.3, changefreq="yearly")
        self.add_url("/faq", priority=0.5, changefreq="monthly")
    
    def add_blog_posts(self, posts):
        """Add blog posts to the sitemap."""
        for post in posts:
            self.add_url(
                f"/blog/{post.slug}",
                priority=0.7,
                changefreq="monthly"
            )
    
    def add_work_items(self, work_items):
        """Add work items to the sitemap."""
        for item in work_items:
            self.add_url(
                f"/work/{item.slug}",
                priority=0.8,
                changefreq="monthly"
            )

    def add_offerings(self, offerings):
        """Add offering pages to the sitemap."""
        for offering in offerings:
            self.add_url(
                f"/packages/{offering.slug}",
                priority=0.7,
                changefreq="monthly"
            )
    
    def generate_xml(self) -> str:
        """Generate the XML sitemap."""
        xml_lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        ]
        
        for url in self._urls:
            xml_lines.append("  <url>")
            xml_lines.append(f"    <loc>{url.loc}</loc>")
            xml_lines.append(f"    <lastmod>{url.lastmod}</lastmod>")
            xml_lines.append(f"    <changefreq>{url.changefreq}</changefreq>")
            xml_lines.append(f"    <priority>{url.priority}</priority>")
            xml_lines.append("  </url>")
        
        xml_lines.append("</urlset>")
        return "\n".join(xml_lines)


# Singleton instance
sitemap_service = SitemapService()
