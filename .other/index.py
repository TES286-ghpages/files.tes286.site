import json
import os
import shutil
import sys
import time

import requests

# Constants
GITHUB_API_URL = "https://api.github.com"
GITHUB_REPO = "TES286-ghpages/files.tes286.site"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
TOTAL_SIZE = 0

s = requests.Session()


def get(url, headers):
    print(f"GET {url}")
    if not GITHUB_TOKEN:
        del headers["Authorization"]
    r = s.get(
        url,
        headers=headers
    )
    if r.ok:
        return r
    else:
        print(f"Error: {r.status_code} on {url}")
        print(f"Response: {r.text}")
        sys.exit(1)


def getRoot():
    return get(
        f"{GITHUB_API_URL}/repos/{GITHUB_REPO}/contents",
        headers={
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }
    ).json()


def getChildren(url):
    children = []
    data = get(url, headers={
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }).json()
    for item in data:
        if item["name"].startswith(".") or item["name"].startswith("_") or item["name"] == "CNAME" or item["name"].endswith(".html"):
            print(f"Skipping {item['name']}")
            continue
        if item["type"] == "dir":
            children.append({"name": item["name"], "type": "dir", "children": getChildren(
                item["url"]), "size": item["size"]})
        else:
            children.append({"name": item["name"], "type": "file", "size": item["size"],
                            "url": "https://files.tes286.site/" + item["path"]})
    for i in children:
        if i["type"] == "dir":
            i["size"] = sum(x["size"] for x in i["children"])
    return children


def build_index():
    index = []
    root = getRoot()
    for item in root:
        if item["name"].startswith(".") or item["name"].startswith("_") or item["name"] == "CNAME" or item["name"].endswith(".html"):
            print(f"Skipping {item['type']} {item['name']}")
            continue
        if item["type"] == "dir":
            index.append({"name": item["name"], "type": "dir", "children": getChildren(
                item["url"]), "size": item["size"]})
        else:
            index.append({"name": item["name"], "type": "file", "size": item["size"],
                         "url": "https://files.tes286.site/" + item["path"]})
    for i in index:
        if i["type"] == "dir":
            i["size"] = sum(x["size"] for x in i["children"])
    TOTAL_SIZE = sum(x["size"] for x in index)
    index.sort(key=lambda x: x["name"])
    final_index = {
        "index": index,
        "total_size": TOTAL_SIZE,
        "last_updated": int(time.time())
    }
    with open("index.json", "w") as f:
        json.dump(final_index, f)


if __name__ == "__main__":
    build_index()
    print(f"Total size: {TOTAL_SIZE}")
    print(f"Last updated: {time.ctime(int(time.time()))}")
    print("Done!")
