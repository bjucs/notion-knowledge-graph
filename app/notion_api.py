import requests
import os
from dotenv import load_dotenv

# Load API key and root page ID
load_dotenv()
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
ROOT_PAGE_ID = os.getenv("NOTION_PAGE_ID")  # Start from a known page

HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

"""Fetch all child blocks (paragraphs, sub-pages, etc.) from a Notion page"""
def fetch_page_blocks(page_id: str) -> dict:
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        return {"error": f"Failed to fetch page {page_id}. Status: {response.status_code}"}

    return response.json()

"""Extract links to other Notion pages from block responses"""
def extract_page_links(blocks_data):
    linked_pages = []

    for block in blocks_data.get("results", []):
        if block["type"] == "child_page":
            linked_pages.append(block["id"])
        elif block["type"] == "link_to_page":
            linked_page_id = block.get("link_to_page", {}).get("page_id")
            if linked_page_id:
                linked_pages.append(linked_page_id)

    return linked_pages

"""Recursively finds all pages linked from the root page, avoiding duplicate API calls"""
def fetch_all_pages(root_page_id: str) -> list:
    visited = set()
    cache = {}  

    def dfs(page_id: str):
        if page_id in visited:
            return
        
        visited.add(page_id)
        if page_id not in cache:  
            cache[page_id] = fetch_page_blocks(page_id)

        linked_pages = extract_page_links(cache[page_id])

        for linked_id in linked_pages:
            dfs(linked_id)

    dfs(root_page_id)
    return list(visited)


