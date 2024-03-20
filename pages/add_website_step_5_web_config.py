# import streamlit as st
# from utils.page_header import page_header
# from utils.navigation_button import navigation_button as nav
# from utils.state.source import WebSource
# from utils.state.target import WebTarget
# from utils.supabase import SupaAddWebHandler


# st.set_page_config(
#     page_title="Pengaturan Publish - AGC Likrea Assistant",
#     page_icon=":robot:",
# )

# page_header(
#     title="Pengaturan AI",
#     description="Isi form berikut untuk mengonfigurasi web target",
# )

# source = WebSource()
# target = WebTarget()
# supa = SupaAddWebHandler()

# source_url = source.get("url")
# target_url = target.get("url")
# target_id = target.get("id")
# source_exist, target_exist, target_config_exist = supa.get_target_config(
#     source_url, target_url
# )

# post_status_index = {
#     "draft": 0,
#     "publish": 1,
# }

# default_config = {
#     "source_lang": "",
#     "target_lang": "",
#     "target_auth_user": "",
#     "target_auth": "",
#     "post_status": "draft",
# }
# if not target.get("config"):
#     target.set("config", default_config)


# def source_lang_input():
#     if source_exist:
#         disabled = True
#         default_value = source_exist["language"]
#     else:
#         disabled = False
#         default_value = target.get("config")["source_lang"]

#     return st.text_input(
#         f"Masukkan bahasa utama pada situs sumber `{source.get('url')}`",
#         placeholder="Misal: English",
#         value=default_value,
#         disabled=disabled,
#     )


# def target_lang_input():
#     if target_exist:
#         disabled = True
#         default_value = target_exist["language"]
#     else:
#         disabled = False
#         default_value = target.get("config")["target_lang"]
#     return st.text_input(
#         f"Masukkan bahasa utama pada situs target `{target.get('url')}`",
#         placeholder="Misal: Indonesia",
#         value=default_value,
#         disabled=disabled,
#     )


# def auth_data_input():
#     config_exist = target_config_exist
#     config = {}
#     if config_exist:
#         for items in config_exist:
#             config[items["key"]] = items["value"]

#     default_target_auth_user = (
#         config["auth_username"]
#         if config.get("auth_username", None)
#         else target.get("config")["target_auth_user"]
#     )

#     default_target_auth_token = (
#         config["auth_token"]
#         if config.get("auth_token", None)
#         else target.get("config")["target_auth"]
#     )

#     default_post_status = (
#         config["status"]
#         if config.get("status", None)
#         else target.get("config")["post_status"]
#     )

#     auth_user = st.text_input(
#         f"Masukkan wp `username` pada situs target: `{target.get('url')}`",
#         placeholder="Contoh: admin_cuakz",
#         value=default_target_auth_user,
#         disabled=True if config.get("auth_username", None) else False,
#     )
#     auth_token = st.text_input(
#         f"Masukkan wp `token password` pada situs target: `{target.get('url')}`",
#         placeholder="Contoh: 7hjs sdas d0sa asd92",
#         help="Token password bisa didapat di menu `Add Application` pada halaman profile pengguna wordpress",
#         value=default_target_auth_token,
#         disabled=True if config.get("auth_token", None) else False,
#     )

#     post_status = st.radio(
#         "Pilih status artikel yang akan dikirim ke web target",
#         ["draft", "publish"],
#         captions=[
#             "Hasil penulisan ulang berstatus `draft`",
#             "Artikel langsung terpublikasi setelah AI selesai menulis ulang",
#         ],
#         horizontal=True,
#         index=post_status_index[default_post_status],
#         disabled=True if config.get("auth_token", None) else False,
#     )

#     return auth_user, auth_token, post_status


# def config():
#     source_lang = source_lang_input()
#     target_lang = target_lang_input()
#     target_auth_user, target_auth, post_status = auth_data_input()

#     button_disabled = (
#         not source_lang
#         or not target_lang
#         or not target_auth_user
#         or not target_auth
#         or not post_status
#     )

#     target.set(
#         "config",
#         {
#             "source_lang": source_lang,
#             "target_lang": target_lang,
#             "target_auth_user": target_auth_user,
#             "target_auth": target_auth,
#             "post_status": post_status,
#         },
#     )

#     nav(
#         prev={"target": "add_website_step_4_config_target.py"},
#         next={
#             "target": "add_website_step_6_review.py",
#             "config": {"disabled": button_disabled},
#         },
#     )


