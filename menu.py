import streamlit as st


def authenticated_menu():
    st.sidebar.title("Menu")
    st.sidebar.page_link("pages/dashboard.py", label="Dashboard")
    st.sidebar.divider()
    st.sidebar.subheader("Bot Likrea")
    st.sidebar.page_link("pages/list_websites.py", label="Daftar Situs")
    st.sidebar.page_link("pages/add_website_main.py", label="Tambah Situs")
    st.sidebar.page_link("pages/article_queue.py", label="Antrian Artikel")
    st.sidebar.page_link("pages/error_processed.py", label="Artikel Gagal Diproses")
    st.sidebar.divider()
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
