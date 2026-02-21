import json

# Load the source data (correct chapter assignments)
with open('proverbs-wisdom-units-FINAL.json') as f:
    data = json.load(f)

# Group by actual chapter
chapters = {i: [] for i in range(1, 32)}  # Proverbs has 31 chapters

for unit in data['units']:
    chap = unit['chapter']
    if chap in chapters:
        chapters[chap].append({
            'range': unit['reference'].replace('Proverbs ', ''),
            'title': unit.get('themes', ['Financial Wisdom'])[0] if unit.get('themes') else 'Financial Wisdom',
            'text': unit['text'],
            'summary': f"Thematic unit on {unit['primary_category']}",
            'financial_concepts': [unit['primary_category'].lower().replace(' & ', '/').replace(' ', '_')] + 
                                 [c.lower().replace(' & ', '/').replace(' ', '_') for c in unit.get('secondary_categories', [])]
        })

# Build final structure (only chapters 1-12 have content for now)
book_structure = {
    'book_title': 'Proverbs: Financial Wisdom by Chapter',
    'chapters': []
}

# Chapter titles based on actual content
chapter_titles = {
    1: 'Chapter 1: The Foundation of Wisdom',
    2: 'Chapter 2: Seek Wisdom as Treasure', 
    3: 'Chapter 3: Trust and Honor',
    4: 'Chapter 4: Guard Your Heart',
    5: 'Chapter 5: Avoid the Seductress',
    6: 'Chapter 6: Warnings and Instructions',
    7: 'Chapter 7: The Crafty Harlot',
    8: 'Chapter 8: Wisdom Calls Out',
    9: 'Chapter 9: Two Banquets',
    10: 'Chapter 10: The Way of Righteousness',
    11: 'Chapter 11: Honest Scales',
    12: 'Chapter 12: The Work of Hands'
}

for chap_num in range(1, 13):
    sections = chapters.get(chap_num, [])
    # Filter out any sections that don't belong (double check)
    sections = [s for s in sections if s['range'].startswith(f'{chap_num}:')]
    
    book_structure['chapters'].append({
        'chapter': chap_num,
        'title': chapter_titles.get(chap_num, f'Chapter {chap_num}'),
        'section_count': len(sections),
        'sections': sections
    })

# Save
with open('proverbs_by_chapter_fixed.json', 'w') as f:
    json.dump(book_structure, f, indent=2)

print(f"Fixed book structure with {len(book_structure['chapters'])} chapters")
for ch in book_structure['chapters']:
    print(f"  Chapter {ch['chapter']}: {ch['section_count']} sections")
    for s in ch['sections'][:3]:
        print(f"    - {s['range']}")
    if len(ch['sections']) > 3:
        print(f"    ... and {len(ch['sections'])-3} more")
