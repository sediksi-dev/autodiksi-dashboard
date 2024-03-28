import streamlit as st
from utils.page_header import page_header
from utils.state.bot import WebTarget, WebSource, WebConfig
from utils.navigation_button import navigation_button as nav, NavigationButton
from utils.supabase import SupaAddWebHandler

st.set_page_config(
    page_title="Pengaturan Publish - AGC Likrea Assistant",
    page_icon=":robot:",
)

page_header(
    title="Review Web",
    description="Isi form berikut untuk mengonfigurasi web target",
)

source = WebSource()
target = WebTarget()
config = WebConfig()
supa = SupaAddWebHandler()


def get_cat_by_slug(slug, data):
    data = [x for x in data if x["slug"] == slug]
    if data:
        return data[0]
    return None


def get_mapping_columns():
    mapping = config.get("mapping")
    source_cat = source.get("categories")
    target_cat = target.get("categories")

    for map in mapping:
        src = get_cat_by_slug(map["source"], source_cat)
        targets = map["target"]
        for trg in targets:
            trg = get_cat_by_slug(trg, target_cat)
            src_data = {
                "name": src["name"],
                "slug": src["slug"],
                "id": src["id"],
            }

            trg_data = {
                "name": trg["name"],
                "slug": trg["slug"],
                "id": trg["id"],
            }

            yield {
                "source": src_data,
                "target": trg_data,
            }
    # for map in mapping:
    #     src = get_cat_by_slug(map["source"], source_cat)
    #     trg = get_cat_by_slug(map["target"], target_cat)

    #     src_data = {
    #         "name": src["name"],
    #         "slug": src["slug"],
    #         "id": src["id"],
    #     }

    #     trg_data = {
    #         "name": trg["name"],
    #         "slug": trg["slug"],
    #         "id": trg["id"],
    #     }

    #     yield {
    #         "source": src_data,
    #         "target": trg_data,
    #     }

    # if mapping is None:
    #     return []


source_url = source.get("url")
target_url = target.get("url")

mapping = list(get_mapping_columns())
with st.expander("Review Konfigurasi", expanded=True):
    st.write(
        f"""AGC Likrea Assistant akan melakukan publish dari `{source_url}` ke `{target_url}` dengan konfigurasi sebagai berikut:"""
    )
    source_lang = config.get("source_lang")
    target_lang = config.get("target_lang")
    post_status = config.get("post_status")

    for map in mapping:
        st.write(
            f"""- Artikel berkategori `{map['source']['name']}`  pada `{source_url}` akan dipublish sebagai artikel berkategori `{map['target']['name']}` pada `{target_url}`"""
        )
    st.write(
        f"""Setiap artikel berkategori di atas akan ditulis ulang dari bahasa `{source_lang}` ke bahasa `{target_lang}` oleh AGC. Setiap artikel yang dipublish pada `{target_url}` akan berstatus `{post_status}`"""
    )

    st.write(
        "Jika konfigurasi di atas sudah sesuai, silahkan klik tombol `Submit` untuk melanjutkan."
    )

nav(
    prev=NavigationButton(
        text="Sebelumnya",
        target="bot_5_web_config.py",
    ),
    next=NavigationButton(
        text="Submit",
        target="bot_7_submitter.py",
        type="primary",
    ),
)
