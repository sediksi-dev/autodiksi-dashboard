import streamlit as st
from utils.page_header import page_header
from utils.navigation_button import navigation_button as nav
from utils.state.source import WebSource
from utils.state.target import WebTarget
from utils.supabase import SupaAddWebHandler


st.set_page_config(
    page_title="Pengaturan Publish - AGC Likrea Assistant",
    page_icon=":robot:",
)

page_header(
    title="Pengaturan AI",
    description="Isi form berikut untuk mengonfigurasi web target",
)

source = WebSource()
target = WebTarget()
supa = SupaAddWebHandler()

source_url = source.get("url")
target_url = target.get("url")
target_id = target.get("id")
source_exist, target_exist, target_config_exist = supa.get_target_config(
    source_url, target_url
)

post_status_index = {
    "draft": 0,
    "publish": 1,
}

default_config = {
    "source_lang": "",
    "target_lang": "",
    "target_auth_user": "",
    "target_auth": "",
    "post_status": "draft",
}
if not target.get("config"):
    target.set("config", default_config)


def source_lang_input():
    if source_exist:
        disabled = True
        default_value = source_exist["language"]
    else:
        disabled = False
        default_value = target.get("config")["source_lang"]

    return st.text_input(
        f"Masukkan bahasa utama pada situs sumber `{source.get('url')}`",
        placeholder="Misal: English",
        value=default_value,
        disabled=disabled,
    )


def target_lang_input():
    if target_exist:
        disabled = True
        default_value = target_exist["language"]
    else:
        disabled = False
        default_value = target.get("config")["target_lang"]
    return st.text_input(
        f"Masukkan bahasa utama pada situs target `{target.get('url')}`",
        placeholder="Misal: Indonesia",
        value=default_value,
        disabled=disabled,
    )


def auth_data_input():
    config_exist = target_config_exist
    config = {}
    for items in config_exist:
        config[items["key"]] = items["value"]

    default_target_auth_user = (
        config["auth_username"]
        if config["auth_username"]
        else target.get("config")["target_auth_user"]
    )

    default_target_auth_token = (
        config["auth_token"]
        if config["auth_token"]
        else target.get("config")["target_auth"]
    )

    default_post_status = (
        config["status"] if config["status"] else target.get("config")["post_status"]
    )

    auth_user = st.text_input(
        f"Masukkan wp `username` pada situs target: `{target.get('url')}`",
        placeholder="Contoh: admin_cuakz",
        value=default_target_auth_user,
        disabled=True if config["auth_username"] else False,
    )
    auth_token = st.text_input(
        f"Masukkan wp `token password` pada situs target: `{target.get('url')}`",
        placeholder="Contoh: 7hjs sdas d0sa asd92",
        help="Token password bisa didapat di menu `Add Application` pada halaman profile pengguna wordpress",
        value=default_target_auth_token,
        disabled=True if config["auth_token"] else False,
    )

    post_status = st.radio(
        "Pilih status artikel yang akan dikirim ke web target",
        ["draft", "publish"],
        captions=[
            "Hasil penulisan ulang berstatus `draft`",
            "Artikel langsung terpublikasi setelah AI selesai menulis ulang",
        ],
        horizontal=True,
        index=post_status_index[default_post_status],
        disabled=True if config["status"] else False,
    )

    return auth_user, auth_token, post_status


def config():
    source_lang = source_lang_input()
    target_lang = target_lang_input()
    target_auth_user, target_auth, post_status = auth_data_input()

    button_disabled = (
        not source_lang
        or not target_lang
        or not target_auth_user
        or not target_auth
        or not post_status
    )

    target.set(
        "config",
        {
            "source_lang": source_lang,
            "target_lang": target_lang,
            "target_auth_user": target_auth_user,
            "target_auth": target_auth,
            "post_status": post_status,
        },
    )

    nav(
        prev={"target": "add_website_step_4_config_target.py"},
        next={
            "target": "add_website_step_6_review.py",
            "config": {"disabled": button_disabled},
        },
    )


def config_exist():
    st.write("Konfigurasi web target sudah ada, lanjutkan ke tahap berikutnya")
    nav(
        prev={"target": "add_website_step_4_config_target.py"},
        next={"target": "add_website_step_6_review.py"},
    )


config()
