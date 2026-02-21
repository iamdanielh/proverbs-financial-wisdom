# TOOLS.md - Local Notes

## Authentication
- **Sudo password:** 170417 (stored in ~/.sudo_password, chmod 600)
- Use: `cat ~/.sudo_password | sudo -S [command]`

## Installed Tools

### jq 1.7
**Use for:** JSON filtering, extraction, transformation
**Examples:**
```bash
jq '.' file.json                    # Pretty print
jq '.chapters[].title' book.json    # Extract titles
jq '.chapters | sort_by(.count)'    # Sort
jq 'select(.active == true)'        # Filter
```

### fzf 0.44  
**Use for:** Fuzzy file finding, history search
**Examples:**
```bash
fzf                                 # Interactive file find
history | fzf                       # Search history
find . -name "*.py" | fzf          # Filter Python files
```

### Web Search
**Current:** web_fetch for single URLs
**Limitation:** No bulk web search without API keys
**Alternatives:**
- SearXNG: Needs Docker (not available)
- DuckDuckGo library: Needs pip (not available)
- Brave API: Needs signup/key

### ClawHub
**Installed skills:**
- github — Repo management
- desearch-web-search — Requires API key
- sonoscli — Sonos speaker control
