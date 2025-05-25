import streamlit as st
from dotenv import load_dotenv
import pandas as pd
import requests, json, os, time, feedparser
load_dotenv("app.env")

rss = feedparser.parse("https://export.arxiv.org/rss/cs.LG")
print(f"Entries found: {len(rss.entries)}")
for entry in rss.entries[:5]:
    print(entry.title)
del rss
OLLAMA = os.getenv("OLLAMA")
MODEL = os.getenv("MODEL")
RSS_MAP = {
    "q-fin": os.getenv("QFIN"),
    "cs.LG": os.getenv("CSLG"),
    "stat.ML": os.getenv("STATML")
}



def ollama_summary(text: str) -> str:
    try:
        r = requests.post(
            f"{OLLAMA}/api/generate",
            json={
                "model": MODEL,
                "prompt": f"generate one sentence summary of the following content, and only print one sentence:\n{text}",
                "temperature": 0.3,
                "stream": False,
            },
            timeout=120,
        )
        r.raise_for_status()
        return r.json().get("response", "").strip()
    except Exception as e:
        print(f"Error in summary generation: {e}")
        return "Summary unavailable."



@st.cache_data(ttl=3600)
def fetch_papers(feeds, max_n):
    rows=[]
    for tag in feeds:
        for e in feedparser.parse(RSS_MAP[tag]).entries[:max_n]:
            abs_=e.summary.replace("\n", " ")
            rows.append(
                {
                    "date":e.published[:10],
                    "title": e.title,
                    "authors": ", ".join(a.name for a in e.authors),
                    "link": e.link,
                    "summary": ollama_summary(abs_)
                }
            )
            time.sleep(.1)
    return pd.DataFrame(rows)


st.sidebar.title("AI-strategy-detector")
sel = st.sidebar.multiselect("Feeds", list(RSS_MAP), ["q-fin", "cs.LG"])
max_n = st.sidebar.slider("Papers per feed", 10, 50)
if st.sidebar.button("Refresh Feed"):
    st.cache_data.clear()

df = fetch_papers(tuple(sel), max_n)
querry = st.text_input("Filter")
if querry:
    df = df[df["summary"].str.contains(querry, case=False) | df["title"].str.contains(querry, case=False)]

st.dataframe(df)
csv = df.to_csv(index=False, encoding="utf-8-sig")
st.download_button("Download CSV", csv, "arxiv_summary.csv")
st.caption("Summaries with Gemma 1b in ollama")
