import streamlit as st
import pandas as pd
from utils.page_header import page_header
from utils.supabase import SupaSeedKeywords, SupaSeedTarget

st.set_page_config(
    page_title="Keyword Seeder - AGC Likrea Asisstant",
    page_icon=":robot:",
)

page_header(
    title="Daftar Antrian Keyword",
    description="Masukkan keyword yang ingin diuji untuk melihat hasil penulisan konten",
)

supa = SupaSeedKeywords()
seed_target = SupaSeedTarget()
target = seed_target.getAll()
target = ["Semua"] + list(set([item["url"] for item in target]))


selected_target = st.selectbox("Pilih Web Target", target)


def displayTable(tab, status, selected_target="Semua"):
    try:
        keywords = supa.getAllWithChildren(status=status)
        keywords = [
            {
                "keywords": item["keywords"],
                "language": item["language"],
                "rewrite_date": item["rewrite_date"],
                "rewrite_mode": item["rewrite_mode"],
                "public_url": item["public_url"],
                "target_web": f"{item['web']['url']} ({item['web']['username']})",
                "category": item["taxonomy"]["taxonomy_name"],
            }
            for item in keywords
        ]

        df = pd.DataFrame(keywords).sort_values("rewrite_date", ascending=True)
        df["number"] = range(1, len(df) + 1)
        display_columns = [
            "number",
            "keywords",
            "language",
            "rewrite_date",
            "rewrite_mode",
            "target_web",
            "category",
        ]
        if status == "published":
            display_columns.append("public_url")

        df = df[display_columns]

        # filter by `selected_target`
        if selected_target != "Semua":
            df = df[df["target_web"].str.contains(selected_target)]

        tab.dataframe(
            df,
            hide_index=True,
            column_config={
                "number": st.column_config.NumberColumn(
                    "No.",
                ),
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
                "public_url": st.column_config.LinkColumn(
                    "URL Artikel",
                    help="URL artikel yang telah dipublikasikan",
                ),
            },
        )
    except Exception as e:
        tab.warning(f"Tidak ada data yang dapat ditampilkan: {e}")


queueTab, draftTab, publishedTab, errorTab = st.tabs(
    ["Queue", "Draft", "Published", "Error"]
)
displayTable(queueTab, "queue", selected_target)
displayTable(draftTab, "draft", selected_target)
displayTable(publishedTab, "published", selected_target)
displayTable(errorTab, "error", selected_target)
