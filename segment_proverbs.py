#!/usr/bin/env python3
"""
Segment Proverbs into thematic sections with content-derived financial concepts.
"""

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
                    verses.append({
                        'ref': f"{chapter}:{verse}",
                        'chapter': chapter,
                        'verse': verse,
                        'text': text
                    })
    return verses

def extract_financial_concepts(text):
    """Content-derived financial concepts from text."""
    text_lower = text.lower()
    concepts = []
    
    # Explicit terms mapping
    explicit = {
        'treasure/precious': ['silver', 'gold', 'rubies', 'jewels', 'coral', 'pearls', 'hidden treasures', 'treasure'],
        'wealth/riches': ['riches', 'rich', 'wealthy', 'wealth', 'abundance', 'prosperity'],
        'poverty/need': ['poor', 'poverty', 'needy', 'want', 'lack'],
        'debt/borrowing': ['debt', 'borrow', 'lend', 'lender', 'creditor', 'co-sign', 'surety'],
        'wages/work': ['wages', 'labor', 'toil', 'work', 'worker', 'hireling'],
        'inheritance/legacy': ['inherit', 'inheritance', 'fathers', 'children', 'generations'],
        'provision/storage': ['barns', 'grain', 'food', 'store', 'harvest', 'fields', 'vineyard'],
        'generosity/giving': ['give', 'gift', 'generous', 'openhanded', 'alms', 'firstfruits'],
        'trade/commerce': ['buy', 'sell', 'merchant', 'trade', 'market', 'price'],
        'dishonest gain': ['dishonest', 'false', 'deceit', 'ill-gotten', 'stolen', 'fraud'],
        'planning': ['plan', 'counsel', 'advice', 'guidance', 'wisdom'],
        'diligence': ['diligent', 'diligence', 'industrious', 'sow', 'reap', 'plow'],
        'laziness': ['sluggard', 'lazy', 'sleep', 'slothful', 'idle', 'hand-folded'],
    }
    
    for concept, terms in explicit.items():
        if any(t in text_lower for t in terms):
            concepts.append(concept)
    
    # Implicit patterns
    if 'my son' in text_lower and any(x in text_lower for x in ['listen', 'instruction', 'teaching']):
        if not any(c in concepts for c in ['wages/work', 'generosity/giving']):
            pass  # skip generic
    
    # Greed/pursuit
    if any(x in text_lower for x in ['greedy', 'greed', 'gain', 'quick', 'hurry', 'chase']):
        concepts.append('greed/risky pursuit')
    
    # Justice/fair dealing
    if any(x in text_lower for x in ['just', 'justice', 'fair', 'honest', 'integrity', 'righteous']):
        concepts.append('just/equitable dealing')
    
    return list(set(concepts))

def detect_section_break(v, next_v=None):
    """Detect if verse starts a new thematic section."""
    text = v['text']
    
    # Strong breakers
    if text.startswith('My son'):
        return True
    if text.startswith('Listen, '):
        return True
    if text.startswith('The words of '):
        return True
    if text.startswith('Does not '):
        return True  
    if text.startswith('Who can find '):
        return True
    if text.startswith('Go to '):  # Wisdom's call
        return True
    
    # Wisdom personified speech
    if 'Wisdom calls' in text or 'Wisdom has built' in text:
        return True
    
    # Chapter nature verses
    if text.startswith('The') and 'is' in text and len(text) < 100:
        # Likely nature/descriptive verse
        pass
    
    return False

def segment_chapter(verses):
    """Split chapter into thematic sections."""
    sections = []
    current = [verses[0]]
    
    for i in range(1, len(verses)):
        v = verses[i]
        prev = verses[i-1]
        
        # Check for section break
        if detect_section_break(v):
            # Finish current section
            if len(current) >= 1:
                sections.append(current)
            current = [v]
        else:
            # Continue current section
            current.append(v)
        
        # Natural break: end of argument/couplet
        if len(current) >= 4:
            last_text = current[-1]['text']
            # If ends with conclusive statement and next might be new topic
            if i + 1 < len(verses):
                next_v = verses[i + 1]
                if detect_section_break(next_v):
                    sections.append(current)
                    current = []
    
    if current:
        sections.append(current)
    
    # Merge tiny sections (1-2 verses) with neighbors where possible
    merged = []
    for sec in sections:
        if len(sec) == 1 and merged:
            merged[-1].extend(sec)
        else:
            merged.append(sec)
    
    return merged if merged else sections

def generate_title(verses):
    """Generate section title from content."""
    first = verses[0]['text'][:50]
    full_text = ' '.join(v['text'] for v in verses)[:200].lower()
    
    # Specific patterns
    if 'my son' in first.lower():
        if 'strange woman' in full_text or 'adulteress' in full_text or 'seductress' in full_text:
            return "Warning Against the Adulteress"
        if 'sinners' in full_text and 'entice' in full_text:
            return "Rejecting Evil Companions"
        if any(x in full_text for x in ['wisdom', 'understanding', 'knowledge']):
            return "Call to Pursue Wisdom"
        if any(x in full_text for x in ['debt', 'surety', 'co-sign']):
            return "Warning on Surety/Debt"
        if any(x in full_text for x in ['diligent', 'lazy', 'sluggard']):
            return "Diligence vs. Laziness"
        return "Father's Instruction"
    
    if 'wisdom calls' in full_text:
        return "Wisdom's Public Call"
    
    if 'wisdom has built' in full_text:
        return "Wisdom's Banquet"
    
    if 'who can find' in full_text:
        return "In Praise of the Excellent Wife"
    
    if 'king' in full_text and ('throne' in full_text or 'reign' in full_text or 'justice' in full_text):
        return "Royal Wisdom"
    
    if any(x in full_text for x in ['sluggard', 'lazy', 'sleep', 'hand in dish']):
        return "The Sluggard"
    
    # Nature/animal proverbs clustering
    if 'ant' in full_text or 'conies' in full_text or 'locust' in full_text:
        return "Lessons from Creatures"
    
    # Generic: use first few words
    words = first.split()[:4]
    return ' '.join(words) + '...'

def analyze_chapter(chapter_num, verses):
    """Analyze a single chapter."""
    verses_sorted = sorted(verses, key=lambda x: x['verse'])
    sections_raw = segment_chapter(verses_sorted)
    
    sections = []
    for sec_verses in sections_raw:
        if not sec_verses:
            continue
            
        start = f"{sec_verses[0]['chapter']}:{sec_verses[0]['verse']}"
        end = f"{sec_verses[-1]['chapter']}:{sec_verses[-1]['verse']}"
        
        if start == end:
            verse_range = start
        else:
            verse_range = f"{sec_verses[0]['chapter']}:{sec_verses[0]['verse']}-{sec_verses[-1]['verse']}"
        
        full_text = ' '.join(v['text'] for v in sec_verses)
        
        sections.append({
            'range': verse_range,
            'title': generate_title(sec_verses),
                       'text': full_text,
            'summary': '',  # Will be filled
            'financial_concepts': extract_financial_concepts(full_text)
        })

    return sections

def analyze_all_chapters():
    """Process all Proverbs chapters."""
    verses = load_proverbs()
    chapter_verses = {}
    for v in verses:
        ch = v['chapter']
        if ch not in chapter_verses:
            chapter_verses[ch] = []
        chapter_verses[ch].append(v)
    
    results = {}
    for ch_num in sorted(chapter_verses.keys()):
        results[f"Chapter_{ch_num}"] = analyze_chapter(ch_num, chapter_verses[ch_num])
    return results

if __name__ == '__main__':
    output = analyze_all_chapters()
    import json
    print(json.dumps(output, indent=2))
