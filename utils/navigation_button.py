import streamlit as st
from pydantic import BaseModel
from typing import Literal, Callable


class NavigationButton(BaseModel):
    text: str = "Sebelumnya"
    target: str = ""
    config: dict = {}  # button config
    type: Literal["primary", "secondary"] = "secondary"
    callbacks: Callable = None


def navigation_button(prev: NavigationButton = None, next: NavigationButton = None):
    col1, col2 = st.columns([1, 1])
    if prev:
        prev_button = col1.button(
            prev.text,
            use_container_width=True,
            type=prev.type,
            key="prev_button",
            **prev.config,
        )
        if prev_button:
            if prev.callbacks:
                prev.callbacks()
            st.switch_page(f"pages/{prev.target}")

    if next:
        next_button = col2.button(
            next.text,
            use_container_width=True,
            type=next.type,
            key="next_button",
            **next.config,
        )
        if next_button:
            if next.callbacks:
                next.callbacks()
            st.switch_page(f"pages/{next.target}")

    return (
        col1,
        col2,
    )
