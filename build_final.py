import json

with open('proverbs_complete_book.json') as f:
    book = json.load(f)

with open('proverbs_insights.json') as f:
    insights = json.load(f)

html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Proverbs: 238 Sections of Financial Wisdom</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
               background: linear-gradient(135deg, #1a237e 0%, #283593 50%, #3949ab 100%); 
               min-height: 100vh; color: #333; }
        .header { background: rgba(0,0,0,0.5); color: white; padding: 1.5rem; text-align: center; 
                 position: sticky; top: 0; z-index: 100; }
        .header h1 { font-size: 1.4rem; font-weight: 300; }
        .header h1 span { font-weight: 700; display: block; margin-top: 0.3rem; }
        .nav { display: flex; flex-wrap: wrap; gap: 0.4rem; justify-content: center; 
               padding: 1rem; background: rgba(255,255,255,0.05); }
        .nav-btn { background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2);
                    color: white; padding: 0.5rem 0.8rem; border-radius: 20px; cursor: pointer; }
        .nav-btn.active { background: white; color: #1a237e; }
        .container { max-width: 900px; margin: 0 auto; padding: 1rem; }
        .chapter-card { background: white; border-radius: 16px; margin-bottom: 1.5rem; 
                        overflow: hidden; box-shadow: 0 10px 40px rgba(0,0,0,0.3); }
        .chapter-header { padding: 1.5rem; color: white; }
        .chapter-icon { font-size: 2.5rem; margin-bottom: 0.5rem; }
        .chapter-title { font-size: 1.2rem; font-weight: 700; }
        .chapter-body { padding: 1.5rem; }
        .verse-section { background: #fafafa; border-radius: 12px; margin-bottom: 1rem; 
                       padding: 1.2rem; border: 1px solid #e0e0e0; }
        .verse-header { display: flex; justify-content: space-between; margin-bottom: 0.8rem; }
        .verse-range { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                      color: white; padding: 0.3rem 0.8rem; border-radius: 12px; font-size: 0.8rem; }
        .verse-text { font-size: 1rem; line-height: 1.8; color: #333; }
        .concept-tag { background: #fff3e0; color: #e65100; padding: 0.25rem 0.7rem; 
                      border-radius: 10px; font-size: 0.75rem; margin-right: 0.4rem; }
        .search-box { width: 100%; padding: 1rem; border: none; border-radius: 12px; 
                     margin-bottom: 1rem; font-size: 1rem; }
        .footer { text-align: center; padding: 2rem; color: rgba(255,255,255,0.6); }
        .insight-box { background: #f8f9fa; border-left: 4px solid; padding: 1rem; 
                      margin: 1rem 0; font-style: italic; }
    </style>
</head>
<body>
    <div class="header"><h1>📖 Proverbs <span>Complete Financial Wisdom</span></h1></div>
    <div class="nav" id="nav"></div>
    <div class="container">
        <input type="text" class="search-box" id="search" placeholder="🔍 Search...">
        <div id="content"></div>
    </div>
    <div class="footer">238 Sections • 313 Verses • 12 Thematic Chapters</div>

<script>
const book = ''' + json.dumps(book) + ''';
const insights = ''' + json.dumps(insights) + ''';
let current = 0;

function init() {
    let nav = '<button class="nav-btn active" onclick="show(0)">All</button>';
    book.chapters.forEach((c,i) => nav += '<button class="nav-btn" onclick="show('+(i+1)+')">'+(i+1)+'</button>');
    document.getElementById('nav').innerHTML = nav;
    render();
    document.getElementById('search').addEventListener('input', render);
}

function show(n) {
    current = n;
    document.querySelectorAll('.nav-btn').forEach((b,i) => b.classList.toggle('active', i===n));
    render();
}

function render() {
    const s = document.getElementById('search').value.toLowerCase();
    let h = '';
    const chs = current === 0 ? book.chapters : [book.chapters[current-1]];
    
    chs.forEach((ch, idx) => {
        const cn = current === 0 ? ch.chapter : current;
        const ins = insights.find(i => i.chapter === cn);
        h += '<div class="chapter-card">';
        h += '<div class="chapter-header" style="background:'+(ins?ins.color:'#1a237e')+'">';
        h += '<div class="chapter-icon">'+(ins?ins.icon:'📖')+'</div>';
        h += '<div class="chapter-title">Chapter '+ch.chapter+': '+ch.title+'</div>';
        h += '</div><div class="chapter-body">';
        if(ins) {
            h += '<div class="insight-box" style="border-color:'+ins.color+'">';
            h += '<strong>💡 '+ins.headline+'</strong><br>'+ins.summary;
            h += '</div>';
        }
        h += '<p style="margin-bottom:1rem;color:#666">'+ch.section_count+' sections</p>';
        
        const fil = ch.sections.filter(sec => {
            if(!s) return true;
            return sec.text.toLowerCase().includes(s) || sec.concepts.some(c=>c.toLowerCase().includes(s));
        });
        
        fil.forEach(sec => {
            h += '<div class="verse-section">';
            h += '<div class="verse-header">';
            h += '<span style="font-weight:600">'+sec.title+'</span>';
            h += '<span class="verse-range">'+sec.range+'</span></div>';
            h += '<div class="verse-text">'+sec.text+'</div>';
            h += '<div style="margin-top:0.5rem">';
            sec.financial_concepts.forEach(c => h += '<span class="concept-tag">'+c+'</span>');
            h += '</div></div>';
        });
        h += '</div></div>';
    });
    document.getElementById('content').innerHTML = h || '<p style="color:white;text-align:center">No results</p>';
}

init();
</script>
</body>
</html>'''

with open('proverbs_full.html', 'w') as f:
    f.write(html)

print('Created proverbs_full.html')