# def config_exist():
#     st.write("Konfigurasi web target sudah ada, lanjutkan ke tahap berikutnya")
#     nav(
#         prev={"target": "add_website_step_4_config_target.py"},
#         next={"target": "add_website_step_6_review.py"},
#     )


# config()

import streamlit as st
from utils.page_header import page_header
from utils.navigation_button import navigation_button as nav
from utils.state.source import WebSource
from utils.state.target import WebTarget
from utils.supabase import SupaAddWebHandler


def init_page():
    st.set_page_config(
        page_title="Pengaturan Publish - AGC Likrea Assistant", page_icon=":robot:"
    )
    page_header(
        title="Pengaturan AI",
        description="Isi form berikut untuk mengonfigurasi web target",
    )


def get_default_config():
    return {
        "source_lang": "",
        "target_lang": "",
        "target_auth_user": "",
        "target_auth": "",
        "post_status": "draft",
    }


def input_with_default(
    title, placeholder, exist_value, config_value, disabled=False, **kwargs
):
    return st.text_input(
        title,
        placeholder=placeholder,
        value=exist_value if exist_value else config_value,
        disabled=disabled,
        **kwargs,
    )


def main():
    source = WebSource()
    target = WebTarget()
    supa = SupaAddWebHandler()

    source_url, target_url = source.get("url"), target.get("url")
    source_exist, target_exist, target_config_exist = supa.get_target_config(
        source_url, target_url
    )

    if not target.get("config"):
        target.set("config", get_default_config())

    config = (
        {item["key"]: item["value"] for item in target_config_exist}
        if target_config_exist
        else {}
    )

    source_lang = input_with_default(
        f"Masukkan bahasa utama pada situs sumber `{source_url}`",
        "Misal: English",
        source_exist.get("language") if source_exist else None,
        target.get("config")["source_lang"],
        disabled=bool(source_exist),
    )
    target_lang = input_with_default(
        f"Masukkan bahasa utama pada situs target `{target_url}`",
        "Misal: Indonesia",
        target_exist.get("language") if target_exist else None,
        target.get("config")["target_lang"],
        disabled=bool(target_exist),
    )

    auth_user = input_with_default(
        f"Masukkan wp `username` pada situs target: `{target_url}`",
        "Contoh: admin_cuakz",
        config.get("auth_username"),
        target.get("config")["target_auth_user"],
        disabled="auth_username" in config,
    )
    auth_token = input_with_default(
        f"Masukkan wp `token password` pada situs target: `{target_url}`",
        "Contoh: 7hjs sdas d0sa asd92",
        config.get("auth_token"),
        target.get("config")["target_auth"],
        disabled="auth_token" in config,
        help="Token password bisa didapat di menu `Add Application` pada halaman profile pengguna wordpress",
    )

    post_status_index = {"draft": 0, "publish": 1}
    post_status = st.radio(
        "Pilih status artikel yang akan dikirim ke web target",
        ["draft", "publish"],
        captions=[
            "Hasil penulisan ulang berstatus `draft`",
            "Artikel langsung terpublikasi setelah AI selesai menulis ulang",
        ],
        horizontal=True,
        index=post_status_index[
            config.get("status", target.get("config")["post_status"])
        ],
        disabled="status" in config,
    )

    def update_config():
        target.set(
            "config",
            {
                "source_lang": source_lang,
                "target_lang": target_lang,
                "target_auth_user": auth_user,
                "target_auth": auth_token,
                "post_status": post_status,
            },
        )

    button_disabled = not all(
        [source_lang, target_lang, auth_user, auth_token, post_status]
    )

    update_config()

    # Menentukan apakah tombol navigasi selanjutnya harus dinonaktifkan berdasarkan apakah semua input telah diisi

    if target_config_exist:
        st.write("Konfigurasi web target sudah ada, lanjutkan ke tahap berikutnya")
        nav(
            prev={
                "target": "add_website_step_4_config_target.py",
                "config": {"key": "prev_key_button_if_config_exist"},
            },
            next={
                "target": "add_website_step_6_review.py",
                "config": {"key": "next_key_button_if_config_exist"},
            },
        )
    else:
        nav(
            prev={"target": "add_website_step_4_config_target.py"},
            next={
                "target": "add_website_step_6_review.py",
                "config": {"disabled": button_disabled},
            },
        )


init_page()
main()
