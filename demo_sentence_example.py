from notion_client import Client
from ollama_api import call_ollama_api

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

def generate_sentence_example(word, ollama_api, model):
    """Generate a short, simple, and clear English sentence using the vocabulary word via Ollama API."""
    prompt = f"Provide only a short, clear, and easy-to-memorize English sentence using the word '{word}' without any explanations or additional text."
    return call_ollama_api(prompt, ollama_api, model)

if __name__ == "__main__":
    import json
    from config import load_config
    
    config = load_config()
    notion_api_key = config['NOTION_API_KEY']
    database_id = config['NOTION_DATABASE_ID']
    ollama_api_url = config['OLLAMA_API_URL']
    model_name = config['OLLAMA_MODEL']
    
    notion = Client(auth=notion_api_key)
    
    # Fetch data from Notion
    print("Fetching Notion data...")
    notion_data = fetch_notion_data(notion, database_id)
    print(f"Fetched {len(notion_data)} items.")
    
    # Iterate over all rows and update Sentence Example
    for item in notion_data:
        page_id = item['id']
        test_property = "Sentence Example"
        test_word = item['properties'].get('English', {}).get('title', [{}])[0].get('text', {}).get('content', '')
        if test_word:
            test_value = generate_sentence_example(test_word, ollama_api_url, model_name)
            print(f"Updating page {page_id} with {test_property}: {test_value}")
            update_notion_page(notion, page_id, test_property, test_value)
    
    print("All rows updated successfully!")
