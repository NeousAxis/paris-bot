#!/usr/bin/env bash
# exit on error
set -e

pip install -r requirements.txt

playwright install --with-deps chromium