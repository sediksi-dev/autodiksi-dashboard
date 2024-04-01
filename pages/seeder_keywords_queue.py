import streamlit as st
import pandas as pd
from utils.page_header import page_header
from utils.supabase import SupaSeedKeywords

st.set_page_config(
    page_title="Keyword Seeder - AGC Likrea Asisstant",
    page_icon=":robot:",
)

page_header(
    title="Daftar Antrian Keyword",
    description="Masukkan keyword yang ingin diuji untuk melihat hasil penulisan konten",
)

supa = SupaSeedKeywords()
tab1, tab2 = st.tabs(["Draft", "Published"])

try:
    draft_keywords = supa.getAllWithChildren(status="draft")
    draft_keywords = [
        {
            "keywords": item["keywords"],
            "language": item["language"],
            "rewrite_date": item["rewrite_date"],
            "rewrite_mode": item["rewrite_mode"],
            "target_web": item["web"]["url"],
            "category": item["taxonomy"]["taxonomy_name"],
        }
        for item in draft_keywords
    ]

    df_draft = pd.DataFrame(draft_keywords).sort_values("rewrite_date", ascending=True)
    df_draft["number"] = range(1, len(df_draft) + 1)
    df_draft = df_draft[
        [
            "number",
            "keywords",
            "language",
            "rewrite_date",
            "rewrite_mode",
            "target_web",
            "category",
        ]
    ]

    tab1.dataframe(
        df_draft,
        hide_index=True,
        column_config={
            "keywords": st.column_config.TextColumn(
                "Kata Kunci",
            ),
            "language": st.column_config.TextColumn(
                "Bahasa",
            ),
            "rewrite_date": st.column_config.DatetimeColumn(
                "Tanggal Rewrite",
                format="DD-MM-YYYY HH:mm",
                help="Tanggal terakhir artikel di-rewrite",
            ),
            "rewrite_mode": st.column_config.TextColumn(
                "Mode Rewrite",
                help="Mode rewrite yang digunakan",
            ),
            "target_web": st.column_config.TextColumn(
                "Web Target",
                help="Web target tempat artikel akan dipublikasikan",
            ),
            "category": st.column_config.TextColumn(
                "Kategori",
                help="Kategori terpilih untuk artikel yang akan dihasilkan",
            ),
        },
    )
except Exception as e:
    tab1.warning(f"Tidak ada data yang dapat ditampilkan: {e}")

try:
    draft_keywords = supa.getAllWithChildren(status="published")
    draft_keywords = [
        {
            "keywords": item["keywords"],
            "language": item["language"],
            "rewrite_date": item["rewrite_date"],
            "rewrite_mode": item["rewrite_mode"],
            "target_web": item["web"]["url"],
            "category": item["taxonomy"]["taxonomy_name"],
        }
        for item in draft_keywords
    ]

    df_draft = pd.DataFrame(draft_keywords).sort_values("rewrite_date", ascending=True)
    df_draft["number"] = range(1, len(df_draft) + 1)
    df_draft = df_draft[
        [
            "number",
            "keywords",
            "language",
            "rewrite_date",
            "rewrite_mode",
            "target_web",
            "category",
        ]
    ]

    tab2.dataframe(
        df_draft,
        hide_index=True,
        column_config={
            "keywords": st.column_config.TextColumn(
                "Kata Kunci",
            ),
            "language": st.column_config.TextColumn(
                "Bahasa",
            ),
            "rewrite_date": st.column_config.DatetimeColumn(
                "Tanggal Rewrite",
                format="DD-MM-YYYY HH:mm",
                help="Tanggal terakhir artikel di-rewrite",
            ),
            "rewrite_mode": st.column_config.TextColumn(
                "Mode Rewrite",
                help="Mode rewrite yang digunakan",
            ),
            "target_web": st.column_config.TextColumn(
                "Web Target",
                help="Web target tempat artikel akan dipublikasikan",
            ),
            "category": st.column_config.TextColumn(
                "Kategori",
                help="Kategori terpilih untuk artikel yang akan dihasilkan",
            ),
        },
    )
except Exception as e:
    tab2.warning(f"Tidak ada data yang dapat ditampilkan: {e}")
