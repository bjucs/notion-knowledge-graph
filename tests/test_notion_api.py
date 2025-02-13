import unittest
from unittest.mock import patch
from app.notion_api import fetch_page_blocks, extract_page_links, fetch_all_pages

class TestNotionAPI(unittest.TestCase):
    @patch("app.notion_api.requests.get")
    def test_fetch_page_blocks_success(self, mock_get):
        """Test if fetch_page_blocks() correctly returns Notion API data"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "object": "list",
            "results": [{"id": "page_1", "type": "child_page"}]
        }

        page_data = fetch_page_blocks("test_page_id")
        self.assertIn("results", page_data)
        self.assertEqual(page_data["results"][0]["id"], "page_1")

    @patch("app.notion_api.requests.get")
    def test_fetch_page_blocks_failure(self, mock_get):
        """Test fetch_page_blocks() handles API failures"""
        mock_get.return_value.status_code = 403
        mock_get.return_value.json.return_value = {"error": "Unauthorized"}

        page_data = fetch_page_blocks("invalid_page_id")
        self.assertIn("error", page_data)

    def test_extract_page_links(self):
        """Test extract_page_links() to correctly retrieve linked pages"""
        mock_blocks = {
            "results": [
                {"id": "page_1", "type": "child_page"},
                {"id": "page_2", "type": "link_to_page", "link_to_page": {"page_id": "linked_page"}},
                {"id": "page_3", "type": "paragraph"}  # Should be ignored
            ]
        }

        linked_pages = extract_page_links(mock_blocks)
        self.assertEqual(linked_pages, ["page_1", "linked_page"])  # Should only return page IDs

    @patch("app.notion_api.fetch_page_blocks")
    def test_fetch_all_pages(self, mock_fetch_blocks):
        """Test fetch_all_pages() finds all linked pages recursively"""
        mock_fetch_blocks.side_effect = lambda page_id: {
            "results": [{"id": f"page_{int(page_id[-1]) + 1}", "type": "child_page"}]
        } if page_id != "page_3" else {"results": []}  # Stops at page_3

        all_pages = fetch_all_pages("page_1")
        self.assertIn("page_1", all_pages)
        self.assertIn("page_2", all_pages)
        self.assertIn("page_3", all_pages)  # Should include the last fetched page

if __name__ == "__main__":
    unittest.main()
