"""
Download Tailwind CSS standalone binary and build CSS.

Usage (run from project root):
    python helper/build_css.py
"""
import os
import sys
import subprocess
from pathlib import Path

# Resolve paths relative to this script
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
BINARY_DIR = PROJECT_ROOT / ".tailwind"
BINARY_PATH = BINARY_DIR / "tailwindcss.exe"
INPUT_CSS = PROJECT_ROOT / "app" / "static" / "css" / "input.css"
OUTPUT_CSS = PROJECT_ROOT / "app" / "static" / "css" / "style.min.css"
CONFIG = PROJECT_ROOT / "tailwind.config.js"

TAILWIND_VERSION = "v3.4.1"
URL = f"https://github.com/tailwindlabs/tailwindcss/releases/download/{TAILWIND_VERSION}/tailwindcss-windows-x64.exe"


def download_binary():
    """Download Tailwind standalone binary using requests."""
    try:
        import requests
    except ImportError:
        print("ERROR: 'requests' not found. Install: pip install requests")
        sys.exit(1)

    BINARY_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Downloading Tailwind CSS {TAILWIND_VERSION} (~45MB)...")
    print(f"  URL: {URL}")

    resp = requests.get(URL, stream=True, timeout=120, allow_redirects=True)
    resp.raise_for_status()

    total = int(resp.headers.get("content-length", 0))
    downloaded = 0

    with open(BINARY_PATH, "wb") as f:
        for chunk in resp.iter_content(chunk_size=65536):
            f.write(chunk)
            downloaded += len(chunk)
            if total:
                pct = int(downloaded / total * 100)
                bar = "█" * (pct // 2) + "░" * (50 - pct // 2)
                print(f"\r  [{bar}] {pct}%", end="", flush=True)

    print(f"\n  Saved: {BINARY_PATH} ({BINARY_PATH.stat().st_size:,} bytes)")


def build_css():
    """Run the Tailwind CLI to compile CSS."""
    cmd = [
        str(BINARY_PATH),
        "-i", str(INPUT_CSS),
        "-o", str(OUTPUT_CSS),
        "--minify",
        "-c", str(CONFIG),
    ]
    print(f"Building CSS...")
    print(f"  Input:  {INPUT_CSS.relative_to(PROJECT_ROOT)}")
    print(f"  Output: {OUTPUT_CSS.relative_to(PROJECT_ROOT)}")
    print(f"  Config: {CONFIG.relative_to(PROJECT_ROOT)}")

    result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(PROJECT_ROOT))

    if result.returncode == 0:
        size = OUTPUT_CSS.stat().st_size
        print(f"  Built successfully: {size:,} bytes")
    else:
        print(f"  BUILD FAILED:")
        print(result.stderr)
        sys.exit(1)


def main():
    print("=" * 50)
    print("Tailwind CSS Build Script")
    print("=" * 50)

    if not INPUT_CSS.exists():
        print(f"ERROR: Input CSS not found: {INPUT_CSS}")
        sys.exit(1)

    if not CONFIG.exists():
        print(f"ERROR: Config not found: {CONFIG}")
        sys.exit(1)

    if not BINARY_PATH.exists():
        download_binary()
    else:
        print(f"Tailwind binary found: {BINARY_PATH}")

    build_css()
    print("\nDone!")


if __name__ == "__main__":
    main()
