import json

with open('proverbs_complete_book.json') as f:
    book = json.load(f)

with open('proverbs_insights.json') as f:
    insights = json.load(f)

book_json = json.dumps(book).replace('</', '<\\/')
insights_json = json.dumps(insights).replace('</', '<\\/')

html = f'''<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Proverbs Complete</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:linear-gradient(135deg,#1a237e,#283593,#3949ab);min-height:100vh;color:#333}}
.header{{background:rgba(0,0,0,.5);color:white;padding:1.5rem;text-align:center;position:sticky;top:0;z-index:100}}
.header h1{{font-size:1.3rem;font-weight:300}}.header h1 span{{font-weight:700;display:block;margin-top:.3rem}}
.nav{{display:flex;flex-wrap:wrap;gap:.4rem;justify-content:center;padding:1rem;background:rgba(255,255,255,.05)}}
.nav-btn{{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.2);color:white;padding:.5rem .8rem;border-radius:20px;cursor:pointer;font-size:.8rem}}
.nav-btn.active{{background:white;color:#1a237e;font-weight:600}}
.container{{max-width:900px;margin:0 auto;padding:1rem}}
.card{{background:white;border-radius:16px;margin-bottom:1.5rem;overflow:hidden;box-shadow:0 10px 40px rgba(0,0,0,.3)}}
.ch-h{{padding:1.5rem;color:white}}
.ch-icon{{font-size:2.5rem;margin-bottom:.5rem;display:block}}
.ch-num{{font-size:.75rem;opacity:.9;text-transform:uppercase;letter-spacing:1px}}
.ch-title{{font-size:1.2rem;font-weight:700;margin:.3rem 0}}
.ch-sub{{font-size:.9rem;opacity:.9}}
.ch-body{{padding:1.5rem}}
.quote{{background:#f8f9fa;border-left:4px solid;padding:1rem;margin:1rem 0;font-style:italic;border-radius:0 8px 8px 0}}
.tags{{display:flex;flex-wrap:wrap;gap:.5rem;margin:1rem 0}}
.tag{{background:#e3f2fd;padding:.4rem .9rem;border-radius:15px;font-size:.85rem;color:#1565c0}}
.count{{text-align:center;padding:.8rem;background:#f5f5f5;border-radius:8px;margin:1rem 0;font-size:.9rem;color:#666}}
.vs{{background:#fafafa;border-radius:12px;margin-bottom:1rem;padding:1.2rem;border:1px solid #e0e0e0}}
.vh{{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:.8rem;flex-wrap:wrap;gap:.5rem}}
.vr{{background:linear-gradient(135deg,#667eea,#764ba2);color:white;padding:.3rem .8rem;border-radius:12px;font-size:.8rem;font-weight:600}}
.vt{{font-weight:600;color:#1a237e;font-size:.95rem;flex:1}}
.vtext{{font-size:1rem;line-height:1.7;color:#333;margin-bottom:.8rem}}
.vc{{display:flex;flex-wrap:wrap;gap:.4rem}}
.ct{{background:#fff3e0;color:#e65100;padding:.25rem .7rem;border-radius:10px;font-size:.75rem;border:1px solid #ffe0b2}}
.sbox{{width:100%;padding:1rem;border:none;border-radius:12px;margin-bottom:1rem;font-size:1rem;background:rgba(255,255,255,.95)}}
.stats{{background:rgba(255,255,255,.1);padding:1rem;text-align:center;color:rgba(255,255,255,.9);font-size:.85rem;border-radius:8px;margin-bottom:1rem}}
.footer{{text-align:center;padding:2rem;color:rgba(255,255,255,.6);font-size:.85rem}}
</style></head>
<body>
<div class="header"><h1>📖 Proverbs <span>Complete Financial Wisdom</span></h1></div>
<div class="nav" id="nav"></div>
<div class="container">
<div class="stats" id="stats">Loading...</div>
<input type="text" class="sbox" id="search" placeholder="🔍 Search verses, topics...">
<div id="content">Loading...</div>
</div>
<div class="footer"><p>238 Sections • 12 Chapters • Complete</p></div>
<script>
const book={book_json};
const insights={insights_json};
let currentChapter=0;
function init(){{
  let navHtml='<button class="nav-btn active" onclick="showChapter(0)">📊 All</button>';
  book.chapters.forEach((ch,i)=>{{navHtml+='<button class="nav-btn" onclick="showChapter('+(i+1)+')">'+ch.chapter+'</button>'}});
  document.getElementById('nav').innerHTML=navHtml;
  const total=book.chapters.reduce((sum,ch)=>sum+ch.section_count,0);
  document.getElementById('stats').innerHTML='📚 <b>'+total+'</b> sections • '+book.chapters.map(ch=>'Ch '+ch.chapter+': <b>'+ch.section_count+'</b>').join(' • ');
  render();
  document.getElementById('search').addEventListener('input',render);
}}
function showChapter(n){{
  currentChapter=n;
  document.querySelectorAll('.nav-btn').forEach((btn,i)=>btn.classList.toggle('active',i===n));
  render();
  window.scrollTo({{top:0,behavior:'smooth'}});
}}
function render(){{
  const s=document.getElementById('search').value.toLowerCase();
  const c=document.getElementById('content');
  let h='';
  const chs=currentChapter===0?book.chapters:[book.chapters[currentChapter-1]];
  chs.forEach(ch=>{{
    const ins=insights.find(i=>i.chapter===ch.chapter);
    h+='<div class="card"><div class="ch-h" style="background:'+ch.color+'"><span class="ch-icon">'+ch.icon+'</span><div class="ch-num">Chapter '+ch.chapter+'</div><div class="ch-title">'+ch.title+'</div>'+(ins?'<div class="ch-sub">'+ins.headline+'</div>':'')+'</div>';
    h+='<div class="ch-body">';
    if(ins){{
      h+='<div class="quote" style="border-color:'+ins.color+'"><b>Proverbs Says:</b> '+ins.proverbs_says+'</div>';
      h+='<div class="tags">'+ins.key_points.map(p=>'<span class="tag">'+p+'</span>').join('')+'</div>';
    }}
    h+='<div class="count">'+ch.section_count+' Financial Wisdom Sections</div>';
    const filtered=ch.sections.filter(sec=>{{
      if(!s)return true;
      return sec.text.toLowerCase().includes(s)||sec.title.toLowerCase().includes(s)||sec.range.toLowerCase().includes(s)||sec.financial_concepts.some(con=>con.toLowerCase().includes(s));
    }});
    filtered.forEach(sec=>{{
      h+='<div class="vs"><div class="vh"><span class="vt">'+sec.title+'</span><span class="vr">'+sec.range+'</span></div>';
      h+='<div class="vtext">'+sec.text+'</div>';
      h+='<div class="vc">'+sec.financial_concepts.map(con=>'<span class="ct">'+con+'</span>').join('')+'</div></div>';
    }});
    h+='</div></div>';
  }});
  c.innerHTML=h||'<p style="color:white;text-align:center;padding:2rem">No results</p>';
}}
init();
</script></body></html>'''

with open('proverbs_complete.html', 'w') as f:
    f.write(html)

print('Created proverbs_complete.html (all 238 sections)')
