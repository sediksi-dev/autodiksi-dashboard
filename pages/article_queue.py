import streamlit as st
from utils.page_header import page_header
from utils.supabase import SupaListWebHandler
import pandas as pd

st.set_page_config(
    page_title="Daftar Antrian Artikel - AGC Likrea Assistant",
    page_icon=":robot:",
)

page_header(
    title="Daftar Antrian Artikel",
    description="Berikut adalah antrian artikel yang akan dihasilkan oleh AGC Likrea.",
)

supa = SupaListWebHandler()
queue_db = supa.get_article_by_status("draft")
queue = {
    "post_title": [a["post_title"] for a in queue_db],
    "source_url": [a["source_url"] for a in queue_db],
    "published_date": [a["published_date"] for a in queue_db],
}
df = pd.DataFrame(queue)
if len(df) == 0:
    st.warning("Tidak ada antrian artikel.")
st.dataframe(
    df,
    hide_index=True,
    use_container_width=True,
    column_config={
        "post_title": st.column_config.TextColumn(label="Judul Artikel"),
        "source_url": st.column_config.LinkColumn(
            label="URL Sumber", display_text="Buka URL", width=100
        ),
        "published_date": st.column_config.DatetimeColumn(
            label="Tanggal Publikasi", format="DD/MMM/YYYY HH:mm"
        ),
    },
)
