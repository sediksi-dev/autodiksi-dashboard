import streamlit as st
import pandas as pd
from utils.page_header import page_header
from utils.navigation_button import navigation_button as nav
from utils.state.source import WebSource as Source

st.set_page_config(
    page_title="Pilih kategori - AGC Likrea Assistant",
    page_icon=":robot:",
)

page_header(
    title="Cek Kategori By URL",
    description="Pilih kategori yang sesuai dengan artikel yang ingin dijadikan sumber konten AGC Likrea.",
)


source = Source()


def show_dataframe():
    categories = source.get("categories")
    df = pd.DataFrame(categories)
    df = df[["id", "name", "slug", "total", "link"]]

    df.sort_values("total", ascending=False, inplace=True)
    st.dataframe(
        df,
        hide_index=True,
        use_container_width=True,
        column_config={
            "id": st.column_config.NumberColumn(
                label="ID",
                format="%d",
            ),
            "name": st.column_config.TextColumn(
                label="Nama Kategori",
            ),
            "slug": st.column_config.TextColumn(
                label="Slug",
            ),
            "total": st.column_config.NumberColumn(
                label="Total Artikel",
                # Output: 1.333 Posts. Expected: 1.333 Posts
                format="%0f Posts",
            ),
            "link": st.column_config.LinkColumn(
                label="Link", help="Kunjungi untuk melihat contoh-contoh artikel"
            ),
        },
    )


def select_categories():
    selected = source.get("selected_categories")
    categories = source.get("categories")
    if categories:
        selected_categories = st.multiselect(
            "Pilih kategori yang sesuai",
            options=[c["slug"] for c in categories],
            help="Pilih satu atau lebih kategori yang sesuai dengan artikel yang ingin dihasilkan.",
            label_visibility="collapsed",
            default=[c["slug"] for c in selected] if selected else None,
        )
        return selected_categories


def save_categories(selected):
    categories = source.get("categories")
    selected_data = [c for c in categories if c["slug"] in selected]
    source.set("selected_categories", selected_data)


selected = select_categories()
with st.expander("Lihat Semua Kategori", expanded=True):
    show_dataframe()

nav(
    prev={
        "target": "add_website_step_1_check_sources.py",
    },
    next={
        "target": "add_website_step_4_config_target.py",
        "type": "primary",
        "config": {"disabled": len(selected) == 0},
        "callbacks": lambda: save_categories(selected),
    },
)
