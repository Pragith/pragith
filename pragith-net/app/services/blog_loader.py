import os
import glob
import markdown
import yaml
from datetime import date, datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class BlogPost(BaseModel):
    title: str
    date: date
    slug: str
    summary: str
    tags: List[str] = []
    status: str = "published"  # draft | published | unpublished
    content: str  # HTML content
    raw_content: str # content without frontmatter
    
    class Config:
        arbitrary_types_allowed = True

class BlogService:
    def __init__(self, content_dir: str):
        self.content_dir = content_dir
        self._posts: List[BlogPost] = []
        self._posts_by_slug: Dict[str, BlogPost] = {}
        self._posts_by_tag: Dict[str, List[BlogPost]] = {}
    
    def load_posts(self):
        """Loads and parses all blog posts from the content directory."""
        posts = []
        # Pattern: YYYY-MM-DD-title.md
        files = glob.glob(os.path.join(self.content_dir, "*.md"))
        
        for file_path in files:
            try:
                post = self._parse_file(file_path)
                if post and post.status == "published":
                    posts.append(post)
            except Exception as e:
                print(f"Error loading {file_path}: {e}")
        
        # Sort by date descending
        self._posts = sorted(posts, key=lambda p: p.date, reverse=True)
        self._posts_by_slug = {p.slug: p for p in self._posts}
        
        self._rebuild_tag_index()
        return self._posts

    def _parse_file(self, file_path: str) -> Optional[BlogPost]:
        filename = os.path.basename(file_path)
        # Expected format: YYYY-MM-DD-slug.md
        if not filename[0:10].replace("-", "").isdigit(): 
             # Skip if doesn't match date pattern loosely, or handle robustly
             # But spec says format is YYYY-MM-DD-title.md
             pass
             
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Split frontmatter
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter_raw = parts[1]
                body_raw = parts[2]
                
                meta = yaml.safe_load(frontmatter_raw)
                
                # Check required fields
                if not all(k in meta for k in ['title', 'date', 'summary']):
                    print(f"Skipping {filename}: Missing frontmatter")
                    return None
                
                # Parse date
                post_date = meta['date']
                if isinstance(post_date, str):
                    post_date = datetime.strptime(post_date, '%Y-%m-%d').date()
                elif isinstance(post_date, datetime):
                    post_date = post_date.date()

                # Parse Tags
                tags = meta.get('tags', [])
                if isinstance(tags, str):
                    tags = [t.strip() for t in tags.split(',')]
                # Normalize tags
                tags = [t.lower().replace(" ", "-") for t in tags]

                # Parse status (default to "published" for backwards compatibility)
                status = meta.get('status', 'published').strip().lower()

                # Convert markdown
                html_content = markdown.markdown(
                    body_raw,
                    extensions=['fenced_code', 'codehilite', 'tables', 'toc']
                )
                
                # Generate slug from filename (YYYY-MM-DD-my-slug.md -> my-slug)
                # Or use frontmatter slug if present? Spec implies filename usage.
                # "Generate clean slugs"
                # Remove date prefix and extension
                slug_candidate = filename[11:-3] 
                
                return BlogPost(
                    title=meta['title'],
                    date=post_date,
                    slug=slug_candidate,
                    summary=meta['summary'],
                    tags=tags,
                    status=status,
                    content=html_content,
                    raw_content=body_raw
                )
        return None

    def _rebuild_tag_index(self):
        self._posts_by_tag = {}
        for post in self._posts:
            for tag in post.tags:
                if tag not in self._posts_by_tag:
                    self._posts_by_tag[tag] = []
                self._posts_by_tag[tag].append(post)

    def get_all(self) -> List[BlogPost]:
        if not self._posts:
            self.load_posts()
        return self._posts

    def get_by_slug(self, slug: str) -> Optional[BlogPost]:
        if not self._posts:
            self.load_posts()
        return self._posts_by_slug.get(slug)
    
    def get_by_tag(self, tag: str) -> List[BlogPost]:
        if not self._posts:
            self.load_posts()
        return self._posts_by_tag.get(tag, [])

# Singleton instance (use absolute path so it works from any CWD)
from pathlib import Path as _Path
_CONTENT_DIR = str(_Path(__file__).parent.parent / "content" / "blog")
blog_service = BlogService(content_dir=_CONTENT_DIR)
