import streamlit as st
import time
from typing import List
from utils.page_header import page_header
from utils.state.bot import WebTarget, WebSource, WebConfig
from utils.supabase import (
    SupaWebHandler,
    WebData,
    SupaTaxonomyHandler,
    TaxonomyData,
    TaxonomyMappingData,
    WebConfigData,
    SupaConfigHandler,
)

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
target_url = target.get("url")
source_url = source.get("url")

submit = st.button("Submit", key="submit", use_container_width=True, type="primary")


def get_cat_by_slug(slug, data, web_id):
    data = [x for x in data if x["slug"] == slug]
    if data:
        return TaxonomyData.model_validate(
            {
                "term_name": "categories",
                "taxonomy_id": data[0]["id"],
                "taxonomy_name": data[0]["slug"],
                "web_id": web_id,
            }
        )
    return None


def add_web():
    supa = SupaWebHandler()
    target_data = WebData(
        url=target_url,
        role_key="target",
    )
    source_data = WebData(
        url=source_url,
        role_key="source",
    )
    source = supa.add(source_data)
    target = supa.add(target_data)

    return source, target


def add_taxonomies(source_id: int, target_id: int):
    supa = SupaTaxonomyHandler()
    source_categories = source.get("categories")
    target_categories = target.get("categories")
    mapping = config.get("mapping")
    results = []
    for map in mapping:
        src = get_cat_by_slug(map["source"], source_categories, source_id)
        if f"{src.web_id}-{src.taxonomy_id}" in [
            f"{x.web_id}-{x.taxonomy_id}" for x in results
        ]:
            continue
        results.append(src)
        for trg in map["target"]:
            trg_item = get_cat_by_slug(trg, target_categories, target_id)
            if f"{trg_item.web_id}-{trg_item.taxonomy_id}" in [
                f"{x.web_id}-{x.taxonomy_id}" for x in results
            ]:
                continue
            results.append(trg_item)
    responses = [supa.add(result) for result in results]
    return responses


def add_taxonomies_mapping(data: List[TaxonomyData]):
    supa = SupaTaxonomyHandler()
    config.get("mapping")
    results = []
    for map in config.get("mapping"):
        match_source = [x for x in data if x.taxonomy_name == map["source"]]
        if not match_source:
            continue
        source = match_source[0]
        for target in map["target"]:
            match_target = [x for x in data if x.taxonomy_name == target]
            if not match_target:
                continue
            target = match_target[0]
            results.append(
                TaxonomyMappingData.model_validate(
                    {
                        "source_id": source.id,
                        "target_id": target.id,
                    }
                )
            )
    return supa.mapping(results)


def add_web_config(source_id: int, target_id: int):
    supa = SupaConfigHandler()
    key_map = {
        "source_lang": "language",
        "target_lang": "language",
        "rewrite_mode": "rewrite_mode",
        "post_status": "post_status",
        "target_auth_user": "auth_username",
        "target_auth_pass": "auth_token",
    }

    web_config = []
    config_data = config.getAll(exclude=["mapping"])
    for key, value in config_data.items():
        if key in ["source_lang"]:
            web_config.append(
                WebConfigData.model_validate(
                    {
                        "key": key_map[key],
                        "value": value,
                        "web_id": source_id,
                    }
                )
            )
        else:
            web_config.append(
                WebConfigData.model_validate(
                    {
                        "key": key_map[key],
                        "value": value,
                        "web_id": target_id,
                    }
                )
            )
    web_config.append(
        WebConfigData.model_validate(
            {
                "key": "rewrite_mode",
                "value": "default",
                "web_id": target_id,
            }
        )
    )

    return supa.add(web_config)


if submit:
    with st.status(
        "Menyimpan konfigurasi AGC....", expanded=True, state="running"
    ) as status:
        time.sleep(1)

        status.update(label="Menambahkan website...", state="running")
        st.write("Menambahkan website...")
        source_res, target_res = add_web()
        status.update(state="complete")
        time.sleep(1)

        status.update(label="Menyimpan konfigurasi kategori...", state="running")
        st.write("Menyimpan konfigurasi kategori...")
        taxonomies = add_taxonomies(source_res.id, target_res.id)
        status.update(state="complete")
        time.sleep(1)

        status.update(
            label="Menyimpan konfigurasi mapping kategori...", state="running"
        )
        st.write("Menyimpan konfigurasi mapping kategori...")
        mapping = add_taxonomies_mapping(taxonomies)
        status.update(state="complete")
        time.sleep(1)

        status.update(label="Menyimpan konfigurasi web...", state="running")
        st.write("Menyimpan konfigurasi web...")
        web_config = add_web_config(source_res.id, target_res.id)
        status.update(state="complete")
        st.balloons()
        st.success("Konfigurasi berhasil disimpan!, Tunggu sebentar...")
        time.sleep(3)
        st.switch_page("pages/dashboard.py")
