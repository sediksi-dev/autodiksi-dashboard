import streamlit as st
from utils.page_header import page_header
from utils.state.source import WebSource
from utils.state.target import WebTarget
from utils.navigation_button import navigation_button as nav
from utils.supabase import SupaAddWebHandler
import time

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
supa = SupaAddWebHandler()


def get_cat_by_slug(slug, data):
    data = [x for x in data if x["slug"] == slug]
    if data:
        return data[0]
    return None


def get_mapping_columns():
    mapping = target.get("mapping")
    source_cat = source.get("categories")
    target_cat = target.get("categories")

    for map in mapping:
        src = get_cat_by_slug(map["source"], source_cat)
        trg = get_cat_by_slug(map["target"], target_cat)

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

    if mapping is None:
        return []


source_url = source.get("url")
target_url = target.get("url")
config = target.get("config")

mapping = list(get_mapping_columns())
with st.expander("Review Konfigurasi", expanded=True):
    st.write(
        f"""AGC Likrea Assistant akan melakukan publish dari `{source_url}` ke `{target_url}` dengan konfigurasi sebagai berikut:"""
    )
    for map in mapping:
        st.write(
            f"""- Artikel berkategori `{map['source']['name']}`  pada `{source_url}` akan dipublish sebagai artikel berkategori `{map['target']['name']}` pada `{target_url}`"""
        )
    st.write(
        f"""Setiap artikel berkategori di atas akan ditulis ulang dari bahasa `{config['source_lang']}` ke bahasa `{config['target_lang']}` oleh AGC. Setiap artikel yang dipublish pada `{target_url}` akan berstatus `{config['post_status']}`"""
    )

    st.write(
        "Jika konfigurasi di atas sudah sesuai, silahkan klik tombol `Submit` untuk melanjutkan."
    )

_, submiter = nav(
    prev={"target": "add_website_step_5_web_config.py"},
)

submit = submiter.button(
    "Submit", key="submit", use_container_width=True, type="primary"
)


def add_web():
    target_data = {
        "url": target_url,
        "language": config["target_lang"],
    }
    source_data = {
        "url": source_url,
        "language": config["source_lang"],
    }

    source = supa.add_web("source", source_data)
    target = supa.add_web("target", target_data)

    return source, target


def add_config(target_id):
    auth_username = config.get("target_auth_user")
    auth_token = config.get("target_auth")
    mode = config.get("rewrite_mode", "default")
    post_status = config.get("post_status", "draft")

    web_config = {
        "auth_username": auth_username,
        "auth_token": auth_token,
        "mode": mode,
        "status": post_status,
    }
    config_data = []
    for key, value in web_config.items():
        res = supa.add_web_config(target_id, key, value)
        config_data.append(res)

    return config_data


def add_taxonomies(source_id, target_id):
    results = []
    for map in mapping:
        src = map["source"]
        trg = map["target"]
        src_res = supa.add_taxonomies(
            source_id,
            {
                "taxonomy_id": src["id"],
                "taxonomy_name": src["slug"],
            },
        )
        trg_res = supa.add_taxonomies(
            target_id,
            {
                "taxonomy_id": trg["id"],
                "taxonomy_name": trg["slug"],
            },
        )
        results.append({"source": src_res, "target": trg_res})
    return results


if submit:
    with st.status(
        "Menyimpan konfigurasi....", expanded=True, state="running"
    ) as status:
        st.write("Menambahkan website...")
        source_data, target_data = add_web()
        status.update(state="complete")
        time.sleep(1)

        st.write("Menambahkan konfigurasi...")
        status.update(state="running")
        target_id = target_data["id"]
        source_id = source_data["id"]
        config = add_config(target_id)
        status.update(state="complete")
        time.sleep(1)

        status.update(state="running")
        st.write("Menambahkan taxonomies...")
        taxonomies = add_taxonomies(source_id, target_id)
        status.update(state="complete")
        time.sleep(1)

        status.update(state="running")
        st.write("Menambahkan mapping taxonomies...")
        for tax in taxonomies:
            source_id = tax["source"]["id"]
            target_id = tax["target"]["id"]
            supa.add_taxonomies_mapping(source_id, target_id)
        status.update(state="complete")
        st.balloons()
        status.success("Konfigurasi berhasil disimpan!, Tunggu sebentar...")
        time.sleep(3)
        st.switch_page("pages/dashboard.py")
