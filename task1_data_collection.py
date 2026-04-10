import os
import json
import requests
from datetime import datetime

print("Program started successfully")

# -------------------------------
# Create folder if not exists
# -------------------------------
os.makedirs("data", exist_ok=True)

# -------------------------------
# Hacker News API URLs
# -------------------------------
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"

try:
    response = requests.get(TOP_STORIES_URL)
    story_ids = response.json()
except Exception as e:
    print("Error fetching top stories:", e)
    story_ids = []

stories = []
count = 0

# -------------------------------
# Fetch 100 stories
# -------------------------------
for story_id in story_ids[:100]:

    try:
        item_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        item = requests.get(item_url).json()

        if not item:
            continue

        story = {
            "post_id": item.get("id"),
            "title": item.get("title"),
            "category": "news",
            "score": item.get("score", 0),
            "num_comments": item.get("descendants", 0),
            "author": item.get("by", "unknown"),
            "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        stories.append(story)
        count += 1

    except Exception as e:
        print(f"Skipping story {story_id} due to error:", e)

# -------------------------------
# Save JSON file
# -------------------------------
output_path = "data/trends.json"

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(stories, f, indent=4)

# -------------------------------
# Final output message
# -------------------------------
print(f"Collected {count} stories, saved to {output_path}")