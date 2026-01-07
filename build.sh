#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Run migrations (automatically creates missing tables)
python -m flask db upgrade
