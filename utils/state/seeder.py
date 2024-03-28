import streamlit as st
from typing import Dict, Any


class SeederState:
    def __init__(self, key: str, default_value: Dict[str, Any]):
        self.role = key
        self._default_value = default_value
        if key not in st.session_state:
            st.session_state[self.role] = {}

    def start(self):
        st.session_state[self.role] = self._default_value
        for key, value in self._default_value.items():
            setattr(
                self,
                key,
                property(lambda self: self.get(key)),
            )

    def getAll(self, exclude: list = []):
        if len(exclude) > 0:
            return {
                key: value
                for key, value in st.session_state[self.role].items()
                if key not in exclude
            }
        return st.session_state[self.role]

    def get(self, key: str) -> Any:
        if key not in self._default_value.keys():
            raise KeyError(f"Can't get key {key} from state {self.role}")
        return st.session_state[self.role][key]

    def set(self, key: str, value: Any):
        if key not in self._default_value.keys():
            raise KeyError(f"Can't set key {key} to state {self.role}")
        st.session_state[self.role][key] = value

    def reset(self):
        for key, value in self._default_value.items():
            self.set(key, value)

    def reset_and_set(self, key: str, value: Any):
        st.cache_data.clear()
        self.reset()
        self.set(key, value)


class SingleSeedArticle(SeederState):
    def __init__(self):
        super().__init__(
            "seeder",
            {
                "keyword": "",
                "language": "Indonesia",
                "article_data": None,
            },
        )
