#!/usr/bin/env python3
import json

with open('proverbs_book_structure.json') as f:
    data = json.load(f)

insights = [
    {"chapter": 1, "headline": "Wealth needs roots before it bears fruit", "summary": "The fear of Yahweh is the beginning—not destination—of financial wisdom. Without this foundation, profit is a house on sand.", "key_points": ["Wisdom > Money", "Character is Capital", "Foundation First"], "proverbs_says": "Before counting money, learn to fear God. Proverbs' first lesson: foundation matters more than cash flow.", "color": "#1a237e", "icon": "🏛️"},
    {"chapter": 2, "headline": "Treat labor like treasure—seek it that way", "summary": "Seek wisdom as silver, search as hidden treasure. The mental model: wisdom = active pursuit = capital. Not passive.", "key_points": ["Diligence = Abundance", "Active Work", "Sow to Reap"], "proverbs_says": "You don't get wealthy; you get wisdom, and wisdom generates wealth. The search is active.", "color": "#00695c", "icon": "⚒️"},
    {"chapter": 3, "headline": "Inaction compounds poverty", "summary": "Folded hands create debt as reliably as open hands create wealth. Poverty accumulates through neglect, not strikes.", "key_points": ["Motion > Stillness", "Avoid Folds", "Wake Up"], "proverbs_says": "Laziness mortgages your future for present ease. Poverty is behavioral failure with financial consequences.", "color": "#c62828", "icon": "💤"},
    {"chapter": 4, "headline": "Shortcuts destroy wisdom", "summary": "Counsel is more valuable than silver. Strategic planning precedes success. The wise consult; fools rush.", "key_points": ["Consult Widely", "Think Ahead", "Advice is Asset"], "proverbs_says": "Financial planning isn't lonely spreadsheet work—it's communal wisdom. Your budget needs peer review.", "color": "#455a64", "icon": "🧭"},
    {"chapter": 5, "headline": "Hurry makes holes in pockets", "summary": "Wealth from gambling or quick gain is temporary. The one who hastens to be rich will not go unpunished.", "key_points": ["Patience > Speed", "Greed Self-Destructs", "Sustainable > Fast"], "proverbs_says": "Speed is the enemy of sustainability. Don't get rich fast—the tortoise beats the hare in finance too.", "color": "#e65100", "icon": "⚡"},
    {"chapter": 6, "headline": "Never sign what you can't pay", "summary": "Debt is a snare. Co-signing is explicitly warned. The borrower becomes servant to the lender. Free yourself.", "key_points": ["Debt = Bondage", "Avoid Surety", "Escape Early"], "proverbs_says": "Co-signing guarantees another's irresponsibility. Your signature enslaves you to their choices.", "color": "#b71c1c", "icon": "⛓️"},
    {"chapter": 7, "headline": "Give first, receive more", "summary": "Honor Yahweh with substance—not surplus. Firstfruits unlock overflow. Generosity is physics, not charity.", "key_points": ["Firstfruits Principle", "Generosity Multiplies", "Open Hand"], "proverbs_says": "Give first, receive more. The universe honors generosity—barns overflow to the giver.", "color": "#2e7d32", "icon": "💧"},
    {"chapter": 8, "headline": "Build barns before you need them", "summary": "The wise store up choice food; fools devour everything. Wealth requires delayed gratification and reserves.", "key_points": ["Build Reserves", "Delay Gratification", "Storage Matters"], "proverbs_says": "Wealth is built slowly, then suddenly. The barns of the diligent have surplus.", "color": "#f57c00", "icon": "📦"},
    {"chapter": 9, "headline": "Wisdom > Gold by every metric", "summary": "Silver, gold, rubies—all valuable, but wisdom more so. Get wisdom though it costs all you have.", "key_points": ["Wisdom is Premium", "Prioritize Correctly", "ROI is Eternal"], "proverbs_says": "Most value wealth over wisdom. Proverbs corrects this: wisdom produces wealth, not vice versa.", "color": "#6a1b9a", "icon": "💎"},
    {"chapter": 10, "headline": "False scales are discovered", "summary": "Just weights please God. Dishonest gain is ill-gotten and short-lived. Integrity in business is non-negotiable.", "key_points": ["Integrity Pays", "Deceit Fails", "Just Dealing"], "proverbs_says": "Dishonest money dwindles. The just balance is found out—so use it from the start.", "color": "#37474f", "icon": "⚖️"},
    {"chapter": 11, "headline": "Wealth transfers; character compounds", "summary": "A good name is more valuable than riches. Train children young. You steward for the next generation.", "key_points": ["Name > Money", "Train Children", "Think Generations"], "proverbs_says": "The house of the righteous stands. Build a lasting name, not just a bank account.", "color": "#5d4037", "icon": "🌳"},
    {"chapter": 12, "headline": "Pay promptly; work faithfully", "summary": "The laborer is worthy of hire. Withhold not wages overnight. The worker deserves fair compensation.", "key_points": ["Prompt Payment", "Labor Reward", "Fairness"], "proverbs_says": "Don't sleep while workers wait for pay. Fair wages given quickly build trust and honor.", "color": "#00796b", "icon": "💵"}
]

with open('proverbs_insights.json', 'w') as f:
    json.dump(insights, f, indent=2)

print(f"Created {len(insights)} insights")
for i, ins in enumerate(insights, 1):
    print(f"{i}. {ins['icon']} {ins['headline']}")
