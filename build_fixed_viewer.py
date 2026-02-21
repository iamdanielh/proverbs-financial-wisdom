import json

with open('proverbs_insights.json') as f:
    insights = json.load(f)

with open('proverbs_by_chapter_fixed.json') as f:
    book = json.load(f)

insights_json = json.dumps(insights)
book_json = json.dumps(book)

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Proverbs Financial Wisdom</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: linear-gradient(135deg, #1a237e 0%, #283593 50%, #3949ab 100%); min-height: 100vh; color: #333; }}
        .header {{ background: rgba(0,0,0,0.4); color: white; padding: 1.2rem; text-align: center; position: sticky; top: 0; z-index: 100; }}
        .header h1 {{ font-size: 1.3rem; font-weight: 300; }}
        .header h1 span {{ font-weight: 700; display: block; font-size: 1.1rem; }}
        .nav {{ display: flex; flex-wrap: wrap; gap: 0.5rem; justify-content: center; padding: 1rem; background: rgba(255,255,255,0.05); }}
        .nav-btn {{ background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); color: white; padding: 0.5rem 1rem; border-radius: 20px; cursor: pointer; font-size: 0.85rem; }}
        .nav-btn:hover {{ background: rgba(255,255,255,0.2); }}
        .nav-btn.active {{ background: white; color: #1a237e; }}
        .container {{ max-width: 900px; margin: 0 auto; padding: 1rem; }}
        .insight-card {{ background: white; border-radius: 16px; margin-bottom: 1.5rem; overflow: hidden; box-shadow: 0 10px 40px rgba(0,0,0,0.3); }}
        .insight-header {{ padding: 1.5rem; color: white; }}
        .insight-icon {{ font-size: 2.5rem; margin-bottom: 0.5rem; }}
        .insight-chapter {{ font-size: 0.8rem; opacity: 0.9; text-transform: uppercase; letter-spacing: 1px; }}
        .insight-headline {{ font-size: 1.3rem; font-weight: 700; }}
        .insight-body {{ padding: 1.5rem; }}
        .insight-summary {{ font-size: 1rem; line-height: 1.6; color: #444; margin-bottom: 1rem; }}
        .insight-proverbs {{ background: #f8f9fa; border-left: 4px solid; padding: 1rem; margin-bottom: 1rem; font-style: italic; border-radius: 0 8px 8px 0; }}
        .key-points {{ display: flex; flex-wrap: wrap; gap: 0.5rem; }}
        .key-point {{ background: #f0f4f8; padding: 0.4rem 0.8rem; border-radius: 15px; font-size: 0.85rem; color: #555; }}
        .verse-section {{ background: white; border-radius: 12px; margin-bottom: 1rem; padding: 1.2rem; box-shadow: 0 4px 20px rgba(0,0,0,0.15); }}
        .verse-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem; flex-wrap: wrap; gap: 0.5rem; }}
        .verse-title {{ font-weight: 600; color: #1a237e; font-size: 1rem; }}
        .verse-range {{ background: #e8eaf6; padding: 0.3rem 0.6rem; border-radius: 12px; font-size: 0.8rem; color: #3949ab; }}
        .verse-text {{ font-size: 1rem; line-height: 1.7; color: #333; margin-bottom: 0.8rem; }}
        .verse-concepts {{ display: flex; flex-wrap: wrap; gap: 0.4rem; }}
        .concept-tag {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 0.3rem 0.7rem; border-radius: 12px; font-size: 0.75rem; }}
        .search-box {{ width: 100%; padding: 1rem; border: none; border-radius: 12px; margin-bottom: 1rem; font-size: 1rem; background: rgba(255,255,255,0.95); }}
        .footer {{ text-align: center; padding: 2rem; color: rgba(255,255,255,0.7); font-size: 0.85rem; }}
    </style>
</head>
<body>
    <div class="header"><h1>📖 Proverbs <span>Financial Wisdom Explorer</span></h1></div>
    <div class="nav" id="nav"></div>
    <div class="container">
        <input type="text" class="search-box" id="search" placeholder="🔍 Search verses, topics...">
        <div id="content"></div>
    </div>
    <div class="footer"><p>12 Chapters • Financial Wisdom • Verses in Correct Chapters</p></div>
    <script>
        const insights = {insights_json};
        const book = {book_json};
        let currentChapter = 0;
        
        function init() {{
            const nav = document.getElementById("nav");
            nav.innerHTML = '<button class="nav-btn active" onclick="showChapter(0)">📊 All</button>' + 
                insights.map(i => '<button class="nav-btn" onclick="showChapter('+i.chapter+')">'+i.chapter+'</button>').join("");
            render();
            document.getElementById("search").addEventListener("input", render);
        }}
        
        function showChapter(n) {{
            currentChapter = n;
            document.querySelectorAll(".nav-btn").forEach((b,i) => b.classList.toggle("active", i===n));
            render();
        }}
        
        function render() {{
            const search = document.getElementById("search").value.toLowerCase();
            const container = document.getElementById("content");
            let html = "";
            
            const chapters = currentChapter === 0 ? book.chapters : [book.chapters[currentChapter-1]];
            
            chapters.forEach((ch, idx) => {{
                const chapNum = currentChapter === 0 ? idx + 1 : currentChapter;
                const insight = insights.find(i => i.chapter === chapNum);
                
                if (insight) {{
                    html += '<div class="insight-card">' +
                        '<div class="insight-header" style="background: '+insight.color+'">' +
                            '<div class="insight-icon">'+insight.icon+'</div>' +
                            '<div class="insight-chapter">Chapter '+insight.chapter+'</div>' +
                            '<div class="insight-headline">'+insight.headline+'</div>' +
                        '</div>' +
                        '<div class="insight-body">' +
                            '<div class="insight-summary">'+insight.summary+'</div>' +
                            '<div class="insight-proverbs" style="border-color: '+insight.color+'"><strong>Proverbs Says:</strong> '+insight.proverbs_says+'</div>' +
                            '<div class="key-points">'+insight.key_points.map(p => '<span class="key-point">'+p+'</span>').join("")+'</div>' +
                        '</div></div>';
                }}
                
                const filtered = ch.sections.filter(s => {{
                    if (!s.financial_concepts || s.financial_concepts.length === 0) return false;
                    if (!search) return true;
                    return s.text.toLowerCase().includes(search) || s.title.toLowerCase().includes(search) || s.financial_concepts.some(c => c.toLowerCase().includes(search));
                }});
                
                filtered.forEach(s => {{
                    html += '<div class="verse-section">' +
                        '<div class="verse-header">' +
                            '<span class="verse-title">'+s.title+'</span>' +
                            '<span class="verse-range">'+s.range+'</span>' +
                        '</div>' +
                        '<div class="verse-text">'+s.text+'</div>' +
                        '<div class="verse-concepts">'+s.financial_concepts.map(c => '<span class="concept-tag">'+c+'</span>').join("")+'</div>' +
                    '</div>';
                }});
            }});
            
            container.innerHTML = html || "<p style='color:white;text-align:center;padding:2rem'>No results found</p>";
        }}
        
        init();
    </script>
</body>
</html>'''

with open('proverbs_correct.html', 'w') as f:
    f.write(html)

print('Created proverbs_correct.html')