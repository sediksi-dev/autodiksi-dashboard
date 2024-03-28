import streamlit as st
import urllib.parse as urlparse

import requests
from requests.auth import HTTPBasicAuth
from utils.state.seeder import SingleSeedArticle
from utils.page_header import page_header


st.set_page_config(
    page_title="Generator - AGC Likrea Asisstant",
    page_icon=":robot:",
)

page_header(
    title="Generate Article from Keyword",
    description="Masukkan keyword yang ingin diuji untuk melihat hasil penulisan konten",
)


seeder = SingleSeedArticle()
keyword = seeder.get("keyword")
language = seeder.get("language")
article = seeder.get("article_data")

url = st.secrets["agc_api"]["url"]
username = st.secrets["agc_api"]["username"]
password = st.secrets["agc_api"]["password"]


full_url = (
    f"{url}/seeder/generate/"
    + f"?keyword={urlparse.quote(keyword)}&lang_target={urlparse.quote(language)}"
)
if article:
    image_css = """<style>
    img {
        max-width: 100%;
        height: auto;
    }
    </style>\n\n"""

    full_article = image_css + f"# {article['title']}\n\n{article['article']}"
    view, raw = st.tabs(["View Article", "Raw"])
    view.markdown(full_article, unsafe_allow_html=True)
    raw.code(article["article"], line_numbers=False, language="markdown")
else:
    with st.status("Generated Article", state="running"):
        response = requests.post(
            full_url,
            auth=HTTPBasicAuth(username, password),
        )

        if response.status_code == 200:
            data = response.json()
            seeder.set("article_data", data)
            st.rerun()
        else:
            st.error("Failed to generate article")
            st.write(response.text)
