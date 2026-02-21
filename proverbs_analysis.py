import csv
import json
import re
from collections import defaultdict

# Read the CSV file
verses = []
with open('proverbs.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        if len(row) >= 2:
            ref = row[0]
            text = row[1]
            # Parse chapter and verse
            match = re.match(r'Proverbs (\d+):(\d+)', ref)
            if match:
                chapter = int(match.group(1))
                verse_num = int(match.group(2))
                verses.append({
                    'chapter': chapter,
                    'verse': verse_num,
                    'text': text,
                    'ref': ref
                })

print(f"Loaded {len(verses)} verses")
print(f"Chapters: {min(v['chapter'] for v in verses)} - {max(v['chapter'] for v in verses)}")

# Group verses by chapter
chapters_data = defaultdict(list)
for v in verses:
    chapters_data[v['chapter']].append(v)

# Sort chapters
chapters_data = {k: sorted(chapters_data[k], key=lambda x: x['verse']) for k in sorted(chapters_data.keys())}

print(f"Total chapters: {len(chapters_data)}")
for ch, vs in chapters_data.items():
    print(f"Chapter {ch}: {len(vs)} verses")
