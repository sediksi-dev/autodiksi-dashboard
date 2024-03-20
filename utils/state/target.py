import streamlit as st


class WebTarget:
    def __init__(self):
        if "target" not in st.session_state:
            st.session_state.target = {}

    def start(self):
        self.set("url", "")
        self.set("categories", [])

    def set(self, key, value):
        st.session_state.target[key] = value

    def get(self, key, default_return=None):
        if key not in st.session_state.target:
            st.session_state.target[key] = None

        if st.session_state.target[key]:
            return st.session_state.target[key]
        else:
            return default_return
