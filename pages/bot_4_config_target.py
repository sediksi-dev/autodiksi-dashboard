import streamlit as st
import pandas as pd
from utils.page_header import page_header
from utils.state.bot import WebTarget, WebSource, WebConfig
from utils.wp_handler import check_is_wp, check_all_term
from utils.navigation_button import navigation_button as nav, NavigationButton

st.set_page_config(
    page_title="Tambahkan Web Target- AGC Likrea Assistant",
    page_icon=":robot:",
)

page_header(
    title="Tambahkan Web Target",
    description="Isi form berikut untuk mengonfigurasi web target",
)

if "check_target_btn" not in st.session_state:
    st.session_state.check_target_btn = True

source = WebSource()
target = WebTarget()
config = WebConfig()

source_url = source.get("url")
categories = source.get("selected_categories")


def set_target_url():
    st.session_state.check_target_btn = True
    target.set("categories", [])
    config.reset_mapping()
    target.set("url", st.session_state._target_url)


def get_categories():
    target_url = target.get("url")
    st.session_state.check_target_btn = False
    if not target_url:
        st.toast("URL target tidak boleh kosong.", icon="❌")
        return
    try:
        is_wp = check_is_wp(target_url)
        if is_wp:
            categories = check_all_term(target_url, "categories")
            if categories and len(categories.get("data", [])) > 0:
                target.set("categories", categories["data"])
            else:
                st.toast("Gagal mengambil kategori.")
        else:
            st.toast("Target website bukan wordpress")
    except Exception as e:
        st.error("Gagal melakukan pemanggilan.\n{}".format(e))


def display_target_categories(target_cat):
    with st.expander(f"Lihat Daftar Kategori Target `{target.get('url')}`"):
        df = pd.DataFrame(target_cat)
        df = df[["name", "slug", "total", "link"]]
        st.dataframe(
            df,
            hide_index=True,
            use_container_width=True,
        )


def update_selected_categories(val):
    state_val = f"target_map_{val}"
    config.set_mapping_by_source_key(val, st.session_state[state_val])


def select_box_target(src):
    target_options = [t["slug"] for t in target.get("categories")]
    selected_target = config.get_mapping_by_source_key(src["slug"])

    input = st.multiselect(
        f"Pilih kategori untuk `{src['name']}`",
        target_options,
        key=f"target_map_{src['slug']}",
        default=selected_target,
        on_change=lambda: update_selected_categories(src["slug"]),
    )
    return input


def categories_map():
    src = source.get("selected_categories")
    res = []
    for _, s in enumerate(src):
        trgt = select_box_target(s)
        res.append({"source": s["slug"], "target": trgt})
    config.set("mapping", res)


# Ketika target_url berubah, maka reset kategori target
target_url = st.text_input(
    f"Artikel dari `{source_url}` dipost kembali ke `{target.get('url')}`",
    key="_target_url",
    value=target.get("url"),
    placeholder="Contoh: www.fatwapedia.com atau awreceh.id",
    help="Masukkan tanpa `https` dan `/` di akhir",
    on_change=set_target_url,
)

# Ketika target_url telah diisi, maka tampilkan tombol cek target
if st.session_state.check_target_btn:
    save_target_url = st.button("Cek Target", on_click=get_categories)


if len(target.get("categories")) > 0:
    target_cat = target.get("categories")
    # Jika kategori target sudah diisi, tampilkan kategori target
    if target_cat:
        display_target_categories(target_cat)
        categories_map()
        nav(
            prev=NavigationButton(
                target="bot_3_pick_categories.py",
            ),
            next=NavigationButton(
                text="Selanjutnya",
                type="primary",
                target="bot_5_web_config.py",
            ),
        )
