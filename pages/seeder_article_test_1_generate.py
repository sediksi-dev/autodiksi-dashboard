import streamlit as st
import urllib.parse as urlparse
import os
from dotenv import load_dotenv


import requests
from requests.auth import HTTPBasicAuth
from utils.state.seeder import SingleSeedArticle
from utils.page_header import page_header

load_dotenv()

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

url = os.environ.get("AGC_API_URL")
username = os.environ.get("AGC_API_USERNAME")
password = os.environ.get("AGC_API_PASSWORD")


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
    title = article["title"] if article["title"] else "No Title"
    body = article["article"] if article["article"] else "No Article"

    full_article = image_css + f"# {title}\n{body}"
    view, raw = st.tabs(["View Article", "Raw"])
    view.markdown(full_article, unsafe_allow_html=True)
    with raw.container(height=400) as raw:
        st.code(article["article"], line_numbers=False, language="markdown")
else:
    with st.status("Generating Article", state="running"):
        response = requests.post(
            full_url,
            auth=HTTPBasicAuth(username, password),
        )

        if response.status_code == 200:
            data = response.json()
            seeder.set("article_data", data["data"])
            st.rerun()
        else:
            st.error("Failed to generate article")
            st.write(response.text)
