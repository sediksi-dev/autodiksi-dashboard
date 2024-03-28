import streamlit as st
from utils.page_header import page_header
from utils.navigation_button import navigation_button as nav, NavigationButton
from utils.state.bot import WebTarget, WebSource, WebConfig
from utils.supabase import SupaConfigHandler

st.set_page_config(
    page_title="Pengaturan Publish - AGC Likrea Assistant", page_icon=":robot:"
)
page_header(
    title="Pengaturan AI",
    description="Isi form berikut untuk mengonfigurasi web target",
)

source = WebSource()
target = WebTarget()
config = WebConfig()
db_config = SupaConfigHandler()


def get_default_config():
    source_config = db_config.getAll(source.get("url"))
    target_config = db_config.getAll(target.get("url"))
    return {
        "source_lang": source_config.language if source_config else None,
        "target_lang": target_config.language if target_config else None,
        "target_auth_user": target_config.auth_username if target_config else None,
        "target_auth_pass": target_config.auth_token if target_config else None,
        "post_status": target_config.post_status if target_config else None,
        "rewrite_mode": target_config.rewrite_mode if target_config else None,
    }


def update_config(key, value=None):
    if value is None:
        field_key = f"_config_{key}"
        config.set(key, st.session_state[field_key])
    else:
        config.set(key, value)


def text_input_config(label, key, placeholder=None):
    db_value = default_config.get(key)
    config_value = config.get(key)
    field_key = f"_config_{key}"

    if db_value is not None:
        update_config(key, value=db_value)
        value = st.text_input(
            f"Tidak bisa diubah. `{key}` existing in database",
            value=db_value,
            key=field_key,
            disabled=True,
        )
        return value
    return st.text_input(
        label,
        value=config_value,
        key=field_key,
        placeholder=placeholder,
        on_change=lambda: update_config(key),
    )


default_config = get_default_config()

config_source_lang = text_input_config(
    "Bahasa Utama pada Situs Sumber",
    "source_lang",
    placeholder="Misal: Indonesia",
)

config_target_lang = text_input_config(
    "Bahasa Utama pada Situs Target",
    "target_lang",
    placeholder="Misal: English",
)

config_target_auth_user = text_input_config(
    "Username pada Situs Target",
    "target_auth_user",
    placeholder="Misal: admin_cuakz",
)

config_target_auth_pass = text_input_config(
    "Password pada Situs Target",
    "target_auth_pass",
    placeholder="Misal: 7hjs sdas d0sa asd92",
)

post_status_index = {"draft": 0, "publish": 1}
post_status_default = default_config.get("post_status")
if post_status_default is not None:
    config.set("post_status", post_status_default)
disabled_post_status = post_status_default is not None
post_status_label = (
    f"Tidak dapat mengubah post_status (Dipilih: {post_status_default})"
    if post_status_default
    else "Status Artikel pada Situs Target"
)

config_post_status = st.radio(
    post_status_label,
    ["draft", "publish"],
    captions=[
        "Hasil penulisan ulang berstatus `draft`",
        "Artikel langsung terpublikasi setelah AI selesai menulis ulang",
    ],
    horizontal=True,
    index=post_status_index[post_status_default] if post_status_default else 0,
    disabled=disabled_post_status,
)

next_button_disabled = not all(
    [
        config_source_lang != "",
        config_target_lang != "",
        config_target_auth_user != "",
        config_target_auth_pass != "",
        config_post_status != "",
    ]
)

nav(
    prev=NavigationButton(
        target="bot_4_config_target.py",
    ),
    next=NavigationButton(
        text="Selanjutnya",
        type="primary",
        target="bot_6_review.py",
        config={"disabled": next_button_disabled},
    ),
)
