"""Download Tailwind CSS standalone binary and build CSS."""
import os
import sys
import subprocess
import urllib.request

TAILWIND_VERSION = "v3.4.1"
BINARY_DIR = ".tailwind"
BINARY_NAME = "tailwindcss.exe"
BINARY_PATH = os.path.join(BINARY_DIR, BINARY_NAME)
URL = f"https://github.com/tailwindlabs/tailwindcss/releases/download/{TAILWIND_VERSION}/tailwindcss-windows-x64.exe"

def main():
    os.makedirs(BINARY_DIR, exist_ok=True)
    
    if not os.path.exists(BINARY_PATH):
        print(f"Downloading Tailwind CSS {TAILWIND_VERSION}...")
        urllib.request.urlretrieve(URL, BINARY_PATH)
        print("Downloaded successfully.")
    else:
        print("Tailwind binary already exists.")
    
    print("Building CSS...")
    result = subprocess.run(
        [BINARY_PATH, "-i", "./app/static/css/input.css", "-o", "./app/static/css/style.min.css", "--minify"],
        capture_output=True, text=True
    )
    
    if result.returncode == 0:
        print("CSS built successfully!")
        size = os.path.getsize("./app/static/css/style.min.css")
        print(f"Output: app/static/css/style.min.css ({size:,} bytes)")
    else:
        print(f"CSS build FAILED:\n{result.stderr}")
        sys.exit(1)

if __name__ == "__main__":
    main()
