import streamlit as st
from utils.page_header import page_header
from utils.state.seeder import SingleSeedArticle

st.set_page_config(
    page_title="Keyword Seeder - AGC Likrea Asisstant",
    page_icon=":robot:",
)

page_header(
    title="Test Keyword Seeder",
    description="Masukkan keyword yang ingin diuji untuk melihat hasil penulisan konten",
)


seeder = SingleSeedArticle()
seeder.start()


def update_text_input(key):
    seeder.set(key, st.session_state[f"__{key}__"])


def generating():
    st.switch_page("pages/seeder_article_test_1_generate.py")


with st.form(key="__article_seeder_form__"):
    keyword = st.text_input(
        "Keyword",
        placeholder="Masukkan keyword yang ingin diuji",
        key="__keyword__",
        value=seeder.get("keyword"),
    )
    language = st.selectbox(
        "Bahasa",
        ["Indonesia", "Inggris"],
        key="__language__",
        index=0 if seeder.get("language") == "Indonesia" else 1,
    )
    generate = st.form_submit_button(
        "Generate",
        use_container_width=True,
        type="primary",
    )

if generate:
    if keyword == "":
        st.warning("Keyword tidak boleh kosong")
        st.stop()
    update_text_input("keyword")
    update_text_input("language")
    generating()
