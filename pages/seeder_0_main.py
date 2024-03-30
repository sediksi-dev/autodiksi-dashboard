import streamlit as st
import pandas as pd
from utils.page_header import page_header
from utils.state.seeder import SeederKeywords

st.set_page_config(
    page_title="Keyword Seeder - AGC Likrea Asisstant",
    page_icon=":robot:",
)

page_header(
    title="Test Keyword Seeder",
    description="Masukkan keyword yang ingin diuji untuk melihat hasil penulisan konten",
)


seeder = SeederKeywords()
seeder.start()
st.cache_data.clear()

table_file = st.file_uploader(
    "Unggah file CSV dengan kolom `keywords`",
    type=["csv"],
    help="Upload file CSV berisi kata kunci yang ingin ditambahkan ke antrian artikel. File harus memiliki kolom `keywords`",
)

if table_file is not None:
    df = pd.read_csv(table_file)
    keywords = df["keywords"].tolist()
    seeder.set("keywords", keywords)


def reset_keywords():
    seeder.reset()


if len(seeder.get("keywords")) > 0:
    col1, col2 = st.columns([1, 1])
    with col1:
        st.button("Reset Keywords", on_click=seeder.reset, use_container_width=True)
    with col2:
        next_button = st.button("Selanjutnya", use_container_width=True, type="primary")

    if next_button:
        st.switch_page("pages/seeder_1_config.py")
