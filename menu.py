import streamlit as st


def bot_likrea_section():
    st.sidebar.divider()
    st.sidebar.subheader("Artikel Bot")
    st.sidebar.page_link("pages/list_websites.py", label="Daftar Situs")
    st.sidebar.page_link("pages/bot_0_main.py", label="Tambah Situs")
    st.sidebar.page_link("pages/article_queue.py", label="Antrian Artikel")
    st.sidebar.page_link("pages/error_processed.py", label="Artikel Gagal Diproses")


def likrea_article_generator():
    st.sidebar.divider()
    st.sidebar.subheader("Keyword Seeder")
    st.sidebar.page_link(
        "pages/keyword_seeder_article_test.py", label="Generator Artikel"
    )
    st.sidebar.divider()


def authenticated_menu():
    st.sidebar.title("Menu")
    st.sidebar.page_link("pages/dashboard.py", label="Dashboard")
    bot_likrea_section()
    likrea_article_generator()

    st.sidebar.button(
        "Logout",
        on_click=lambda: st.session_state.pop("auth"),
        use_container_width=True,
        type="primary",
    )


def menu():
    if "auth" not in st.session_state:
        st.session_state.auth = False

    if st.session_state.auth:
        authenticated_menu()
    else:
        st.switch_page("app.py")
