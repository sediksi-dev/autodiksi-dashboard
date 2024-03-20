import streamlit as st
from utils.page_header import page_header

st.set_page_config(
    page_title="Dashboard - AGC Likrea Assistant",
    page_icon=":robot:",
)

page_header(
    title="Dashboard",
    description="Selamat datang di halaman dashboard AGC Likrea Assistant.",
)
