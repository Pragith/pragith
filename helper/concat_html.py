"""
HTML Concatenation Helper Script
Concatenates all HTML template files into a single file with proper formatting.
"""

from pathlib import Path
from datetime import datetime

def concat_html_files(
    templates_dir: Path,
    output_dir: Path,
    exclude_patterns: list[str] = None
) -> Path:
    """
    Concatenate all HTML files from templates directory.
    
    Args:
        templates_dir: Path to the templates directory
        output_dir: Path to output directory
        exclude_patterns: List of filename patterns to exclude
    
    Returns:
        Path to the created output file
    """
    if exclude_patterns is None:
        exclude_patterns = []
    
    # Get all HTML files
    html_files = sorted(templates_dir.glob("**/*.html"))
    
    # Filter out excluded files
    html_files = [
        f for f in html_files 
        if not any(pattern in f.name for pattern in exclude_patterns)
    ]
    
    # Create timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"website_content_{timestamp}.html"
    
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Build concatenated content
    content_parts = []
    
    # Add header
    content_parts.append("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Website Content Snapshot - {timestamp}</title>
    <style>
        body {{
            font-family: monospace;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .file-section {{
            background: white;
            margin: 30px 0;
            padding: 20px;
            border: 2px solid #333;
            box-shadow: 4px 4px 0px 0px #000;
        }}
        .file-header {{
            background: #000;
            color: #0f0;
            padding: 10px 15px;
            margin: -20px -20px 20px -20px;
            font-weight: bold;
            font-size: 16px;
        }}
        .file-path {{
            color: #0f0;
            opacity: 0.7;
            font-size: 12px;
            margin-top: 5px;
        }}
        .file-content {{
            background: #fafafa;
            border-left: 4px solid #0f0;
            padding: 15px;
            overflow-x: auto;
            white-space: pre-wrap;
            word-wrap: break-word;
        }}
        .separator {{
            border-top: 3px dashed #333;
            margin: 50px 0;
        }}
        .index {{
            background: white;
            border: 2px solid #333;
            padding: 20px;
            margin-bottom: 30px;
        }}
        .index h2 {{
            margin-top: 0;
            border-bottom: 2px solid #333;
            padding-bottom: 10px;
        }}
        .index ul {{
            list-style: none;
            padding: 0;
        }}
        .index li {{
            padding: 5px 0;
        }}
        .index a {{
            color: #000;
            text-decoration: none;
        }}
        .index a:hover {{
            color: #0f0;
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <h1>Website Content Snapshot</h1>
    <p><strong>Generated:</strong> {timestamp_readable}</p>
    <p><strong>Total Files:</strong> {file_count}</p>
    
    <div class="index">
        <h2>📋 File Index</h2>
        <ul>
{index_items}
        </ul>
    </div>
""".format(
        timestamp=timestamp,
        timestamp_readable=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        file_count=len(html_files),
        index_items=""  # Will be filled later
    ))
    
    # Build index
    index_items = []
    file_sections = []
    
    for idx, html_file in enumerate(html_files, 1):
        relative_path = html_file.relative_to(templates_dir)
        file_id = f"file-{idx}"
        
        # Add to index
        index_items.append(f'            <li><a href="#{file_id}">{idx}. {relative_path}</a></li>')
        
        # Read file content
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                file_content = f.read()
        except Exception as e:
            file_content = f"ERROR READING FILE: {str(e)}"
        
        # Escape HTML for display
        file_content_escaped = (
            file_content
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
        )
        
        # Add file section
        file_sections.append(f"""
    <div class="file-section" id="{file_id}">
        <div class="file-header">
            📄 {html_file.name}
            <div class="file-path">{relative_path}</div>
        </div>
        <div class="file-content">{file_content_escaped}</div>
    </div>
    
    <div class="separator"></div>
""")
    
    # Update header with index
    content_parts[0] = content_parts[0].replace(
        '{index_items}',
        '\n'.join(index_items)
    )
    
    # Add all file sections
    content_parts.extend(file_sections)
    
    # Add footer
    content_parts.append("""
    <footer style="text-align: center; margin-top: 50px; padding: 20px; border-top: 2px solid #333;">
        <p>End of Website Content Snapshot</p>
        <p style="color: #666; font-size: 12px;">Generated by pragith.net helper script</p>
    </footer>
</body>
</html>
""")
    
    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(content_parts))
    
    return output_file


if __name__ == "__main__":
    # Configuration
    TEMPLATES_DIR = Path(r"../pragith-net/app/templates")
    OUTPUT_DIR = Path(r"../helper")
    
    # Files to exclude (if any)
    EXCLUDE_PATTERNS = [
        # Example: "base.html"  # Uncomment to exclude base templates
    ]
    
    print("HTML Concatenation Helper")
    print("=" * 50)
    print(f"Templates Directory: {TEMPLATES_DIR}")
    print(f"Output Directory: {OUTPUT_DIR}")
    print()
    
    # Run concatenation
    output_file = concat_html_files(
        templates_dir=TEMPLATES_DIR,
        output_dir=OUTPUT_DIR,
        exclude_patterns=EXCLUDE_PATTERNS
    )
    
    print(f"✅ Success!")
    print(f"📁 Output file: {output_file}")
    print(f"📊 File size: {output_file.stat().st_size:,} bytes")
    print()
    print("You can open this file in your browser to view all HTML templates.")
