import requests
import json

# Test root endpoint
try:
    response = requests.get('http://localhost:5000/')
    print(f"Root endpoint status: {response.status_code}")
    print(f"Root endpoint content: {response.text}")
except Exception as e:
    print(f"Error accessing root endpoint: {e}")

# Test pipeline list endpoint
try:
    response = requests.post('http://localhost:5000/pl/list', json={"name": ""})
    print(f"Pipeline list endpoint status: {response.status_code}")
    print(f"Pipeline list endpoint content: {response.text}")
except Exception as e:
    print(f"Error accessing pipeline list endpoint: {e}")

# Test if we can directly read the pl.json file
try:
    with open('data/pl.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        print(f"Successfully read pl.json file")
        print(f"Number of pipelines: {len(data) if isinstance(data, list) else 'not a list'}")
except Exception as e:
    print(f"Error reading pl.json file: {e}")