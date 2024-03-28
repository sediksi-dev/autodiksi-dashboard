from typing import Dict, Any
import streamlit as st


class BotState:
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


class WebSource(BotState):
    def __init__(self):
        super().__init__(
            "source",
            {
                "is_wp": False,
                "url": "",
                "categories": [],
                "selected_categories": [],
            },
        )


class WebTarget(BotState):
    def __init__(self):
        super().__init__(
            "target",
            {"url": "", "categories": []},
        )


class WebConfig(BotState):
    def __init__(self):
        super().__init__(
            "config",
            {
                "source_lang": "",
                "target_lang": "",
                "target_auth_user": "",
                "target_auth_pass": "",
                "post_status": "draft",
                "mapping": [],
            },
        )

    def reset_mapping(self):
        self.set("mapping", [])

    def get_mapping_by_source_key(self, source_key: str):
        mapping = self.get("mapping")
        for map in mapping:
            if map["source"] == source_key:
                return map["target"]
        return []

    def set_mapping_by_source_key(self, source_key: str, value: Any):
        mapping = self.get("mapping")
        for map in mapping:
            if map["source"] == source_key:
                map["target"] = value
                break
            else:
                mapping.append({"source": source_key, "target": [value]})
