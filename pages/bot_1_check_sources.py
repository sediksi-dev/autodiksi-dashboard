import streamlit as st

from utils.page_header import page_header
from utils.wp_handler import check_is_wp
from utils.state.bot import WebSource, WebTarget
from utils.navigation_button import navigation_button as nav, NavigationButton

st.set_page_config(
    page_title="Cek Situs Sumber - AGC Likrea Assistant",
    page_icon=":robot:",
)

page_header(
    title="Cek Situs Sumber",
    description="Masukkan URL situs sumber untuk mengecek apakah situs tersebut dapat menjadi sumber konten AGC Likrea.",
)

source = WebSource()
target = WebTarget()


def display_form():
    """Display form for checking source URL
    Returns:
        tuple: URL and submit button status
    """

    with st.form(key="source_url_check_form"):
        url = st.text_input(
            "Masukkan URL situs sumber",
            placeholder="contoh: sediksi.com",
            help="Jangan diawali dengan https:// atau http:// dan jangan akhiri dengan /",
            value=source.get("url"),
        )

        submit = st.form_submit_button(
            "Cek Situs Sumber",
            use_container_width=True,
            type="primary",
        )

        return url, submit


def check_url(url, result_container=None, info_container=None):
    """Check if the URL is a valid WordPress site

    Args:
        url (str): URL of the source website
        result_container (st.empty, optional): Container for displaying the result. Defaults to None.
        info_container (st.empty, optional): Container for displaying the info message. Defaults to None.

    Returns:
        bool: True if the URL is a valid WordPress site, False otherwise
    """

    result_container.empty()
    if len(url) > 0:
        try:
            is_wp = check_is_wp(url)
            if not is_wp:
                source.set("is_wp", False)
                raise Exception("Error ketika mengecek situs")
            else:
                source.set("is_wp", True)
                if info_container:
                    info_container.success(
                        ":white_check_mark: Situs dapat dijadikan sumber konten AGC Likrea."
                    )
        except Exception as e:
            if info_container:
                info_container.error(
                    f":x: Situs tidak dapat dijadikan sumber konten AGC Likrea.\n{e}"
                )
            source.set("is_wp", False)
    else:
        source.set("is_wp", False)
    return source.get("is_wp")


def main():
    url, submitted = display_form()
    msg_container = st.empty()
    nav_container = st.container()

    if len(url) > 0 and submitted:
        try:
            check_url(url, info_container=msg_container, result_container=nav_container)
        except Exception as e:
            msg_container.error(f":x: {e}")

    if source.get("is_wp"):
        source.set("url", url)
        with nav_container:
            nav(
                prev=NavigationButton(
                    text="Sebelumnya",
                    target="bot_0_main.py",
                    config={"disabled": not source.get("is_wp")},
                ),
                next=NavigationButton(
                    text="Selanjutnya",
                    target="bot_2_check_categories.py",
                    type="primary",
                    config={"disabled": not source.get("is_wp")},
                ),
            )


main()
