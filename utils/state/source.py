import streamlit as st
from .bot import BotState


default_source_state = {
    "is_wp": False,
    "url": "",
    "categories": [],
    "selected_categories": [],
}


class WebSource(BotState):
    def __init__(self):
        super().__init__("source", default_source_state)
