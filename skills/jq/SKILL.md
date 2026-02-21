# jq - JSON Processing

## What It Is
Command-line JSON processor. Lightweight, fast alternative to Python for JSON manipulation.

## Installation
```bash
# Ubuntu/Debian
sudo apt-get install jq

# macOS
brew install jq
```

## ✅ Status: INSTALLED (jq 1.7)

## Common Use Cases

### 1. Pretty Print JSON
```bash
jq '.' proverbs_complete_book.json | head -20
```

### 2. Extract Fields
```bash
# Get all chapter titles
jq '.chapters[].title' proverbs_complete_book.json

# Count sections per chapter  
jq '.chapters[] | {chapter: .chapter, section_count: .section_count}'
```

### 3. Filter Arrays
```bash
# Find chapters with 30+ sections
jq '.chapters[] | select(.section_count > 30) | .title'

# Top 3 by section count
jq '.chapters | sort_by(.section_count) | reverse | .[:3]' proverbs_complete_book.json
```

### 4. Transform Data
```bash
# All verse ranges
jq '.chapters[].sections[].range' proverbs_complete_book.json | wc -l
# Output: 238

# Export specific fields
jq '.chapters[] | {num: .chapter, title: .title, sections: .section_count}'
```

## vs Python
| Task | jq | Python |
|------|----|--------|
| Quick peek | ✅ `.` | `json.load` |
| Field extraction | ✅ `.key` | `data['key']` |
| One-liners | ✅ | ❌ scripts |
| Complex logic | ❌ | ✅ |

## Integration
- Terminal: Direct use
- Python: `subprocess.run(['jq', '.'], input=json_str)`
