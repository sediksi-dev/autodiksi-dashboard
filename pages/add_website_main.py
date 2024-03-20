import streamlit as st
from utils.page_header import page_header
from utils.state.source import WebSource as Source
from utils.state.target import WebTarget as Target

st.set_page_config(
    page_title="Tambah Website - AGC Likrea Asisstant",
    page_icon=":robot:",
)

page_header(
    title="Tambah Website",
    description="Masukkan URL situs sumber untuk mengecek apakah situs tersebut dapat menjadi sumber konten AGC Likrea.",
)

source = Source()
target = Target()
source.start()
target.start()

start_button = st.button("Selanjutnya", use_container_width=True)

if start_button:
    st.switch_page("pages/add_website_step_1_check_sources.py")
