import feedparser

url = "http://rss.arxiv.org/rss/q-fin"
feed = feedparser.parse(url)
print(f"Entries found: {len(feed.entries)}")
for entry in feed.entries[:2]:
    print("Title:", entry.title)