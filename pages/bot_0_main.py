import streamlit as st
from utils.page_header import page_header
from utils.state.bot import WebSource, WebTarget, WebConfig

st.set_page_config(
    page_title="Tambah Website - AGC Likrea Asisstant",
    page_icon=":robot:",
)

page_header(
    title="Tambah Website",
    description="Masukkan URL situs sumber untuk mengecek apakah situs tersebut dapat menjadi sumber konten AGC Likrea.",
)

source = WebSource()
target = WebTarget()
config = WebConfig()

source.start()
target.start()
config.start()

start_button = st.button("Lanjutkan", use_container_width=True, type="primary")

if start_button:
    st.switch_page("pages/bot_1_check_sources.py")
