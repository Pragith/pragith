#!/bin/bash
# Standalone Tailwind CSS build script (no Node/npm required)

set -e

TAILWIND_VERSION="v3.4.1"
PLATFORM="windows-x64"
BINARY_NAME="tailwindcss-${PLATFORM}.exe"
BINARY_PATH="./.tailwind/${BINARY_NAME}"

# Create .tailwind directory if it doesn't exist
mkdir -p .tailwind

# Download standalone Tailwind CLI if not present
if [ ! -f "$BINARY_PATH" ]; then
    echo "Downloading Tailwind CSS standalone binary..."
    curl -sLO "https://github.com/tailwindlabs/tailwindcss/releases/download/${TAILWIND_VERSION}/${BINARY_NAME}"
    mv "${BINARY_NAME}" "$BINARY_PATH"
    chmod +x "$BINARY_PATH"
    echo "✓ Tailwind CLI downloaded"
fi

# Build CSS
echo "Building CSS..."
"$BINARY_PATH" -i ./app/static/css/input.css -o ./app/static/css/style.min.css --minify

echo "✓ CSS built successfully: app/static/css/style.min.css"
