import json
with open('articles.json','r',encoding='utf-8') as f:
    articles = json.load(f)
with open('index.html','r',encoding='utf-8') as f:
    html = f.read()
old_block = "function loadFromJSON(){\n  fetch('./articles.json',{cache:'no-store'}).then(r=>r.json()).then(data=>{\n    allArticles=data.sort((a,b)=>new Date(b.date||0)-new Date(a.date||0));\n    document.getElementById('status').textContent=`Displaying ${allArticles.length} articles.`;\n    document.getElementById('lastLoad').textContent=new Date().toLocaleString();\n    buildTags();\n    renderPage(allArticles,currentPage);\n  }).catch(e=>{document.getElementById('status').textContent='Failed to load articles.json. Refresh to retry.';console.error(e);});\n}"
new_block = "function loadFromJSON(){\n  allArticles=ARTICLES_DATA.sort((a,b)=>new Date(b.date||0)-new Date(a.date||0));\n  document.getElementById('status').textContent=`Displaying ${allArticles.length} articles.`;\n  document.getElementById('lastLoad').textContent=new Date().toLocaleString();\n  buildTags();\n  renderPage(allArticles,currentPage);\n}"
html = html.replace(old_block, new_block)
injection = 'const ARTICLES_DATA = ' + json.dumps(articles) + ';\n'
html = html.replace('function loadFromJSON(){', injection + 'function loadFromJSON(){')
with open('index.html','w',encoding='utf-8') as f:
    f.write(html)
print('done', len(articles), len(html))
