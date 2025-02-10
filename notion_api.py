from notion_client import Client

def fetch_notion_data(notion, database_id):
    """Fetch vocabulary words from Notion database."""
    results = []
    response = notion.databases.query(database_id=database_id)
    results.extend(response.get('results', []))
    
    while response.get('has_more'):
        response = notion.databases.query(database_id=database_id, start_cursor=response['next_cursor'])
        results.extend(response.get('results', []))
    
    return results

def update_notion_page(notion, page_id, property_name, value):
    """Update a specific property of a Notion page."""
    notion.pages.update(
        page_id=page_id,
        properties={
            property_name: {
                "rich_text": [{"text": {"content": value}}]
            }
        }
    )

if __name__ == "__main__":
    import json
    from config import load_config
    
    config = load_config()
    notion_api_key = config['NOTION_API_KEY']
    database_id = config['NOTION_DATABASE_ID']
    
    notion = Client(auth=notion_api_key)
    
    # Test fetching data
    print("Fetching Notion data...")
    notion_data = fetch_notion_data(notion, database_id)
    print(json.dumps(notion_data, indent=2))
    
    # Test updating a page (assuming at least one result exists)
    if notion_data:
        test_page_id = notion_data[0]['id']
        test_property = "Chinese"
        test_value = "This should be updated"
        print(f"Updating page {test_page_id} with {test_property}: {test_value}")
        update_notion_page(notion, test_page_id, test_property, test_value)
        print("Update successful!")
