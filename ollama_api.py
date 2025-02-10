import json
import re
import requests

def call_ollama_api(prompt, ollama_api, model, keep_thinking_process=False):
    """Call Ollama API with a given prompt and handle streaming JSON."""
    headers = {'Content-Type': 'application/json'}
    data = json.dumps({
        "model": model,
        "prompt": prompt
    })

    response = requests.post(ollama_api, headers=headers, data=data, stream=True)

    if response.status_code == 200:
        translation = ""
        try:
            for line in response.iter_lines():
                if line:
                    json_data = json.loads(line.decode('utf-8'))
                    if "response" in json_data:
                        translation += json_data["response"]
                    if json_data.get("done", False):
                        break
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
            return None

        # Remove everything between <think> and </think> if keep_thinking_process is False
        if not keep_thinking_process:
            translation = re.sub(r"<think>.*?</think>", "", translation, flags=re.DOTALL).strip()
        
        return translation.strip()
    else:
        print(f"Ollama API error: {response.text}")
        return None

if __name__ == "__main__":
    ollama_api_url = "http://localhost:11434/api/generate"
    model_name = "deepseek-r1:14b"
    test_prompt = "Translate 'hello' to Chinese"
    
    # Test both options
    result_with_thinking = call_ollama_api(test_prompt, ollama_api_url, model_name, keep_thinking_process=True)
    print(f"With Thinking Process: {result_with_thinking}")
    
    print('------------------------------------')
    
    result_without_thinking = call_ollama_api(test_prompt, ollama_api_url, model_name, keep_thinking_process=False)
    print(f"Without Thinking Process: {result_without_thinking}")
