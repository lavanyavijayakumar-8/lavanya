#!/usr/bin/env bash
# Exit immediately if a command exits with a non-zero status
set -o errexit

# Upgrade pip and install production dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Pre-seed demo sample images for the 1-click test gallery
python seed_samples.py

# Collect all static files into staticfiles/ for WhiteNoise
python manage.py collectstatic --no-input
