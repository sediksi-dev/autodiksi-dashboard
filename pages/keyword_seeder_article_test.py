import streamlit as st
# import random
import time
from utils.page_header import page_header

st.set_page_config(
    page_title="Keyword Seeder - AGC Likrea Asisstant",
    page_icon=":robot:",
)

page_header(
    title="Test Keyword Seeder",
    description="Masukkan keyword yang ingin diuji untuk melihat hasil penulisan konten",
)

if "generate" not in st.session_state:
    st.session_state.generate = "idle"
    is_generate = st.session_state.generate
else:
    is_generate = st.session_state.generate


keyword = st.text_input("Keyword", placeholder="Masukkan keyword yang ingin diuji")
generate = st.button(
    "Generate",
    use_container_width=True,
    type="primary",
    disabled=is_generate not in ["idle", "failed"],
    # on_click=run,
)
notify = st.empty()


def reset():
    is_generate = "idle"
    return is_generate


def run():
    is_generate = "running"
    if keyword == "":
        notify.error("Keyword tidak boleh kosong")
        return is_generate
    else:
        notify.empty()
        notify.info("Sedang menguji keyword, mohon tunggu sebentar...")
        return is_generate


def success():
    is_generate = "success"
    notify.success("Keyword berhasil diuji")
    return is_generate


def failed():
    is_generate = "failed"
    notify.error("Keyword gagal diuji")
    return is_generate


def generating():
    st.spinner("Sedang menghasilkan konten...")
    time.sleep(3)
    # if results == "success":
    #     success()
    # elif results == "failed":
    #     failed()
    # else:
    #     reset()
    # results = random.choice(["success", "failed"])
    # return results


if generate:
    is_generate = run()

if is_generate == "running":
    results = generating()
