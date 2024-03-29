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


def update_input(key):
    seeder.set_config(key, st.session_state[f"__{key}__"])


target_web_url = st.text_input(
    "Pilih web target",
    key="__target_web_url__",
    placeholder="Misal: example.com",
    help="Alamat web target yang akan dijadikan tempat publikasi artikel. Diisi tanpa tanda petik, garis miring, atau protokol (http/https)",
    on_change=lambda: update_input("target_web_url"),
    value=seeder.get_config("target_web_url"),
)


target_web_username = st.text_input(
    "Masukkan username web target",
    key="__target_web_username__",
    placeholder="Misal: user123",
    help="Username untuk login ke web target. Harus diisi dengan username yang terdaftar di web target",
    on_change=lambda: update_input("target_web_username"),
    value=seeder.get_config("target_web_username"),
)


target_web_password = st.text_input(
    "Masukkan password web target",
    key="__target_web_password__",
    placeholder="Masukkan password",
    help="Password untuk login ke web target. Untuk mendapatkan password, kunjungi `User >> Profile >> Add New Password` di web target",
    on_change=lambda: update_input("target_web_password"),
    value=seeder.get_config("target_web_password"),
)


nav(
    prev=NavigationButton(
        text="Sebelumnya",
        target="seeder_0_main.py",
    ),
    next=NavigationButton(
        text="Selanjutnya",
        target="seeder_2_config.py",
        type="primary",
    ),
)
