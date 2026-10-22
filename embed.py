import json
with open('articles.json','r',encoding='utf-8') as f:
    articles = json.load(f)
with open('index.html','r',encoding='utf-8') as f:
    html = f.read()
old_body = """  fetch('./articles.json',{cache:'no-store'}).then(r=>r.json()).then(data=>{
    allArticles=data.sort((a,b)=>new Date(b.date||0)-new Date(a.date||0));
    document.getElementById('status').textContent=`Displaying ${allArticles.length} articles.`;
    document.getElementById('lastLoad').textContent=new Date().toLocaleString();
    buildTags();
    renderPage(allArticles,currentPage);
  }).catch(e=>{document.getElementById('status').textContent='Failed to load articles.json. Refresh to retry.';console.error(e);});"""
new_body = """  allArticles=ARTICLES_DATA.sort((a,b)=>new Date(b.date||0)-new Date(a.date||0));
  document.getElementById('status').textContent=`Displaying ${allArticles.length} articles.`;
  document.getElementById('lastLoad').textContent=new Date().toLocaleString();
  buildTags();
  renderPage(allArticles,currentPage);"""
html = html.replace(old_body, new_body)
# Insert ARTICLES_DATA before loadFromJSON
injection = 'const ARTICLES_DATA = ' + json.dumps(articles) + ';\n'
html = html.replace('function loadFromJSON(){', injection + 'function loadFromJSON(){')
with open('index.html','w',encoding='utf-8') as f:
    f.write(html)
print('embedded', len(articles))
