import base64, json
with open('articles.json','rb') as f: data=f.read()
b64=base64.b64encode(data).decode('ascii')
with open('index.html','r',encoding='utf-8') as f: html=f.read()
# Replace ARTICLES_DATA line with base64 variant
old = 'const ARTICLES_DATA = ' + json.dumps(data)[:30] + '...'
new = 'const ARTICLES_B64 = "' + b64[:100] + '..."'
html = html.replace(old, new)
with open('index.html','w',encoding='utf-8') as f: f.write(html)
print('done len=', len(b64))
