#!/usr/bin/env bash
# exit on error
set -e

pip install -r requirements.txt

export PLAYWRIGHT_BROWSERS_PATH=./.playwright-browsers
playwright install --with-deps chromium

ls -lR ./.playwright-browsers
