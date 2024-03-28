import streamlit as st

from utils.page_header import page_header
from utils.wp_handler import check_all_term
from utils.state.bot import WebSource
from utils.navigation_button import navigation_button as nav, NavigationButton

st.set_page_config(
    page_title="Cek Kategori By URL - AGC Likrea Assistant",
    page_icon=":robot:",
)

page_header(
    title="Cek Kategori By URL",
    description="Masukkan URL artikel yang ingin dicek kategorinya.",
)

source = WebSource()

st.subheader(f"Cek kategori di {source.get('url')} ")
msg = st.empty()
box = st.empty()


def check_categories():
    box.empty()
    with box.container():
        with st.spinner("Checking categories for the source..."):
            try:
                list_categories = check_all_term(source.get("url"), "categories")
                if list_categories is None or "data" not in list_categories:
                    raise Exception()
                msg.success("Success checking categories for the source.")
                source.set("categories", list_categories["data"])
                return True, list_categories
            except Exception as e:
                msg.error(f"Error checking categories for the source.\n{e}")
                return False, None


state_result, list_categories = check_categories()
if not state_result:
    recheck_button = st.button("Coba lagi")

if state_result and list_categories:
    categories = source.get("categories")
    total_categories = len(categories)
    disable_next = total_categories == 0
    st.write(f"Founds {len(categories)} categories for {source.get('url')}")
    nav(
        prev=NavigationButton(target="bot_1_check_sources.py"),
        next=NavigationButton(
            text="Selanjutnya",
            type="primary",
            target="bot_3_pick_categories.py",
            config={"disabled": disable_next},
        ),
    )
