import requests
import os
import sys
from dotenv import load_dotenv

load_dotenv()
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
ROOT_PAGE_ID = os.getenv("NOTION_PAGE_ID")  

log_file = open("notion_api.log", "w")
sys.stdout = log_file

HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

"""Fetch all child blocks (paragraphs, sub-pages, etc.) from a Notion page"""
def fetch_page_blocks(page_id: str) -> dict:
    url = f"https://api.notion.com/v1/blocks/{page_id}/children/"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        return {"error": f"Failed to fetch page {page_id}. Status: {response.status_code}"}

    return response.json()

"""Fetch all pages from a Notion database"""
def fetch_database_pages(database_id: str) -> list:
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    response = requests.post(url, headers=HEADERS, json={})

    if response.status_code != 200:
        print(f"ERROR: Failed to fetch database {database_id}. Status: {response.status_code}")
        return []

    data = response.json()
    page_ids = {page["id"] for page in data.get("results", [])} 
    return list(page_ids)

"""Extract links to other Notion pages from block responses"""
def extract_page_links(blocks_data):
    linked_pages = set()  

    print("\n📌 DEBUG: Checking blocks...")
    for block in blocks_data.get("results", []):
        block_id = block["id"]
        block_type = block["type"]
        print(f"➡️ Block: {block_id}, Type: {block_type}")

        if block_type == "child_page":
            linked_pages.add(block_id)
            print(f"✅ Found child_page: {block_id}")

        elif block_type == "link_to_page":
            linked_page_id = block.get("link_to_page", {}).get("page_id")
            if linked_page_id:
                linked_pages.add(linked_page_id)
                print(f"✅ Found link_to_page: {linked_page_id}")

        elif block_type == "column_list":
            columns = fetch_page_blocks(block_id)
            for column in columns.get("results", []):
                if column["type"] == "column" and column["has_children"]:
                    print(f"🔍 Found column, fetching child blocks...")
                    column_blocks = fetch_page_blocks(column["id"])
                    linked_pages.update(extract_page_links(column_blocks))

        elif block_type == "child_database":
            print(f"📂 Found child_database: {block_id}, fetching pages inside...")
            db_pages = fetch_database_pages(block_id)
            linked_pages.update(db_pages)

        elif block["has_children"]:
            print(f"🔄 Fetching child blocks inside {block_type}...")
            child_blocks = fetch_page_blocks(block_id)
            linked_pages.update(extract_page_links(child_blocks))

    return list(linked_pages) 

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

        # Filter out already visited pages before recursion
        new_pages = [pid for pid in linked_pages if pid not in visited]
        
        for linked_id in new_pages:
            dfs(linked_id)

    dfs(root_page_id)
    return list(visited)

if __name__ == "__main__":
    print("🔍 Testing Notion API connection...")

    if not NOTION_API_KEY:
        print("ERROR: NOTION_API_KEY is missing! Check your .env file.")
    elif not ROOT_PAGE_ID:
        print("ERROR: NOTION_PAGE_ID is missing! Check your .env file.")
    else:
        response = fetch_page_blocks(ROOT_PAGE_ID)
        print("API Response:", response)
        print("All pages:", fetch_all_pages(ROOT_PAGE_ID))
    
    sys.stdout = sys.__stdout__
    log_file.close()

