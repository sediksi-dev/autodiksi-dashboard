import streamlit as st
from utils.page_header import page_header
from utils.state.seeder import SeederKeywords
from utils.navigation_button import navigation_button as nav, NavigationButton
from utils.supabase import SupaSeedTarget
from utils.wp_handler import check_all_term


def update_config(key: str):
    seeder.set_config(key, st.session_state[f"__{key}__"])


@st.cache_data
def get_target_data():
    target_list = []
    try:
        target_list = target.getAll()
        return target_list
    except Exception as e:
        st.warning(f"Terjadi kesalahan saat mengambil data target: {str(e)}")
        return target_list


def get_target_by_id(target_id: int, target_list):
    for target in target_list:
        if target["id"] == target_id:
            return f"{target['url']} ({target['username']})"
    return None


def default_target_index(target_list):
    try:
        recent_target = seeder.get_config("target_id")
        if recent_target is None:
            return 0

        for i, target in enumerate(target_list):
            if target["id"] == seeder.get_config("target_id"):
                categories = check_all_term(target["url"], "categories")
                seeder.set_config("categories", categories["data"])
                return i
        return 0
    except Exception:
        return 0


def get_category_name_by_id(category_id: int, categories):
    for category in categories:
        if category["id"] == category_id:
            return category["name"]
    return None


def get_default_category_index(categories):
    recent_category = seeder.get_config("selected_category")
    if recent_category is None:
        return 0

    for i, category in enumerate(categories):
        if category["id"] == seeder.get_config("selected_category"):
            return i
    return 0


st.set_page_config(
    page_title="Keyword Seeder - AGC Likrea Asisstant",
    page_icon=":robot:",
)

page_header(
    title="Test Keyword Seeder",
    description="Masukkan keyword yang ingin diuji untuk melihat hasil penulisan konten",
)

seeder = SeederKeywords()
target = SupaSeedTarget()

target_list = get_target_data()
if len(target_list) == 0:
    st.error(
        "Tidak ada target web yang tersedia. Silahkan tambahkan target web terlebih dahulu."
    )
    st.stop()

default_target_idx = default_target_index(target_list)

target_id = st.selectbox(
    "Pilih target web yang akan diuji",
    key="__target_id__",
    options=[target["id"] for target in target_list],
    format_func=lambda target_id: get_target_by_id(target_id, target_list),
    help="Pilih target web yang akan diuji",
    on_change=lambda: update_config("target_id"),
    index=default_target_idx,
)

language = st.text_input(
    "Pilih bahasa yang diinginkan",
    key="__language__",
    placeholder="Misal: Indonesia",
    value=seeder.get_config("language"),
    on_change=lambda: update_config("language"),
    help="Bahasa yang diinginkan untuk artikel",
)

start_date = st.date_input(
    "Pilih tanggal mulai publikasi",
    key="__start_date__",
    help="Tanggal mulai publikasi artikel",
    value=seeder.get_config("start_date"),
    on_change=lambda: update_config("start_date"),
)

time_skip_start, time_skip_end = st.columns(2)
time_skip_start.time_input(
    "Pilih waktu mulai publikasi",
    key="__time_skip_start__",
    help="Artikel akan mulai dipublikasi setelah waktu ini",
    on_change=lambda: update_config("time_skip_start"),
    value=seeder.get_config("time_skip_start"),
)
time_skip_end.time_input(
    "Pilih waktu akhir publikasi",
    key="__time_skip_end__",
    help="Artikel akan berhenti dipublikasi setelah waktu ini",
    value=seeder.get_config("time_skip_end"),
    on_change=lambda: update_config("time_skip_end"),
)

post_interval, random_interval = st.columns(2)
post_interval.number_input(
    "Pilih interval waktu (dalam menit)",
    key="__post_interval__",
    help="Interval waktu antara setiap publikasi artikel (dalam menit)",
    step=5,
    value=seeder.get_config("post_interval"),
    on_change=lambda: update_config("post_interval"),
)
random_interval.number_input(
    "Pilih interval waktu acak (dalam menit)",
    key="__random_interval__",
    help="Interval waktu acak yang ditambahkan ke interval waktu publikasi artikel (dalam menit)",
    step=1,
    min_value=0,
    max_value=15,
    value=seeder.get_config("random_interval"),
    on_change=lambda: update_config("random_interval"),
)

rewrite_mode, publish_status = st.columns(2)
rewrite_mode.selectbox(
    "Pilih mode penulisan ulang",
    key="__rewrite_mode__",
    options=["default", "spintax"],
    index=0,
    disabled=True,
    help="Sementara hanya tersedia mode `default`",
)

publish_status.selectbox(
    "Pilih status artikel",
    key="__publish_status__",
    options=["publish", "draft"],
    index=0 if seeder.get_config("publish_status") == "publish" else 1,
    on_change=lambda: update_config("publish_status"),
    help="Status artikel yang diinginkan",
)

if len(seeder.get_config("categories")) > 0:
    selected_category = st.selectbox(
        "Pilih kategori artikel",
        key="__selected_category__",
        format_func=lambda category_id: get_category_name_by_id(
            category_id, seeder.get_config("categories")
        ),
        options=[category["id"] for category in seeder.get_config("categories")],
        index=get_default_category_index(seeder.get_config("categories")),
        help="Kategori artikel yang diinginkan",
        on_change=lambda: update_config("selected_category"),
    )

nav(
    prev=NavigationButton(
        text="Sebelumnya",
        target="seeder_0_main.py",
    ),
    next=NavigationButton(
        text="Selanjutnya",
        target="seeder_2_review.py",
        type="primary",
    ),
)
