import streamlit as st


def navigation_button(prev=None, next=None, **kwargs):
    col1, col2 = st.columns([1, 1])
    if prev:
        prev_text = prev.get("text", "Sebelumnya")
        prev_config = prev.get("config", {})
        prev_target = prev.get("target", "")
        prev_btn_type = prev.get("type", "secondary")
        prev_callbacks = prev.get("callbacks", None)
        prev_button = col1.button(
            prev_text, use_container_width=True, type=prev_btn_type, **prev_config
        )
        if prev_button:
            if prev_callbacks:
                prev_callbacks()
            st.switch_page(f"pages/{prev_target}")

    if next:
        next_text = next.get("text", "Selanjutnya")
        next_target = next.get("target", "")
        next_config = next.get("config", {})
        next_btn_type = next.get("type", "primary")
        next_callbacks = next.get("callbacks", None)
        next_button = col2.button(
            next_text, use_container_width=True, type=next_btn_type, **next_config
        )
        if next_button:
            if next_callbacks:
                next_callbacks()
            st.switch_page(f"pages/{next_target}")

    return (
        col1,
        col2,
    )
