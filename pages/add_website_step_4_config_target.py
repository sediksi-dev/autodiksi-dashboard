import streamlit as st
import pandas as pd
from utils.page_header import page_header
from utils.state.source import WebSource as Source
from utils.state.target import WebTarget
from utils.wp_handler import check_is_wp, check_all_term
from utils.navigation_button import navigation_button as nav


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


source = Source()
target = WebTarget()

source_url = source.get("url")
categories = source.get("selected_categories")


def set_target_url():
    st.session_state.check_target_btn = True
    target.set("categories", [])
    target.set("url", st.session_state._target_url)


def get_categories():
    target_url = target.get("url")
    st.session_state.check_target_btn = False
    try:
        is_wp = check_is_wp(target_url)
        if is_wp:
            categories = check_all_term(target_url, "categories")
            if categories and len(categories["data"]) > 0:
                target.set("categories", categories["data"])
            else:
                st.toast("Gagal mengambil kategori.")
        else:
            st.toast("Target website bukan wordpress")
    except Exception as e:
        st.toast("Gagal melakukan pemanggilan.\n{}".format(e), icon="❌")


def display_target_categories(target_cat):
    with st.expander(f"Lihat Daftar Kategori Target `{target.get('url')}`"):
        df = pd.DataFrame(target_cat)
        df = df[["name", "slug", "total", "link"]]
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


def select_box_target(src, value=None):
    trg = target.get("categories")
    options = [t["slug"] for t in trg]

    if value:
        # remove value from options
        options.remove(value)
        # place value in first index
        options.insert(0, value)

    input = st.selectbox(
        f"Pilih kategori untuk`{src['name']}`",
        options,
        key=f"target_map_{src['slug']}",
    )
    return input


def categories_map():
    src = source.get("selected_categories")
    # trg = target.get("categories")
    res = []
    if target.get("mapping"):
        selected = target.get("mapping")

    for i, s in enumerate(src):
        try:
            selected_val = selected[i]["target"]
        except Exception:
            selected_val = None
        if selected_val:
            trgt = select_box_target(s, selected_val)
        else:
            trgt = select_box_target(s)
        res.append({"source": s["slug"], "target": trgt})
    target.set("mapping", res)


target_url = st.text_input(
    f"Artikel dari `{source_url}` dipost kembali ke `{target.get('url')}`",
    key="_target_url",
    value=target.get("url"),
    help="Masukkan tanpa `https` dan `/`",
    placeholder="target_url. Misal: cuakz.com",
    on_change=set_target_url,
)

if st.session_state.check_target_btn:
    save_target_url = st.button("Simpan Target", on_click=get_categories)


if target.get("categories"):
    if len(target.get("categories")) > 0:
        target_cat = target.get("categories")
        if target_cat:
            display_target_categories(target_cat)
            categories_map()
            nav(
                prev={"target": "add_website_step_3_pick_categories.py"},
                next={"target": "add_website_step_5_web_config.py"},
            )
