import streamlit as st
from dotenv import load_dotenv
import pandas as pd
import requests, json, os, time, feedparser
load_dotenv("app.env")

OLLAMA = os.get_env("OLLAMA")
MODEL = os.get_env("MODEL")
RSS_MAP = {
    "q-fin": "https://export.arxiv.org/rss/q-fin ",
    "cs.LG": "https://export.arxiv.org/rss/cs.LG",
    "stat.ML": "https://export.arxiv.org/rss/stat.ML"
}


def ollama_summary(text:str) -> str:
    r = requests.post(f"{OLLAMA}/api/generate",
        json = {"model": MODEL,
                "prompt": f"generate one sentence summary of the following content, and only print one sentence:\n{text}"
                "temperature": .3,
                "stream": false,
        },
        timeout=120)
    r.raise_for_status()
    return r.json().strip()

@st.cache_data(ttl=3600)
def fetch_(feeds, max_n):
    rows=[]
    for tag in feeds:
        for e in freepsrser.parse([RSS_MAP[tag]]).entries[:max_n]:
            abs_=e.summary.replace("\n", " ")
            rows.append({"date":e.published[:10],
                         "title": e.title,
                         "authors": })

