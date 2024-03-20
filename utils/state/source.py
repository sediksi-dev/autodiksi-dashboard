import streamlit as st


class WebSource:
    def __init__(self):
        if "source" not in st.session_state:
            st.session_state.source = {}

    def start(self):
        self.set("is_wp", False)
        self.set("url", "")
        self.set("categories", [])
        self.set("selected_categories", [])

    def set(self, key, value):
        st.session_state.source[key] = value

    def get(self, key):
        if key not in st.session_state.source:
            return None
        return st.session_state.source[key]

    def reset(self):
        st.session_state.source = {}

    def reset_and_set_url(self, value):
        st.cache_data.clear()
        self.reset()
        self.set("url", value)
