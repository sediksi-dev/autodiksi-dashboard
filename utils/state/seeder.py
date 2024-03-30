import streamlit as st
import datetime
from typing import Dict, Any


class SeederState:
    def __init__(self, key: str, default_value: Dict[str, Any]):
        self.role = key
        self._default_value = default_value
        if key not in st.session_state:
            st.session_state[self.role] = {}

    def is_default(self):
        if self.role not in st.session_state:
            return True
        elif len(st.session_state[self.role]) == 0:
            return True
        else:
            return False

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


class SeederTarget(SeederState):
    def __init__(self):
        super().__init__(
            "seeder_target",
            {
                "url": "",
                "username": "",
                "password": "",
                "api_endpoint": "wp-json/wp/v2",
                "post_type": "posts",
            },
        )


class SeederKeywords(SeederState):
    def __init__(self):
        super().__init__(
            "seeder_keywords",
            {
                "keywords": [],
                "config": {
                    "target_id": None,
                    "language": "Indonesia",
                    "start_date": datetime.datetime.now().date(),
                    "time_skip_start": datetime.time(7, 0, 0),
                    "time_skip_end": datetime.time(21, 0, 0),
                    "post_interval": 60,
                    "random_interval": 10,
                    "rewrite_mode": "default",
                    "publish_status": "draft",
                    "categories": [],
                    "selected_category": 0,
                },
                "data": None,
            },
        )

    def get_config(self, key: str):
        return self.get("config")[key]

    def set_config(self, key: str, value: Any):
        config = self.get("config")
        config[key] = value
        self.set("config", config)
