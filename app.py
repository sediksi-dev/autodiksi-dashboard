import streamlit as st

if "auth" not in st.session_state:
    st.session_state.auth = False

st.set_page_config(
    page_title="AGC Likrea Assistant",
    initial_sidebar_state="collapsed",
    page_icon=":robot:",
)


st.title("AGC Likrea Assistant")
st.write(
    "Aplikasi ini dibuat untuk membantu kru dalam melakukan manajemen data sumber dan target website Automatic Content Generator (AGC) milik Likrea. Untuk memulai, silahkan login dengan menekan tombol `MASUK`di bawah ini."
)

st.subheader("Login")
username = st.text_input("Username")
password = st.text_input("Password", type="password")
login_button = st.button("Login")

if login_button:
    if username == "admin" and password == "admin":
        st.session_state.auth = True
        st.switch_page("pages/dashboard.py")
    else:
        st.error("Username atau password salah.")
