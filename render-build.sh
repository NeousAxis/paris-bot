#!/usr/bin/env bash
# exit on error
set -e

echo "Starting build process..."

echo "Installing Python dependencies from requirements.txt..."
pip install -r requirements.txt
echo "Python dependencies installed."

echo "Setting PLAYWRIGHT_BROWSERS_PATH to: ./.playwright-browsers"
export PLAYWRIGHT_BROWSERS_PATH=./.playwright-browsers

echo "Running Playwright browser installation..."
python -m playwright install --with-deps chromium
echo "Playwright browser installation command executed."

echo "Listing contents of ./.playwright-browsers:"
ls -lR ./.playwright-browsers
echo "Finished listing contents."

echo "Build process completed."