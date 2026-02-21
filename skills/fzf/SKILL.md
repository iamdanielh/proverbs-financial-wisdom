# fzf - Fuzzy Finder

## What It Is
Interactive filter for any list. Fast fuzzy search in terminal.

## Installation
```bash
# Ubuntu/Debian
sudo apt-get install fzf

# macOS
brew install fzf

# Manual (no sudo)
git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
~/.fzf/install
```

## Common Use Cases

### 1. File Finding
```bash
# Find file interactively
find . -name "*.json" | fzf

# Edit file found
vim $(fzf)
```

### 2. Command History Search
```bash
# Search bash history
history | fzf

# Bind to Ctrl+R (in .bashrc)
eval "$(fzf --bash)"
```

### 3. Directory Navigation
```bash
# Change to directory found
cd $(find ~ -type d | fzf)
```

### 4. Git Integration
```bash
# Checkout branch
git checkout $(git branch | fzf)

# View commit
git show $(git log --oneline | fzf | cut -d' ' -f1)
```

## Python Integration
```python
# Use fzf in Python scripts
import subprocess

def select_file():
    result = subprocess.run(['fzf'], input='\n'.join(files), 
                          capture_output=True, text=True)
    return result.stdout.strip()
```

## Current Status
**✅ INSTALLED** - fzf 0.44.1 ready to use

## Quick Test
```bash
# List all JSON files interactively
find ~/.openclaw/workspace -name "*.json" | fzf

# Search command history
history | fzf
```

## Integration
Ready for shell use. Add to .bashrc for Ctrl+R history search:
```bash
eval "$(fzf --bash)"
```