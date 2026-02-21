import json
import re

# Load the source data
with open('proverbs-wisdom-units-FINAL.json') as f:
    data = json.load(f)

units = data['units']

# Build complete book with all verses
book = {
    'title': 'Proverbs: Financial Wisdom - All 313 Verses',
    'total_units': len(units),
    'chapters': []
}

# Chapter definitions with theme-based sorting
chapter_defs = {
    1: {'title': 'The Foundation: Fear of God', 'color': '#1a237e', 'icon': '🏛️'},
    2: {'title': 'Active Pursuit: Seek Wisdom', 'color': '#00695c', 'icon': '⚒️'},
    3: {'title': 'Diligence: Work vs Laziness', 'color': '#c62828', 'icon': '💤'},
    4: {'title': 'Planning: Counsel and Strategy', 'color': '#455a64', 'icon': '🪶'},
    5: {'title': 'Patience: No Quick Riches', 'color': '#e65100', 'icon': '⚡'},
    6: {'title': 'Debt: Never Sign What You Cannot Pay', 'color': '#b71c1c', 'icon': '⛓️'},
    7: {'title': 'Generosity: Give First, Receive More', 'color': '#2e7d32', 'icon': '💧'},
    8: {'title': 'Reserves: Build Barns Before Need', 'color': '#f57c00', 'icon': '📦'},
    9: {'title': "Wisdom's Value: Better Than Gold", 'color': '#6a1b9a', 'icon': '💎'},
    10: {'title': 'Integrity: Honest Scales', 'color': '#37474f', 'icon': '⚖️'},
    11: {'title': 'Legacy: Build for the Next Generation', 'color': '#5d4037', 'icon': '🌳'},
    12: {'title': 'Fairness: Pay Promptly, Work Faithfully', 'color': '#00796b', 'icon': '💵'}
}

# Theme-based keywords for sorting
theme_keywords = {
    1: ['fear of yahweh', 'beginning of wisdom', 'foundation'],
    2: ['seek', 'treasure', 'silver', 'gold', 'search'],
    3: ['sluggard', 'lazy', 'diligent', 'hand', 'ant'],
    4: ['counsel', 'plans', 'advice', 'guidance'],
    5: ['haste', 'quick', 'ill-gotten', 'dwindles'],
    6: ['surety', 'pledge', 'stranger', 'borrower'],
    7: ['give', 'generous', 'firstfruits', 'honor'],
    8: ['store', 'barn', 'reserve', 'gather'],
    9: ['better than', 'than gold', 'precious'],
    10: ['scale', 'weight', 'measure', 'abomination'],
    11: ['inheritance', 'children', 'grandchildren'],
    12: ['worker', 'wages', 'laborer', 'poor', 'needy']
}

# Sort units into chapters
chapter_units = {i: [] for i in range(1, 13)}

for unit in units:
    text = unit['text'].lower()
    cat = unit.get('primary_category', '').lower()
    chap = unit['chapter']
    
    # Determine best chapter by keywords and category
    best_match = 1
    best_score = 0
    
    # Category mapping
    if 'debt' in cat or 'surety' in cat:
        best_match = 6
    elif 'diligence' in cat:
        best_match = 3
    elif 'laziness' in cat or 'sluggard' in cat:
        best_match = 3
    elif 'generosity' in cat or 'giving' in cat:
        best_match = 7
    elif 'strategic planning' in cat or 'counsel' in cat:
        best_match = 4
    elif 'just dealing' in cat or 'integrity' in cat:
        best_match = 10
    elif 'inheritance' in cat:
        best_match = 11
    elif 'poverty' in cat:
        # Check if about fair wages or oppression
        if 'labor' in text or 'worker' in text or 'wages' in text:
            best_match = 12
        else:
            best_match = 3  # Laziness leads to poverty
    elif 'wealth' in cat:
        if 'better than' in text or 'gold' in text:
            best_match = 9
        else:
            best_match = 1
    elif 'treasure' in cat:
        best_match = 2
    elif 'provision' in cat:
        best_match = 8
    elif 'greed' in cat or 'quick' in text:
        best_match = 5
    elif chap <= 12:
        best_match = chap
    
    # Refine by keyword scoring
    for ch_num, keywords in theme_keywords.items():
        score = sum(3 for kw in keywords if kw in text)
        if score > best_score:
            best_score = score
            best_match = ch_num
    
    chapter_units[best_match].append(unit)

# Build chapters
for ch_num in range(1, 13):
    defs = chapter_defs[ch_num]
    units_in_chap = chapter_units[ch_num]
    
    # Sort by verse reference
    def sort_key(u):
        parts = u['reference'].replace('Proverbs ', '').split(':')
        return (int(parts[0]), int(parts[1].split('-')[0]))
    
    units_in_chap.sort(key=sort_key)
    
    sections = []
    for unit in units_in_chap:
        sections.append({
            'range': unit['reference'].replace('Proverbs ', ''),
            'title': unit.get('themes', [unit['primary_category']])[0] if unit.get('themes') else unit['primary_category'],
            'text': unit['text'],
            'summary': f"{unit['primary_category']}",
            'financial_concepts': [unit['primary_category']] + unit.get('secondary_categories', [])
        })
    
    book['chapters'].append({
        'chapter': ch_num,
        'title': defs['title'],
        'section_count': len(sections),
        'color': defs['color'],
        'icon': defs['icon'],
        'sections': sections
    })
    
    print(f"Chapter {ch_num}: {defs['title']} - {len(sections)} sections")

# Save
with open('proverbs_complete_book.json', 'w') as f:
    json.dump(book, f, indent=2)

print(f"\nTotal: {sum(ch['section_count'] for ch in book['chapters'])} sections in 12 chapters")
