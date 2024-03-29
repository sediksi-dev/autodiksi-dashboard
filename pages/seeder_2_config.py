import streamlit as st
from utils.page_header import page_header
from utils.state.seeder import SeederKeywords
from utils.navigation_button import navigation_button as nav, NavigationButton

st.set_page_config(
    page_title="Keyword Seeder - AGC Likrea Asisstant",
    page_icon=":robot:",
)

page_header(
    title="Test Keyword Seeder",
    description="Masukkan keyword yang ingin diuji untuk melihat hasil penulisan konten",
)

seeder = SeederKeywords()


language = st.text_input(
    "Pilih bahasa yang diinginkan",
    key="__language__",
    placeholder="Misal: Indonesia",
)

col1, col2, col3 = st.columns([1, 1, 1])
start_date = col1.date_input(
    "Pilih tanggal mulai publikasi",
    key="__start_date__",
    help="Tanggal mulai publikasi artikel",
)

time_skip_start = col2.time_input(
    "Pilih waktu mulai publikasi",
    key="__time_skip_start__",
    help="Artikel akan mulai dipublikasi setelah waktu ini",
)

time_skip_end = col3.time_input(
    "Pilih waktu akhir publikasi",
    key="__time_skip_end__",
    help="Artikel akan berhenti dipublikasi setelah waktu ini",
)

post_interval = st.number_input(
    "Pilih interval waktu (dalam menit)",
    key="__post_interval__",
    help="Interval waktu antara setiap publikasi artikel (dalam menit)",
    step=5,
)


rewrite_mode = st.radio(
    "Pilih mode penulisan ulang (Hanya tersedia untuk mode 'default')",
    key="__rewrite_mode__",
    options=["default", "none", "spintax"],
    index=0,
    disabled=True,
    horizontal=True,
    help="Mode penulisan ulang artikel yang diinginkan",
)


nav(
    prev=NavigationButton(
        text="Sebelumnya",
        target="seeder_1_webtarget.py",
    ),
    next=NavigationButton(
        text="Selanjutnya",
        target="seeder_2_config.py",
        type="primary",
    ),
)
