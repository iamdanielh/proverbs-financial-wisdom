#!/usr/bin/env python3
"""Restructure Proverbs financial content into book chapters."""

import json
from collections import defaultdict

# Define book chapter categories based on personal finance structure
BOOK_CATEGORIES = {
    "foundation": {
        "title": "The Foundation: Stewardship and Ownership",
        "description": "God owns everything; we are stewards. The fear of Yahweh as the basis of financial wisdom.",
        "concepts": ["fear of yahweh", "wisdom", "knowledge", "understanding", "trust", "prudence"]
    },
    "income_work": {
        "title": "Income Generation: The Diligence Principle",
        "description": "Work as virtue, laziness as poverty. How diligence creates security.",
        "concepts": ["diligence", "labor", "work", "harvest", "plenty", "hand", "worker", "industrious"]
    },
    "laziness_poverty": {
        "title": "The Sluggard's Path: Consequences of Fiscal Irresponsibility",
        "description": "Warnings against laziness, sleep, and hands folded in poverty.",
        "concepts": ["sluggard", "lazy", "sleep", "slothful", "idle", "poverty", "want"]
    },
    "planning_strategy": {
        "title": "Strategic Financial Planning",
        "description": "Counsel, advice, and wise dealing in financial matters.",
        "concepts": ["plan", "counsel", "advice", "guidance", "consider", "wise dealing"]
    },
    "contentment_vs_greed": {
        "title": "Contentment vs. The Greed Trap",
        "description": "The dangers of quick gain, covetousness, and loving money.",
        "concepts": ["greedy", "greed", "quick gain", "hurry", "covetousness", "love of money"]
    },
    "debt_surety": {
        "title": "Debt and Surety: The Borrower's Warning",
        "description": "Warnings on borrowing, co-signing, and the snare of debt.",
        "concepts": ["debt", "borrow", "lender", "surety", "creditor", "strike hands", "co-sign"]
    },
    "generosity_giving": {
        "title": "Generosity: The Open Hand",
        "description": "Giving, firstfruits, and the prosperity of generosity.",
        "concepts": ["generosity", "give", "gift", "firstfruits", "honor yahweh", "openhanded", "lend"]
    },
    "wealth_building": {
        "title": "Wealth Building and Storage",
        "description": "Barns, storage, provision, and building lasting wealth.",
        "concepts": ["wealth", "riches", "barns", "store", "increase", "abundance", "plenty"]
    },
    "treasure_valuation": {
        "title": "True Treasure: Valuing Wisdom Over Wealth",
        "description": "Silver, gold, rubies—and why wisdom is better.",
        "concepts": ["silver", "gold", "rubies", "treasure", "precious", "better than", "value"]
    },
    "poverty_needs": {
        "title": "Understanding Poverty and Need",
        "description": "The poor, the needy, and how to treat them.",
        "concepts": ["poor", "needy", "poverty", "want", "lack", "oppression"]
    },
    "honest_commerce": {
        "title": "Honest Commerce and Fair Dealing",
        "description": "Just weights, honest transactions, and integrity in business.",
        "concepts": ["honest", "just", "fair", "integrity", "righteous", "equity", "deceitful", "false"]
    },
    "inheritance_legacy": {
        "title": "Legacy and Inheritance",
        "description": "Passing wealth to children, the good name, and multi-generational thinking.",
        "concepts": ["inheritance", "inherit", "fathers", "children", "grandchildren", "house", "name"]
    },
    "wages_compensation": {
        "title": "Wages and Compensation",
        "description": "Laborers deserve their pay, timing of wages, and worker fairness.",
        "concepts": ["wages", "pay", "worker", "hireling", "reap", "sow", "labor"]
    },
    "leadership_stewardship": {
        "title": "Leadership and Household Stewardship",
        "description": "Managing households, servants, and the finances of leadership.",
        "concepts": ["rule", "manage", "household", "servants", "king", "throne", "leaders"]
    },
    "warnings_temptations": {
        "title": "Financial Temptations and Get-Rich-Quick Schemes",
        "description": "Evil companions, stolen gain, and the seduction of easy wealth.",
        "concepts": ["ill-gotten", "stolen", "fraud", "easy gain", "entice", "robber", "spoils"]
    }
}

def match_section_to_book_chapter(section_text, concepts):
    """Match a section to the best book chapter category."""
    text_lower = section_text.lower()
    scores = defaultdict(float)
    
    # Score based on detected concepts
    for concept in concepts:
        concept_lower = concept.lower()
        for cat_id, cat_data in BOOK_CATEGORIES.items():
            for cat_concept in cat_data['concepts']:
                if cat_concept.lower() in concept_lower:
                    scores[cat_id] += 2
    
    # Score based on text content
    for cat_id, cat_data in BOOK_CATEGORIES.items():
        for cat_concept in cat_data['concepts']:
            if cat_concept.lower() in text_lower:
                scores[cat_id] += 1
    
    # Return best match or None
    if scores:
        best = max(scores, key=scores.get)
        if scores[best] > 0:
            return best
    return None

def main():
    # Load the thematic analysis
    with open('proverbs_thematic_analysis.json') as f:
        data = json.load(f)
    
    # Structure for book
    book_structure = {cat_id: [] for cat_id in BOOK_CATEGORIES}
    uncategorized = []
    
    # Process each section with financial concepts
    for ch in data['chapters']:
        for sec in ch['sections']:
            if not sec.get('financial_concepts'):
                continue
            
            # Find best category
            cat = match_section_to_book_chapter(sec['text'], sec['financial_concepts'])
            
            section_data = {
                "range": sec['range'],
                "title": sec['title'],
                "summary": sec['summary'],
                "concepts": sec['financial_concepts'],
                "text": sec['text'][:300] + "..." if len(sec['text']) > 300 else sec['text']
            }
            
            if cat:
                book_structure[cat].append(section_data)
            else:
                uncategorized.append(section_data)
    
    # Build output
    output = {
        "book_title": "Proverbs: Ancient Wisdom for Modern Finance",
        "chapters": [],
        "uncategorized": uncategorized
    }
    
    chapter_num = 1
    for cat_id, cat_data in BOOK_CATEGORIES.items():
        if book_structure[cat_id]:  # Only include if we have content
            output["chapters"].append({
                "chapter_number": chapter_num,
                "category_id": cat_id,
                "title": cat_data["title"],
                "description": cat_data["description"],
                "section_count": len(book_structure[cat_id]),
                "source_verses": book_structure[cat_id]
            })
            chapter_num += 1
    
    # Stats
    total_financial = sum(len(v) for v in book_structure.values())
    output["stats"] = {
        "total_source_sections": total_financial,
        "book_chapters": len(output["chapters"]),
        "uncategorized_sections": len(uncategorized)
    }
    
    # Save
    with open('proverbs_book_structure.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
