import streamlit as st
from utils.page_header import page_header
from utils.wp_handler import check_is_wp
from utils.state.source import WebSource as Source
from utils.navigation_button import navigation_button as nav

st.set_page_config(
    page_title="Cek Situs Sumber - AGC Likrea Assistant",
    page_icon=":robot:",
)

page_header(
    title="Cek Situs Sumber",
    description="Masukkan URL situs sumber untuk mengecek apakah situs tersebut dapat menjadi sumber konten AGC Likrea.",
)

source = Source()


def display_form():
    with st.form(key="source_url_check_form"):
        url = st.text_input(
            "Masukkan URL situs sumber",
            placeholder="contoh: sediksi.com",
            help="Jangan diawali dengan https:// atau http:// dan jangan akhiri dengan /",
            value=st.session_state.source.get("url", ""),
        )

        submit = st.form_submit_button(
            "Cek Situs Sumber",
            use_container_width=True,
            type="primary",
        )

        return url, submit


def check_url(url, result_container=None, info_container=None):
    result_container.empty()
    if len(url) > 0:
        try:
            check_is_wp(url)
            if info_container:
                info_container.success(
                    ":white_check_mark: Situs dapat dijadikan sumber konten AGC Likrea."
                )
            source.set("is_wp", True)
        except Exception as e:
            if info_container:
                info_container.error(
                    f":x: Situs tidak dapat dijadikan sumber konten AGC Likrea.\n{e}"
                )
            source.set("is_wp", False)
    else:
        source.set("is_wp", False)
    return source.get("is_wp")


url, submitted = display_form()
msg_container = st.empty()
nav_container = st.container()

if len(url) > 0 and submitted:
    is_wp = check_url(url, info_container=msg_container, result_container=nav_container)

if source.get("is_wp"):
    source.set("url", url)
    with nav_container:
        nav(
            prev={
                "text": "Sebelumnya",
                "target": "add_website_main.py",
                "config": {"disabled": not source.get("is_wp")},
            },
            next={
                "text": "Selanjutnya",
                "target": "add_website_step_2_check_categories.py",
                "type": "secondary",
                "config": {"disabled": not source.get("is_wp")},
            },
        )
