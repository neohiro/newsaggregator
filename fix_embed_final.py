import json, base64

with open('articles.json','rb') as f:
    b64 = base64.b64encode(f.read()).decode('ascii')

with open('index.html','r',encoding='utf-8') as f:
    html = f.read()

# Replace loadFromJSON body with direct use of ARTICLES_B64
old = """function loadFromJSON(){
  document.getElementById('status').textContent='Fetching news, please wait…';
  document.getElementById('feed').innerHTML='<div class="skeleton"></div><div class="skeleton"></div><div class="skeleton"></div>';
  document.getElementById('pagination').innerHTML='';
  allArticles=[];isSearchActive=false;currentTag='';currentPage=1;document.getElementById('searchInput').value='';
  loadFromJSON();
}"""

# Wait, previous version had fetch from JSON. Let's just replace the fetch-based loadFromJSON with direct assignment from ARTICLES_B64
old_load = "function loadFromJSON(){\n  fetch('./articles.json',{cache:'no-store'}).then(r=>r.json()).then(data=>{\n    allArticles=data.sort((a,b)=>new Date(b.date||0)-new Date(a.date||0));\n    document.getElementById('status').textContent=`Displaying ${allArticles.length} articles.`;\n    document.getElementById('lastLoad').textContent=new Date().toLocaleString();\n    buildTags();\n    renderPage(allArticles,currentPage);\n  }).catch(e=>{document.getElementById('status').textContent='Failed to load articles.json. Refresh to retry.';console.error(e);});\n}"

new_load = """function loadFromJSON(){
  try{
    const data = JSON.parse(atob(ARTICLES_B64));
    allArticles = data.sort((a,b)=>new Date(b.date||0)-new Date(a.date||0));
    document.getElementById('status').textContent=`Displaying ${allArticles.length} articles.`;
    document.getElementById('lastLoad').textContent=new Date().toLocaleString();
    buildTags();
    renderPage(allArticles,currentPage);
  }catch(e){
    document.getElementById('status').textContent='Failed to load articles. Refresh to retry.';
    console.error(e);
  }
}"""

html = html.replace(old_load, new_load)
# Insert ARTICLES_B64 before loadFromJSON
html = html.replace('function loadFromJSON(){', 'const ARTICLES_B64 = "' + b64 + '";\nfunction loadFromJSON(){')

with open('index.html','w',encoding='utf-8') as f:
    f.write(html)

print('embedded base64 length', len(b64))
