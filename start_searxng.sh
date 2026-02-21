#!/bin/bash
# Start SearXNG on port 8080
# Proverbs viewer moved to port 8081

sudo docker run -d \
  --name searxng \
  -p 8080:8080 \
  -v "${HOME}/.openclaw/workspace/searxng:/etc/searxng" \
  -e "BASE_URL=http://localhost:8080/" \
  searxng/searxng:latest

echo "SearXNG starting on http://localhost:8080"
echo "Proverbs viewer will be on http://localhost:8081"
