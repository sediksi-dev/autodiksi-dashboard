import streamlit as st
from menu import menu


def page_header(**kwargs):
    title = kwargs.get("title", "Selamat datang di AGC Likrea Assistant.")
    description = kwargs.get(
        "description",
        "Aplikasi ini dibuat untuk membantu kru dalam melakukan manajemen data sumber dan target website Automatic Content Generator (AGC) milik Likrea. Silahkan pilih menu yang ingin Anda akses di sidebar.",
    )
    menu()
    st.title(title)
    st.write(description)
