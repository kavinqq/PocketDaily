#!/bin/sh
export FLASK_APP=index.py

# Apply database migrations
flask db upgrade

# Start the application
exec gunicorn --bind 0.0.0.0:8050 --workers 2 index:app
