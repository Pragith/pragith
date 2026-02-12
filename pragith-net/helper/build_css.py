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
BINARY_DIR = PROJECT_ROOT / ".tailwind"
# BINARY_PATH is now defined dynamically below based on OS
INPUT_CSS = PROJECT_ROOT / "app" / "static" / "css" / "input.css"
OUTPUT_CSS = PROJECT_ROOT / "app" / "static" / "css" / "style.min.css"
CONFIG = PROJECT_ROOT / "tailwind.config.js"

import platform

TAILWIND_VERSION = "v3.4.1"

def get_binary_url():
    system = platform.system().lower()
    machine = platform.machine().lower()

    if system == "linux":
        if machine == "aarch64":
            return f"https://github.com/tailwindlabs/tailwindcss/releases/download/{TAILWIND_VERSION}/tailwindcss-linux-arm64", "tailwindcss-linux-arm64"
        elif machine == "x86_64":
            return f"https://github.com/tailwindlabs/tailwindcss/releases/download/{TAILWIND_VERSION}/tailwindcss-linux-x64", "tailwindcss-linux-x64"
    elif system == "darwin":
        if machine == "arm64":
            return f"https://github.com/tailwindlabs/tailwindcss/releases/download/{TAILWIND_VERSION}/tailwindcss-macos-arm64", "tailwindcss-macos-arm64"
        elif machine == "x86_64":
            return f"https://github.com/tailwindlabs/tailwindcss/releases/download/{TAILWIND_VERSION}/tailwindcss-macos-x64", "tailwindcss-macos-x64"
    elif system == "windows":
        return f"https://github.com/tailwindlabs/tailwindcss/releases/download/{TAILWIND_VERSION}/tailwindcss-windows-x64.exe", "tailwindcss.exe"

    raise RuntimeError(f"Unsupported platform: {system} {machine}")

URL, BINARY_NAME = get_binary_url()
BINARY_PATH = BINARY_DIR / BINARY_NAME


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
    
    # Make executable on Linux/macOS
    if platform.system().lower() != "windows":
        st = os.stat(BINARY_PATH)
        os.chmod(BINARY_PATH, st.st_mode | 0o111)
        print(f"  Made executable: {BINARY_PATH}")


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
