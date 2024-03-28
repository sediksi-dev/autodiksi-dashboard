import streamlit as st
from utils.page_header import page_header

st.set_page_config(
    page_title="Keyword Seeder - AGC Likrea Asisstant",
    page_icon=":robot:",
)

page_header(
    title="Test Keyword Seeder",
    description="Masukkan keyword yang ingin diuji untuk melihat hasil penulisan konten",
)


table_file = st.file_uploader(
    "Unggah file CSV atau Excel",
    type=["csv", "xlsx", "xls"],
    help="Upload file CSV atau Excel berisi kata kunci yang ingin ditambahkan ke antrian artikel. File harus memiliki kolom `keyword`",
)
