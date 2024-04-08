import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta
from utils.page_header import page_header
from utils.state.seeder import SeederKeywords
from utils.navigation_button import navigation_button as nav, NavigationButton

st.set_page_config(
    page_title="Keyword Seeder - AGC Likrea Asisstant",
    page_icon=":robot:",
)

page_header(
    title="Review Keyword Seeder",
    description="Review keyword yang telah diinputkan dan tentukan tanggal publikasi artikel",
)


seeder = SeederKeywords()
keywords = seeder.get("keywords")
config = seeder.get("config")


def generate_random_interval(config: dict):
    random_interval = config["random_interval"] if "random_interval" in config else 10
    return random.randint(-random_interval, random_interval)


def generate_rewrite_date(keywords: list[str], config: dict):
    published_date = []
    random_interval = generate_random_interval(config)

    start_date = datetime.strptime(str(config["start_date"]), "%Y-%m-%d")
    time_skip_start = datetime.strptime(str(config["time_skip_start"]), "%H:%M:%S")
    time_skip_end = datetime.strptime(str(config["time_skip_end"]), "%H:%M:%S")
    post_interval = config["post_interval"]

    # Join date and time
    # days = 1
    current_date = start_date + timedelta(
        hours=time_skip_start.hour, minutes=time_skip_start.minute + random_interval
    )

    for _, _ in enumerate(keywords, start=1):
        random_interval = generate_random_interval(config)
        # tambahkan waktu publikasi artikel ke dalam list
        published_date.append(current_date)

        # hitung waktu publikasi artikel selanjutnya
        next_date = current_date + timedelta(minutes=post_interval + random_interval)

        # Jika waktu publikasi artikel selanjutnya melebihi time_skip_end, maka tambahkan 1 hari dan set ke time_skip_start
        if next_date.time() >= time_skip_end.time():
            next_date = datetime.combine(
                (next_date + timedelta(days=1)).date(),
                (time_skip_start + timedelta(minutes=random_interval)).time(),
            )

        current_date = next_date
    return published_date


def get_category_name_by_id(category_id: int):
    """Function to get category name by category id

    Args:
        category_id (int): Category id

    Returns:
        str: Category name
    """
    for category in seeder.get_config("categories"):
        if category["id"] == category_id:
            return category["name"]
    return None


df = pd.DataFrame(keywords, columns=["keywords"])
df["language"] = config["language"]
df["rewrite_mode"] = config["rewrite_mode"]
df["rewrite_date"] = generate_rewrite_date(keywords, config)
df["publish_status"] = config["publish_status"]
df["status"] = "draft"
df["target_id"] = config["target_id"]
df["tax_id"] = config["selected_category"]
list_df = df.to_dict(orient="records")
seeder.set("data", list_df)

display_df = df.copy()
display_df["category_name"] = get_category_name_by_id(config["selected_category"])
display_df = display_df[
    [
        "keywords",
        "language",
        "rewrite_date",
        "rewrite_mode",
        "publish_status",
        "category_name",
    ]
]

st.caption(
    f"Kamu akan menyimpan {len(df)} artikel ke dalam antrian artikel. Berikut adalah data artikel yang akan disimpan:"
)

st.dataframe(
    display_df,
    hide_index=True,
    use_container_width=True,
    column_config={
        "keywords": st.column_config.TextColumn(
            "Kata Kunci",
        ),
        "rewrite_date": st.column_config.DatetimeColumn(
            "Tanggal Publikasi",
            help="Tanggal dan waktu publikasi artikel",
            format="DD-MM-YYYY HH:mm:ss",
            timezone="Asia/Jakarta",
        ),
        "language": st.column_config.TextColumn(
            "Bahasa",
        ),
        "rewrite_mode": st.column_config.TextColumn(
            "Mode Rewrite",
        ),
        "publish_status": st.column_config.TextColumn(
            "Status Publikasi",
        ),
        "category_name": st.column_config.TextColumn("Kategori Artikel"),
    },
)


nav(
    prev=NavigationButton(
        text="Ganti Konfigurasi",
        target="seeder_1_config.py",
        type="secondary",
    ),
    next=NavigationButton(
        text="Simpan dan Lanjutkan",
        target="seeder_3_execute.py",
        type="primary",
    ),
)
