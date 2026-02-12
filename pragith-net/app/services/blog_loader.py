import os
import glob
import markdown
import yaml
import bleach
from slugify import slugify
from datetime import date, datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class Tag(BaseModel):
    name: str
    slug: str
    count: int = 0

class BlogPost(BaseModel):
    title: str
    date: date
    slug: str
    summary: str
    tags: List[Tag] = []
    status: str = "published"  # draft | published | unpublished
    content: str  # HTML content (sanitized)
    raw_content: str # content without frontmatter
    
    class Config:
        arbitrary_types_allowed = True

class BlogService:
    # Allowed HTML tags and attributes for sanitization
    ALLOWED_TAGS = [
        'p', 'br', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'blockquote', 'code', 'pre', 'hr', 'div', 'span',
        'ul', 'ol', 'li', 'a', 'img',
        'table', 'thead', 'tbody', 'tr', 'th', 'td',
    ]
    ALLOWED_ATTRIBUTES = {
        'a': ['href', 'title', 'rel'],
        'img': ['src', 'alt', 'title'],
        'code': ['class'],
        'pre': ['class'],
        'div': ['class'],
        'span': ['class'],
    }
    
    def __init__(self, content_dir: str):
        self.content_dir = content_dir
        self._posts: List[BlogPost] = []
        self._posts_by_slug: Dict[str, BlogPost] = {}
        self._posts_by_tag: Dict[str, List[BlogPost]] = {}
        self._all_tags: Dict[str, Tag] = {}  # slug -> Tag
    
    def load_posts(self):
        """Loads and parses all blog posts from the content directory."""
        posts = []
        # Pattern: YYYY-MM-DD-title.md (recursive)
        files = glob.glob(os.path.join(self.content_dir, "**/*.md"), recursive=True)
        
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

                # Parse Tags - create Tag objects with slugs
                tag_names = meta.get('tags', [])
                if isinstance(tag_names, str):
                    tag_names = [t.strip() for t in tag_names.split(',')]
                
                # Create Tag objects
                tags = []
                for tag_name in tag_names:
                    tag_slug = slugify(tag_name.lower())
                    tags.append(Tag(name=tag_name, slug=tag_slug))

                # Parse status (default to "published" for backwards compatibility)
                status = meta.get('status', 'published').strip().lower()

                # Convert markdown
                html_content = markdown.markdown(
                    body_raw,
                    extensions=['fenced_code', 'codehilite', 'tables', 'toc']
                )
                
                # Sanitize HTML content
                html_content = bleach.clean(
                    html_content,
                    tags=self.ALLOWED_TAGS,
                    attributes=self.ALLOWED_ATTRIBUTES,
                    strip=True
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
        self._all_tags = {}
        
        for post in self._posts:
            for tag in post.tags:
                # Index by slug
                if tag.slug not in self._posts_by_tag:
                    self._posts_by_tag[tag.slug] = []
                    self._all_tags[tag.slug] = Tag(name=tag.name, slug=tag.slug, count=0)
                
                self._posts_by_tag[tag.slug].append(post)
                self._all_tags[tag.slug].count += 1

    def get_all(self) -> List[BlogPost]:
        if not self._posts:
            self.load_posts()
        return self._posts

    def get_by_slug(self, slug: str) -> Optional[BlogPost]:
        if not self._posts:
            self.load_posts()
        return self._posts_by_slug.get(slug)
    
    def get_by_tag(self, tag_slug: str) -> List[BlogPost]:
        """Get posts by tag slug."""
        if not self._posts:
            self.load_posts()
        return self._posts_by_tag.get(tag_slug, [])
    
    def get_all_tags(self) -> List[Tag]:
        """Get all tags sorted by count descending."""
        if not self._posts:
            self.load_posts()
        return sorted(self._all_tags.values(), key=lambda t: t.count, reverse=True)

# Singleton instance (use absolute path so it works from any CWD)
from pathlib import Path as _Path
_CONTENT_DIR = str(_Path(__file__).parent.parent / "content" / "blog")
blog_service = BlogService(content_dir=_CONTENT_DIR)
