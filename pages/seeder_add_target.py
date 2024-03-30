import streamlit as st
from utils.page_header import page_header
from utils.state.seeder import SeederTarget

st.set_page_config(
    page_title="Keyword Seeder - AGC Likrea Asisstant",
    page_icon=":robot:",
)

page_header(
    title="Tambahkan Web dan User Target",
    description="Masukkan web dan target user yang akan digunakan sebagai tempat publikasi artikel.",
)

seeder = SeederTarget()

if seeder.is_default():
    seeder.start()


def update_input(key):
    seeder.set(key, st.session_state[f"__{key}__"])


url = st.text_input(
    "Pilih web target",
    key="__url__",
    placeholder="Misal: example.com",
    help="Alamat web target yang akan dijadikan tempat publikasi artikel. Diisi tanpa tanda petik, garis miring, atau protokol (http/https)",
    on_change=lambda: update_input("url"),
    value=seeder.get("url"),
)


username = st.text_input(
    "Masukkan username web target",
    key="__username__",
    placeholder="Misal: user123",
    help="Username untuk login ke web target. Harus diisi dengan username yang terdaftar di web target",
    on_change=lambda: update_input("username"),
    value=seeder.get("username"),
)


password = st.text_input(
    "Masukkan password web target",
    key="__password__",
    placeholder="Masukkan password",
    help="Password untuk login ke web target. Untuk mendapatkan password, kunjungi `User >> Profile >> Add New Password` di web target",
    on_change=lambda: update_input("password"),
    value=seeder.get("password"),
)

with st.expander("Pengaturan Lanjutan"):
    api_endpoint = st.text_input(
        "Masukkan API Endpoint",
        key="__api_endpoint__",
        placeholder="wp-json/wp/v2",
        help="API endpoint yang digunakan untuk mengakses REST API web target. Diisi tanpa tanda petik",
        on_change=lambda: update_input("api_endpoint"),
        value=seeder.get("api_endpoint"),
    )

    post_type = st.text_input(
        "Masukkan Tipe Posting",
        key="__post_type__",
        placeholder="posts",
        help="Tipe posting yang digunakan di web target. Diisi tanpa tanda petik",
        on_change=lambda: update_input("post_type"),
        value=seeder.get("post_type"),
    )


next_button = st.button(
    "Selanjutnya",
    use_container_width=True,
    type="primary",
)

if next_button:
    st.switch_page("pages/seeder_add_target_execute.py")
