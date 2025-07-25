#!/usr/bin/env bash
# exit on error
set -e

echo "Starting build process..."

echo "Installing Python dependencies from requirements.txt..."
pip install -r requirements.txt
echo "Python dependencies installed."

# Install Chrome and ChromeDriver manually
echo "Installing Chrome and ChromeDriver..."
apt-get update
apt-get install -y google-chrome-stable

# Get the latest ChromeDriver version compatible with installed Chrome
CHROME_VERSION=$(google-chrome-stable --version | cut -d ' ' -f3 | cut -d '.' -f1-3)
CHROMEDRIVER_VERSION=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_VERSION}")

echo "Chrome version: ${CHROME_VERSION}"
echo "ChromeDriver version: ${CHROMEDRIVER_VERSION}"

wget "https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip"
unzip chromedriver_linux64.zip
mv chromedriver /usr/local/bin/
chmod +x /usr/local/bin/chromedriver

echo "Chrome and ChromeDriver installed."

echo "Build process completed."

echo "Build process completed."