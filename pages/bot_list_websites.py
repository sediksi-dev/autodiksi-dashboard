import streamlit as st
import pandas as pd
from utils.page_header import page_header
from utils.supabase import SupaListWebHandler

st.set_page_config(
    page_title="Daftar Situs - AGC Likrea Assistant",
    page_icon=":robot:",
)

page_header(
    title="Daftar Situs Terdaftar",
    description="Berikut adalah daftar situs yang terdaftar pada Bot AGC Likrea.",
)

supa = SupaListWebHandler()
tab1, tab2 = st.tabs(["Daftar Situs", "Daftar Artikel Terpublikasi"])


web = list(supa.get_websites_mapping())
web_df = pd.DataFrame(web)
tab1.text("Daftar situs yang terdaftar pada Bot AGC Likrea.")
tab1.dataframe(
    web_df,
    hide_index=True,
    use_container_width=True,
    column_config={
        "source_url": st.column_config.TextColumn(label="URL Sumber"),
        "target_url": st.column_config.TextColumn(label="URL Tujuan"),
        "source_category": st.column_config.TextColumn(label="Kategori Sumber"),
        "target_category": st.column_config.TextColumn(label="Kategori Tujuan"),
    },
)


def get_host(url):
    return url.split("//")[-1].split("/")[0]


def get_slug(url):
    if url[-1] == "/":
        url = url[:-1]
    return url.split("/")[-1]


articles_db = supa.get_article_by_status("published")
articles = {
    "published_date": [a["published_date"] for a in articles_db],
    "source_slug": [get_slug(a["source_url"]) for a in articles_db],
    "public_slug": [get_slug(a["public_url"]) for a in articles_db],
    "source_url": [a["source_url"] for a in articles_db],
    "public_url": [a["public_url"] for a in articles_db],
}
articles_df = pd.DataFrame(articles)[
    [
        "source_slug",
        "source_url",
        "public_slug",
        "public_url",
        "published_date",
    ]
].sort_values("published_date", ascending=False)
tab2.text("Daftar artikel yang telah terpublikasi.")
tab2.dataframe(
    articles_df,
    use_container_width=True,
    column_config={
        "published_date": st.column_config.DatetimeColumn(
            label="Tanggal Publikasi", format="DD/MM/YYYY HH:mm"
        ),
        "source_slug": st.column_config.TextColumn(label="Slug Sumber"),
        "source_url": st.column_config.LinkColumn(
            label="URL Sumber", display_text="Kunjungi"
        ),
        "public_slug": st.column_config.TextColumn(label="Slug Publikasi"),
        "public_url": st.column_config.LinkColumn(
            label="URL Publikasi", display_text="Kunjungi"
        ),
    },
)
