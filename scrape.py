import urllib.request, xml.etree.ElementTree as ET, json, datetime, re
feeds = [
  "https://feeds.bbci.co.uk/news/world/rss.xml","https://feeds.bbci.co.uk/news/technology/rss.xml","https://feeds.bbci.co.uk/news/science_and_environment/rss.xml","https://feeds.bbci.co.uk/news/health/rss.xml","https://feeds.bbci.co.uk/news/business/rss.xml","https://feeds.bbci.co.uk/news/politics/rss.xml","https://feeds.bbci.co.uk/news/uk/rss.xml","https://feeds.nbcnews.com/nbcnews/public/news","https://feeds.cbsnews.com/news/cbsnews/world","https://feeds.foxnews.com/foxnews/world","https://edition.cnn.com/services/rss/edition_world.rss","https://feeds.npr.org/1001/rss.xml","https://feeds.reuters.com/reuters/topNews","https://feeds.a.dj.com/rss/RSSWorldNews.xml","https://feeds.feedburner.com/techcrunch/","https://feeds.arstechnica.com/arstechnica/index","https://www.wired.com/feed/rss","https://www.nytimes.com/svc/collections/v1/publish/https://www.nytimes.com/section/world/rss.xml","https://feeds.washingtonpost.com/rss/world","https://globalnews.ca/world/feed/","https://www.buenosairesherald.com/rss","https://www.theguardian.com/world/rss","https://www.france24.com/en/rss","https://www.spiegel.de/international/index.rss","https://www.euronews.com/rss?format=mrss&level=theme&name=news","https://www.independent.co.uk/news/world/rss","https://feeds.dw.com/rdf/rss-en-world","https://www.lemonde.fr/rss/planete.xml","https://elpais.com/rss/cualeser_usa.xml","https://www.aljazeera.com/xml/rss/all.xml","https://www.japantimes.co.jp/feed/top-stories/","https://www.scmp.com/rss/91/feed","https://timesofindia.indiatimes.com/rssfeeds/296589292.cms","https://mg.co.za/feed/","https://www.dailynewsegypt.com/feed/","https://www.smh.com.au/rss/world.xml","https://feeds.reuters.com/reuters/businessNews","https://feeds.feedburner.com/TheEconomist","https://www.chinadaily.com.cn/rss/world.xml","https://www.asahi.com/ajw/rss/","https://www.timesofisrael.com/feed/","https://feed.feedburner.com/africanews/?format=xml"
]
articles=[]
for url in feeds:
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            data=resp.read()
        root=ET.fromstring(data)
        ns={'content':'http://purl.org/rss/1.0/modules/content/'}
        for item in root.iter('item'):
            title=item.findtext('title') or 'No Title'
            link=item.findtext('link') or '#'
            desc=item.findtext('description') or item.findtext('summary') or ''
            # content:encoded
            ce=item.find('content:encoded', ns)
            if ce is not None and ce.text:
                desc = ce.text
            desc = re.sub(r'<[^>]+>', '', desc).strip()
            pub=item.findtext('pubDate') or ''
            feed_name = root.findtext('.//{http://www.w3.org/2005/Atom}title') or root.findtext('.//title') or url
            articles.append({'title':title,'link':link,'summary':desc or 'No summary.','source':feed_name,'date':pub,'id':str(len(articles))})
    except Exception as e:
        print('skip', url, e)
articles.sort(key=lambda x: x['date'] or '', reverse=True)
with open('articles.json','w',encoding='utf-8') as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)
print('scraped', len(articles))
