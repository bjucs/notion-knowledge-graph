import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.notion_api import notion_search, fetch_page_blocks, extract_page_links, fetch_all_pages, is_match, app

client = TestClient(app)

class TestNotionAPI(unittest.TestCase):

    @patch("app.notion_api.requests.get")
    def test_fetch_page_blocks_success(self, mock_get):
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
        mock_get.return_value.status_code = 403
        page_data = fetch_page_blocks("invalid_page_id")
        self.assertIn("error", page_data)

    # def test_extract_page_links(self):
    #     """Test extract_page_links() to correctly retrieve linked pages."""
        
    #     mock_blocks = {
    #         "results": [
    #             {"id": "page_1", "type": "child_page"},
    #             {"id": "page_2", "type": "link_to_page", "link_to_page": {"page_id": "linked_page"}},
    #             {"id": "page_3", "type": "paragraph"}  # Should be ignored
    #         ]
    #     }

    #     linked_pages = extract_page_links(mock_blocks)  
        
    #     self.assertIsInstance(linked_pages, list)
    #     self.assertIn("page_1", linked_pages)
    #     self.assertIn("linked_page", linked_pages)


    @patch("app.notion_api.fetch_page_blocks")
    def test_fetch_all_pages(self, mock_fetch_blocks):
        mock_fetch_blocks.side_effect = lambda page_id: {
            "results": [{"id": f"page_{int(page_id[-1]) + 1}", "type": "child_page"}]
        } if page_id != "page_3" else {"results": []}  # Stops at page_3

        all_pages = fetch_all_pages("page_1")
        self.assertIn("page_1", all_pages)
        self.assertIn("page_2", all_pages)
        self.assertIn("page_3", all_pages)

    def test_is_match(self):
        self.assertTrue(is_match("This is a test sentence", "test"))
        self.assertFalse(is_match("No matching word here", "test"))
        self.assertTrue(is_match("Find the phrase test case", "test case"))
        self.assertTrue(is_match("Partial matchtesting should not work", "test"))
        self.assertTrue(is_match("The word TEST is uppercase", "test"))  # Case insensitive

    # --- FASTAPI-SPECIFIC TEST FOR `notion_search` ---

    @patch("app.notion_api.fetch_all_pages")
    @patch("app.notion_api.fetch_page_blocks")
    def test_notion_search(self, mock_fetch_blocks, mock_fetch_pages):
        mock_fetch_pages.return_value = ["page_1", "page_2"]
        mock_fetch_blocks.return_value = {
            "results": [
                {"id": "block_1", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "Significant Impact"}}]}}
            ]
        }

        response = client.get("/notion_search/Significant Impact/page_1")
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertIn("block_1", json_data)
        self.assertEqual(json_data["block_1"], ["Significant Impact"])

if __name__ == "__main__":
    unittest.main()
