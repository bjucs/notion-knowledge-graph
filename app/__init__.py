# app/__init__.py

"""
This package contains the core application logic for Notion Text Search.
It includes:
- notion_api.py (Handles Notion API requests)
"""

# Optional: Define what gets imported when doing `from app import *`
from .notion_api import notion_search
