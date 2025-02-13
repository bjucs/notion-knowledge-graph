# tests/__init__.py

"""
This package contains unit tests for the Notion Knowledge Graph.
It includes:
- test_notion_api.py (Tests Notion API interactions)
- test_graph_db.py (Tests Neo4j database interactions)
- test_routes.py (Tests FastAPI endpoints)
"""

from dotenv import load_dotenv

# Load environment variables for testing
load_dotenv()

# Ensure test discovery works correctly
__all__ = ["test_notion_api", "test_routes"]
