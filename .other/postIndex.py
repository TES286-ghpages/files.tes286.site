import requests
import sys
import base64
import pprint

GITHUB_API_URL = 'https://api.github.com'
GITHUB_TOKEN = sys.stdin.readline()
INDEX_PATH = sys.argv[-1]

s = requests.Session()
s.headers.update({'Accept': 'application/vnd.github.v3+json'})
s.headers.update({'User-Agent': 'Mozilla/5.0 TES286/1.0'})
s.headers.update({'Authorization': 'token ' + GITHUB_TOKEN})

def api(method, url, **kwargs):
    url = GITHUB_API_URL + url
    return s.request(method, url, **kwargs)

def postIndex(indexPath):
    with open(indexPath, 'rb') as f:
        data = {'message': 'Upgrade Index', 'content': base64.b64encode(f.read()).decode('ascii')}
        r = api('POST', '/repos/TES286-ghpages/files-index.tes286.site/contents/index.json', json=data)
    r.raise_for_status()
    return r

def main():
    r = postIndex(INDEX_PATH)
    try:
        pprint.pprint(r.json())
    except:
        print(r.text)
