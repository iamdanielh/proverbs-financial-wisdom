#!/usr/bin/env python3
"""Efficient Proverbs thematic analysis."""
import csv
import json
import re
from collections import defaultdict

def load_proverbs():
    verses = []
    with open('/tmp/proverbs.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 2:
                ref = row[0].strip()
                text = row[1].strip()
                match = re.match(r'Proverbs (\d+):(\d+)', ref)
                if match:
                    chapter = int(match.group(1))
                    verse = int(match.group(2))
                    verses.append({'chapter': chapter, 'verse': verse, 'text': text})
    return verses

def extract_financial_concepts(text):
    text_lower = text.lower()
    concepts = []
    
    mappings = {
        'treasure/precious goods': ['silver', 'gold', 'rubies', 'jewels', 'coral', 'pearls', 'treasure', 'costly'],
        'wealth/riches': ['riches', 'rich', 'wealth', 'wealthy', 'abundance', 'prosperity'],
        'poverty/need': ['poor', 'poverty', 'needy', 'want', 'lack'],
        'debt/borrowing': ['debt', 'borrow', 'lend', 'lender', 'creditor', 'surety', 'pawns', 'strikes hands'],
        'wages/work income': ['wages', 'labor', 'toil', 'work', 'worker', 'hireling', 'harvest', 'reap', 'sow'],
        'inheritance/legacy': ['inherit', 'inheritance', 'fathers', 'grandchildren', 'house', 'children'],
        'provision/storage': ['barns', 'grain', 'food', 'store', 'fields', 'vineyard', 'plenty'],
        'generosity/giving': ['give', 'gift', 'generous', 'openhanded', 'firstfruits', 'honor yahweh', 'substance', 'increase'],
        'trade/commerce': ['buy', 'sell', 'merchant', 'trade', 'price', 'gain', 'profit'],
        'dishonest gain': ['dishonest', 'false', 'deceitful', 'ill-gotten', 'stolen', 'fraud'],
        'strategic planning': ['plan', 'counsel', 'advice', 'guidance', 'wise dealing'],
        'diligence/industry': ['diligent', 'diligence', 'hand', 'industrious', 'skillful', 'excellent'],
        'laziness/poverty': ['sluggard', 'lazy', 'sleep', 'slothful', 'idle', 'folds hands'],
        'greed/covetousness': ['greedy', 'greed', 'gain', 'quick', 'hurry', 'chase', 'ill-gotten'],
        'just dealing': ['just', 'justice', 'fair', 'honest', 'integrity', 'righteous', 'equity'],
        'stewardship': ['rule', 'manage', 'household', 'servants', 'leaders', 'throne'],
    }
    
    for concept, terms in mappings.items():
        if any(t in text_lower for t in terms):
            concepts.append(concept)
    
    return concepts[:3]  # Limit to top 3

def generate_summary(verses, full_text):
    first = verses[0]['text'][:60]
    
    # Pattern-based summaries
    if 'my son' in full_text.lower() and 'listen' in full_text.lower():
        return "Fatherly instruction on acquiring and maintaining wisdom"
    if 'wisdom calls' in full_text.lower():
        return "Wisdom personified calling out to the simple and scoffers"
    if 'sluggard' in full_text.lower() or 'lazy' in full_text.lower():
        return "Contrast between diligent and lazy approaches to work and provision"
    if 'strange woman' in full_text.lower() or 'adulteress' in full_text.lower():
        return "Warning against sexual immorality with consequences"
    if 'ant' in full_text.lower() or 'conies' in full_text.lower():
        return "Lessons from creatures demonstrating wisdom and industry"
    if 'king' in full_text.lower() and 'yahweh' in full_text.lower():
        return "Divine principles for leadership and governance"
    if 'who can find' in full_text.lower():
        return "Acrostic poem praising the virtuous wife"
    if len(verses) == 1:
        return f"Standalone wisdom on: {first[:50]}..."
    
    return "Thematic unit on practical wisdom"

def main():
    print("Loading Proverbs...")
    verses = load_proverbs()
    
    chapters = defaultdict(list)
    for v in verses:
        chapters[v['chapter']].append(v)
    
    output = {"chapters": [], "stats": {"total_verses": len(verses)}}
    
    for ch_num in sorted(chapters.keys()):
        ch_verses = chapters[ch_num]
        
        # Simple split: every 2-6 verses, or on "My son", or major breaks
        sections = []
        current = [ch_verses[0]]
        
        for v in ch_verses[1:]:
            text = v['text']
            
            # Break on new instruction
            if text.startswith('My son') or text.startswith('Listen') or text.startswith('Go to'):
                if len(current) > 0:
                    sections.append(current)
                current = [v]
            # Break on personification
            elif 'Wisdom calls' in text or 'Wisdom has built' in text:
                if len(current) > 0:
                    sections.append(current)
                current = [v]
            # Break every 4-5 verses naturally
            elif len(current) >= 5:
                sections.append(current)
                current = [v]
            else:
                current.append(v)
        
        if current:
            sections.append(current)
        
        # Build chapter object
        ch_sections = []
        for sec in sections:
            start = f"{sec[0]['chapter']}:{sec[0]['verse']}"
            end = f"{sec[-1]['chapter']}:{sec[-1]['verse']}"
            verse_range = start if start == end else f"{sec[0]['chapter']}:{sec[0]['verse']}-{sec[-1]['verse']}"
            full_text = ' '.join([v['text'] for v in sec])
            
            # Title from first verse
            first_words = sec[0]['text'][:40].replace('My son,', 'Instruction:')
            title = first_words.split('.')[0] + ('...' if len(first_words) > 30 else '')
            
            ch_sections.append({
                "range": verse_range,
                "title": title,
                "text": full_text,
                "summary": generate_summary(sec, full_text),
                "financial_concepts": extract_financial_concepts(full_text)
            })
        
        output["chapters"].append({
            "chapter": ch_num,
            "sections": ch_sections
        })
    
    # Add section count to stats
    total_sections = sum(len(ch['sections']) for ch in output['chapters'])
    output['stats']['total_sections'] = total_sections
    output['stats']['chapters'] = len(output['chapters'])
    
    # Save
    with open('/home/dangel/.openclaw/workspace/proverbs_thematic_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"Done! {len(output['chapters'])} chapters, {total_sections} sections, {len(verses)} verses.")

if __name__ == '__main__':
    main()
