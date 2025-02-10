import json
import requests
from notion_client import Client
from config import load_config
from ollama_api import call_ollama_api
from notion_api import update_notion_page, fetch_notion_data

def main():
    config = load_config()
    notion_api_key = config['NOTION_API_KEY']
    database_id = config['NOTION_DATABASE_ID']
    ollama_api = config['OLLAMA_API_URL']
    model = config['OLLAMA_MODEL']
    
    notion = Client(auth=notion_api_key)
    notion_data = fetch_notion_data(notion, database_id)
    
    for item in notion_data:
        page_id = item['id']
        properties = item.get('properties', {})
        english_word = properties.get('English', {}).get('title', [{}])[0].get('text', {}).get('content', '')
        
        if english_word:
            prompt = f"Translate this English word to French: {english_word}. Provide only the translation."
            translation = call_ollama_api(prompt, ollama_api, model)
            if translation:
                update_notion_page(notion, page_id, "French", translation)
                print(f"Updated {english_word} -> {translation}")

if __name__ == "__main__":
    main()
