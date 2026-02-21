#!/bin/bash
pkill -f serve_proverbs.py 2>/dev/null
sleep 1
cd /home/dangel/.openclaw/workspace
python3 serve_proverbs.py &
sleep 2
curl -s http://192.168.1.113:8080/proverbs_full.html -o /dev/null -w "%{http_code}"
