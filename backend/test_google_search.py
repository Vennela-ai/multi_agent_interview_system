import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY")
SEARCH_ENGINE_ID = os.getenv("GOOGLE_SEARCH_ENGINE_ID")

if not API_KEY:
    raise ValueError("GOOGLE_SEARCH_API_KEY not found")

if not SEARCH_ENGINE_ID:
    raise ValueError("GOOGLE_SEARCH_ENGINE_ID not found")


query = "Python Developer interview questions"

url = "https://www.googleapis.com/customsearch/v1"

params = {
    "key": API_KEY,
    "cx": SEARCH_ENGINE_ID,
    "q": query,
    "num": 10
}

response = requests.get(
    url,
    params=params,
    timeout=30
)

print("Status code:", response.status_code)

data = response.json()

if response.status_code != 200:
    print("\nERROR:")
    print(data)
    exit()

print("\n========== SEARCH RESULTS ==========\n")

for item in data.get("items", []):
    print("TITLE:", item.get("title"))
    print("URL:", item.get("link"))
    print("SNIPPET:", item.get("snippet"))
    print("-" * 80)