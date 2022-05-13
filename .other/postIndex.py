import requests
import sys
import base64
import pprint

GITHUB_API_URL = 'https://api.github.com'
GITHUB_TOKEN = sys.argv[-2]
GITHUB_TOKEN = GITHUB_TOKEN.encode('utf-8')
GITHUB_TOKEN = b'x-access-token:'+GITHUB_TOKEN
GITHUB_TOKEN = base64.b64decode(GITHUB_TOKEN)
GITHUB_TOKEN = GITHUB_TOKEN.decode('utf-8')
INDEX_PATH = sys.argv[-1]

s = requests.Session()
s.headers.update({'Accept': 'application/vnd.github.v3+json'})
s.headers.update({'User-Agent': 'Mozilla/5.0 TES286/1.0'})
s.headers.update({'Authorization': 'basic ' + GITHUB_TOKEN})

def api(method, url, **kwargs):
    url = GITHUB_API_URL + url
    return s.request(method, url, **kwargs)

def postIndex(indexPath):
    with open(indexPath, 'rb') as f:
        data = {'message': 'Upgrade Index', 'content': base64.b64encode(f.read()).decode('ascii')}
        r = api('PUT', '/repos/TES286-ghpages/files-index.tes286.site/contents/index.json', json=data)
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        try:
            pprint.pprint(r.json())
        except:
            print(r.text)
        raise e

    return r

def main():
    r = postIndex(INDEX_PATH)
    try:
        pprint.pprint(r.json())
    except:
        print(r.text)

if __name__ == '__main__':
    main()