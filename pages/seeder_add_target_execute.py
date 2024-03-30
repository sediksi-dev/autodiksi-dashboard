import streamlit as st
from utils.page_header import page_header
from utils.state.seeder import SeederTarget
from utils.supabase import SupaSeedTarget

# from utils.navigation_button import navigation_button as nav, NavigationButton

st.set_page_config(
    page_title="Keyword Seeder - AGC Likrea Asisstant",
    page_icon=":robot:",
)

page_header(
    title="Tambahkan Web dan User Target",
    description="Masukkan web dan target user yang akan digunakan sebagai tempat publikasi artikel.",
)

seeder = SeederTarget()
supa = SupaSeedTarget()

with st.status("Menyimpan data...", expanded=False, state="running"):
    try:
        data = supa.add(seeder.getAll())
        if data:
            seeder.reset()
            st.success("Data berhasil disimpan")
            st.switch_page("pages/seeder_list_target.py")
    except Exception as e:
        st.error(f"Data gagal disimpan: {e}")
