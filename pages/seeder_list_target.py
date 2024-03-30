import streamlit as st
import pandas as pd
from utils.page_header import page_header
from utils.supabase import SupaSeedTarget

st.set_page_config(
    page_title="Keyword Seeder - AGC Likrea Asisstant",
    page_icon=":robot:",
)

page_header(
    title="Test Keyword Seeder",
    description="Masukkan keyword yang ingin diuji untuk melihat hasil penulisan konten",
)

supa = SupaSeedTarget()
try:
    data = supa.getAll()
    if not data or len(data) == 0:
        st.warning("Data target masih kosong")
    else:
        df = pd.DataFrame(data)
        df = df.drop(columns=["password"])
        df["no"] = range(1, len(df) + 1)
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "no": st.column_config.NumberColumn(
                    "No.",
                    width=10,
                ),
                "url": st.column_config.TextColumn(
                    "URL",
                ),
                "username": st.column_config.TextColumn(
                    "Username",
                ),
                "api_endpoint": st.column_config.TextColumn(
                    "API Endpoint",
                ),
                "post_type": st.column_config.TextColumn(
                    "Post Type",
                ),
            },
            column_order=["no", "url", "username", "api_endpoint", "post_type"],
        )
except Exception as e:
    st.error(f"Data gagal diambil: {e}")
