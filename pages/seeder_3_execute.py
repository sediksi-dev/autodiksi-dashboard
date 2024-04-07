import streamlit as st
import time
from utils.page_header import page_header
from utils.state.seeder import SeederKeywords
from utils.supabase import SupaSeedTaxonomy, SupaSeedKeywords

st.set_page_config(
    page_title="Keyword Seeder - AGC Likrea Asisstant",
    page_icon=":robot:",
)

page_header(
    title="Review Keyword Seeder",
    description="Review keyword yang telah diinputkan dan tentukan tanggal publikasi artikel",
)

seeder = SeederKeywords()
supa = SupaSeedTaxonomy()
keywords_db = SupaSeedKeywords()
data = seeder.get("data")
all_categories = seeder.get_config("categories")


def get_tax_id(tax_id: int, target_id: int, data: list[dict]):
    for item in data:
        if item["taxonomy_id"] == tax_id and item["target_id"] == target_id:
            return item["id"]
    return None


with st.status("Memproses data...", expanded=False, state="running"):
    unique_categories = list(set([item["tax_id"] for item in data]))
    added_categories = []
    for item in unique_categories:
        category = [cat for cat in all_categories if cat["id"] == item]
        if len(category) == 0:
            raise ValueError(f"Category with id {item} not found")
        else:
            category = category[0]
        submitted_data = supa.add(
            {
                "term_name": "categories",
                "taxonomy_id": category["id"],
                "taxonomy_name": category["name"],
                "taxonomy_slug": category["slug"],
            },
            target_id=seeder.get_config("target_id"),
        )
        added_categories.append(submitted_data)

    prepared_data = [
        {
            **item,
            "rewrite_date": item["rewrite_date"].strftime("%Y-%m-%d %H:%M:%S+07"),
            "tax_id": get_tax_id(
                item["tax_id"], seeder.get_config("target_id"), added_categories
            ),
        }
        for item in data
    ]
    submitted_keywords = keywords_db.addBulk(prepared_data)
    st.write("Data berhasil disimpan ke database. Mohon tunggu beberapa saat...")
    st.balloons()
    seeder.reset()
    st.cache_data.clear()
    time.sleep(5)
    st.switch_page("pages/seeder_keywords_queue.py")
