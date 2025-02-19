# tests/__init__.py

"""
This package contains unit tests for Notion Text Search.
It includes:
- test_notion_api.py (Tests Notion API interactions)
"""

from dotenv import load_dotenv

# Load environment variables for testing
load_dotenv()

# Ensure test discovery works correctly
__all__ = ["test_notion_api", "test_routes"]
