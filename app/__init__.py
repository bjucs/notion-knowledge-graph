# app/__init__.py

"""
This package contains the core application logic for the Notion Knowledge Graph.
It includes:
- notion_api.py (Handles Notion API requests)
- graph_db.py (Manages Neo4j interactions)
- routes.py (Defines FastAPI endpoints)
"""

# Optional: Define what gets imported when doing `from app import *`
from .notion_api import fetch_page_blocks, fetch_all_pages
