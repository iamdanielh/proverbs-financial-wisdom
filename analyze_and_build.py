#!/usr/bin/env python3
"""Analyze verses and build insights for each chapter."""
import json
from collections import Counter

with open('proverbs_book_structure.json') as f:
    data = json.load(f)

insights = []

for ch in data['chapters']:
    title = ch['title']
    sections = ch['sections']
    
    # Analyze all text in this chapter
    all_text = ' '.join([s.get('text', '') for s in sections]).lower()
    
    # Count key financial terms
    diligence_terms = ['diligent', 'labor', 'hand', 'work', 'industry', 'harvest']
    poverty_terms = ['sluggard', 'poor', 'poverty', 'lack', 'want']
    wealth_terms = ['wealth', 'riches', 'abundance', 'barns', 'plenty']
    greed_terms = ['greedy', 'hurry', 'quick', 'gain', 'easy']
    debt_terms = ['debt', 'borrow', 'lend', 'surety', 'creditor']
    give_terms = ['give', 'generous', 'firstfruits', 'gift', 'honor yahweh']
    wisdom_terms = ['wisdom', 'understanding', 'knowledge', 'fear of yahweh']
    honest_terms = ['just', 'honest', 'false', 'deceit', 'integrity']
    treasure_terms = ['silver', 'gold', 'rubies', 'coral', 'precious']
    inherit_terms = ['inherit', 'children', 'generation', 'fathers']
    
    def count_terms(terms):
        return sum(all_text.count(t) for t in terms)
    
    # Identify chapter theme by title matching
    chapter_num = ch['chapter']
    
    if chapter_num == 1:
        insight = {
            "title": title,
            "headline": "Wealth needs roots before it bears fruit",
            "summary": "The fear of Yahweh is the beginning of knowledge—not the destination. Proverbs opens by establishing the prerequisite for financial wisdom: reverence. Without this foundation, all profit is a house on sand.",
            "key_insights": [
                "Financial literacy without character is dangerous",
                "The simple need prudence; the young need discretion",
                "Wisdom is acquired through listening, not speculation"
            ],
            "proverbs_says": "Before you count money, learn to fear God. The same source gave both. Without the latter, the former destroys. This is Proverbs' first financial lesson: foundation matters more than cash flow.",
            "color": "#1a237e",
            "icon": "🏛️"
        }
    elif chapter_num == 2:
        insight = {
            "title": title,
            "headline": "Treat labor like treasure—seek it that way",
            "summary": "Wisdom is the asset that produces all other assets. Seek her as silver, search for her as hidden treasure. The mental model: wisdom = active pursuit = capital. Not passive accumulation.",
            "key_insights": [
                "Seeking wisdom takes effort—like mining silver",
                "Understanding pays dividends: 'you will understand righteousness and justice'",
                "Returns on wisdom include riches and honor"
            ],
            "proverbs_says": "Personal finance starts with personal wisdom. You don't get wealthy; you get wisdom, and wisdom generates wealth. The search is active, not inherited.",
            "color": "#00695c",
            "icon": "⚒️"
        }
    elif chapter_num == 3:
        insight = {
            "title": title,
            "headline": "The sluggard is a slow-motion disaster",
            "summary": "Folded hands create debt as reliably as open hands create wealth. Poverty doesn't strike—it accumulates through neglect. The sluggard is addressed directly: sleep less, work more.",
            "key_insights": [
                "Poverty arrives as a traveler, then settles in",
                "'A little sleep' becomes a lot of poverty",
                "Ants work without bosses; sluggards need supervision"
            ],
            "proverbs_says": "Laziness is not rest—it's debt financing. The sluggard mortgages his future for present ease. Proverbs treats this as a moral failure with financial consequences.",
            "color": "#c62828",
            "icon": "💤"
        }
    elif chapter_num == 4:
        insight = {
            "title": title,
            "headline": "Plan with counsel, or plan to fail",
            "summary": "Strategic planning is wisdom in motion. Without guidance, plans fail. With many counselors, success. Planning isn't prediction—it's preparation through wisdom-gathering.",
            "key_insights": [
                "Plans succeed with guidance; fail without",
                "Many counselors = safety",
                "The heart plans; Yahweh establishes"
            ],
            "proverbs_says": "Good financial planning isn't lonely spreadsheet work—it's communal wisdom gathering. Your budget needs peer review. Your vision needs counselors.",
            "color": "#455a64",
            "icon": "🧭"
        }
    elif chapter_num == 5:
        insight = {
            "title": title,
            "headline": "Riches that come fast, leave faster",
            "summary": "Wealth from gambling, get-rich-quick schemes, or dishonest gain is temporary. The one who hastens to be rich will not go unpunished. True wealth is slow currency.",
            "key_insights": [
                "Hurrying to wealth = poverty",
                "Wealth gained by fraud diminishes",
                "Dishonest money dwindles"
            ],
            "proverbs_says": "Speed is the enemy of sustainability. Proverbs doesn't say 'don't get rich'—it says don't get rich fast. The tortoise beats the hare in finance too.",
            "color": "#e65100",
            "icon": "⚡"
        }
    elif chapter_num == 6:
        insight = {
            "title": title,
            "headline": "Debt makes you someone else's property",
            "summary": "Three warnings on surety/co-signing in Proverbs 6. The borrower becomes servant to the lender. Free yourself like a gazelle from the hand of the hunter. Debt is bondage.",
            "key_insights": [
                "Surety is a snare—don't take the bait",
                "Co-signing = guaranteeing someone else's irresponsibility",
                "Escape debt urgently, like prey from hunter"
            ],
            "proverbs_says": "Debt isn't a tool; it's a trap. Proverbs warns repeatedly: if you've cosigned, get out now. Your signature enslaves you to another's choices.",
            "color": "#b71c1c",
            "icon": "⛓️"
        }
    elif chapter_num == 7:
        insight = {
            "title": title,
            "headline": "Generosity is an investment, not a loss",
            "summary": "Honor Yahweh with your substance—not your surplus. Firstfruits unlock overflow. Give when it costs, not when it's convenient. The generous soul will be made fat.",
            "key_insights": [
                "First portions, not leftovers, honor God",
                "Barns and vats overflow to the giver",
                "Withhold not the good you can give today"
            ],
            "proverbs_says": "Generosity isn't charity—it's physics. Give first, receive more. Tested: honor increases substance. The universe honors generosity.",
            "color": "#2e7d32",
            "icon": "💧"
        }
    elif chapter_num == 8:
        insight = {
            "title": title,
            "headline": "Wealth without storage is an oxymoron",
            "summary": "The wise store up choice food and oil; fools devour everything. Wealth building requires delayed gratification. The barns of the diligent have surplus.",
            "key_insights": [
                "Storage separates wise from foolish",
                "Delayed gratification builds reserves",
                "Abundance comes to those