import pandas as pd
import streamlit as st
from utils.page_header import page_header
from utils.supabase import SupaSeedKeywords, SupaSeedTarget

# Set page configuration
st.set_page_config(
    page_title="Keyword Seeder - AGC Likrea Asisstant",
    page_icon=":robot:",
)

# Set page header
page_header(
    title="Daftar Antrian Keyword",
    description="Masukkan keyword yang ingin diuji untuk melihat hasil penulisan konten",
)

# Initialize SupaSeedKeywords and SupaSeedTarget
supa = SupaSeedKeywords()
seed_target = SupaSeedTarget()

# Get all targets
target = seed_target.getAll()
target = ["Semua"] + list(set([item["url"] for item in target]))

# Initialize session state
if "tp" not in st.session_state:
    st.session_state.tp = {
        "queue": 1,
        "draft": 1,
        "published": 1,
        "error": 1,
    }


# Define functions
def reset_tp():
    st.session_state.tp = {
        "queue": 1,
        "draft": 1,
        "published": 1,
        "error": 1,
    }


def get_tp(status):
    return st.session_state.tp.get(status, 1)


def set_tp(status):
    print(f"Set TP: {status}")
    print(st.session_state[f"_page_{status}"])
    st.session_state.tp[status] = st.session_state[f"_page_{status}"]


def next_tp(status):
    current = get_tp(status)
    st.session_state.tp[status] = current + 1


def prev_tp(status):
    current = get_tp(status)
    st.session_state.tp[status] = current - 1


# Select target web
selected_target = st.selectbox(
    "Pilih Web Target", target, on_change=reset_tp, key="_target_web"
)


# Define function to display table
def displayTable(tab, status, selected_target="Semua", page=1, page_size=50):
    try:
        if selected_target == "Semua":
            target_web = None
        else:
            target_web = selected_target
        keywords, count = supa.getSpecific(
            status=status,
            target=target_web,
            page=page,
            per_page=page_size,
        )
        max_page = count // page_size + 1

        if not keywords or len(keywords) == 0 or count == 0:
            raise Exception("Tidak ada data yang dapat ditampilkan")

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
        df["number"] = [i + (page_size * (page - 1)) for i in range(1, len(df) + 1)]
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

        tab.caption(f"Halaman {page} dari {max_page}. Total data: {count} item")
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

        col1, col2, col3 = tab.columns([2, 1, 2])
        col1.button(
            "Prev",
            on_click=prev_tp,
            type="primary",
            args=[status],
            key=f"prev_{status}",
            use_container_width=True,
            disabled=get_tp(status) == 1,
        )
        col2.number_input(
            "Halaman",
            value=page,
            min_value=1,
            max_value=max_page,
            step=1,
            key=f"_page_{status}",
            label_visibility="collapsed",
            on_change=set_tp,
            args=[status],
        )

        col3.button(
            "Next",
            on_click=next_tp,
            type="primary",
            args=[status],
            key=f"next_{status}",
            use_container_width=True,
            disabled=get_tp(status) == max_page,
        )

    except Exception as e:
        tab.warning(f"Gagal menampilkan data: {e}")


# Display tabs
queueTab, draftTab, publishedTab, errorTab = st.tabs(
    ["Queue", "Draft", "Published", "Error"]
)
displayTable(
    queueTab,
    "queue",
    st.session_state._target_web,
    page=get_tp("queue"),
)
displayTable(
    draftTab,
    "draft",
    st.session_state._target_web,
    page=get_tp("draft"),
)
displayTable(
    publishedTab,
    "published",
    st.session_state._target_web,
    page=get_tp("published"),
)
displayTable(
    errorTab,
    "error",
    st.session_state._target_web,
    page=get_tp("error"),
)
