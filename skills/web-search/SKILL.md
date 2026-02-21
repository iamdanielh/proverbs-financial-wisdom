# Web Search via SearXNG

## What It Is
Self-hosted metasearch engine running on Docker.
Aggregates results from multiple search engines without tracking.

## Installation
```bash
# Already installed via Docker
sudo docker run -d \
  --name searxng \
  -p 8080:8080 \
  -v ~/.openclaw/workspace/searxng:/etc/searxng \
  -e BASE_URL=http://192.168.1.113:8080/ \
  searxng/searxng:latest
```

## Usage

### Via Browser
http://192.168.1.113:8080

### Via API (curl)
```bash
# JSON results
curl "http://192.168.1.113:8080/search?q=YOUR+QUERY&format=json"

# HTML results
curl "http://192.168.1.113:8080/search?q=YOUR+QUERY"
```

### Via Python
```python
import requests

def search(query):
    url = "http://localhost:8080/search"
    params = {"q": query, "format": "json"}
    return requests.get(url, params=params).json()
```

## Status
✅ Running at http://192.168.1.113:8080
✅ Container: searxng (Docker)
✅ No API keys needed - completely free

## Proverbs Viewer
Moved to port 8081: http://192.168.1.113:8081/proverbs_complete.html

## Sources
SearXNG queries multiple engines:
- DuckDuckGo
- Bing
- Google (if enabled)
- Wikipedia
- And more...
