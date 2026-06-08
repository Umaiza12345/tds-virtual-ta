import requests
import json
import time

cookies = {}

BASE_URL = "https://discourse.onlinedegree.iitm.ac.in"

response = requests.get(
    f"{BASE_URL}/c/courses/tds-kb/34.json",
    cookies=cookies,
    verify=False
)


data = response.json()

print(data.keys())
topics = data["topic_list"]["topics"]

print("Found topics:", len(topics))

print("First topic title:", topics[0]["title"])

all_posts = []

for topic in topics:
    topic_id = topic["id"]
    slug = topic["slug"]

    topic_url = f"{BASE_URL}/t/{slug}/{topic_id}.json"

    try:
        r = requests.get(
            topic_url,
            cookies=cookies,
            verify=False
        )

        topic_data = r.json()

        content = "\n".join(
            post.get("cooked", "")
            for post in topic_data["post_stream"]["posts"]
        )

        all_posts.append({
            "title": topic_data["title"],
            "url": f"{BASE_URL}/t/{slug}/{topic_id}",
            "content": content
        })

        print("Saved:", topic_data["title"])

        time.sleep(1)

    except Exception as e:
        print("Failed:", topic_id, e)

with open("discourse_data.json", "w", encoding="utf-8") as f:
    json.dump(all_posts, f, indent=2, ensure_ascii=False)

print(f"\nSaved {len(all_posts)} topics")