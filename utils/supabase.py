import streamlit as st
from typing import Union, List
from supabase import create_client, Client
from .supabase_models import (
    SourceWebConfig,
    TargetWebConfig,
    WebData,
    TaxonomyData,
    TaxonomyMappingData,
    WebConfigData,
)


class Supabase:
    def __init__(self):
        self.__url: str = st.secrets["supabase"]["url"]
        self.__key: str = st.secrets["supabase"]["key"]
        self._client: Client = create_client(self.__url, self.__key)


class SupaConfigHandler(Supabase):
    def getAll(self, host: str) -> Union[SourceWebConfig, TargetWebConfig, None]:
        query = (
            "web: web_id!inner(url, role_key)",
            "key",
            "value",
        )

        result = (
            self._client.table("web_config")
            .select(*query)
            .eq("web.url", host)
            .execute()
        )
        if len(result.data) == 0:
            return None

        role_key = result.data[0]["web"]["role_key"]
        data = {}
        for item in result.data:
            data[item["key"]] = item["value"]

        if role_key == "source":
            return SourceWebConfig(**data)
        return TargetWebConfig(**data)

    def check(self, key, web_id):
        try:
            web_config = (
                self._client.table("web_config")
                .select("*")
                .eq("key", key.value)
                .eq("web_id", web_id)
                .maybe_single()
                .execute()
            )
            if web_config:
                return WebConfigData.model_validate(web_config.data)
        except Exception:
            return False

    def add(self, data: List[WebConfigData]) -> WebConfigData:
        existing_data: List[WebConfigData] = []
        non_existing_data: List[WebConfigData] = []
        for item in data:
            config = self.check(item.key, item.web_id)
            if config:
                existing_data.append(config)
            else:
                non_existing_data.append(item)

        if len(non_existing_data) == 0:
            return existing_data

        try:
            response = (
                self._client.table("web_config")
                .insert([item.model_dump() for item in non_existing_data])
                .execute()
            )

            return existing_data + [
                WebConfigData.model_validate(item) for item in response.data
            ]
        except Exception as e:
            return str(e)


class SupaWebHandler(Supabase):
    def check(self, host: str):
        try:
            response = (
                self._client.table("web")
                .select("*")
                .eq("url", host)
                .maybe_single()
                .execute()
            )
            return WebData.model_validate(response.data)
        except Exception:
            return False

    def add(self, data: WebData) -> WebData:
        url = data.url
        web = self.check(url)
        if web:
            return web

        try:
            response = self._client.table("web").insert(data.model_dump()).execute()
            return WebData.model_validate(response.data[0])
        except Exception as e:
            return str(e)


class SupaTaxonomyHandler(Supabase):
    def check(self, web_id: int, taxonomy_id: int):
        try:
            response = (
                self._client.table("taxonomies")
                .select("*")
                .eq("web_id", web_id)
                .eq("taxonomy_id", taxonomy_id)
                .maybe_single()
                .execute()
            )
            return TaxonomyData.model_validate(response.data)
        except Exception:
            return False

    def add(self, data: Union[TaxonomyData, List[TaxonomyData]]) -> TaxonomyData:
        if isinstance(data, list):
            return [self.add(item) for item in data]
        web_id = data.web_id
        taxonomy_id = data.taxonomy_id
        taxonomy = self.check(web_id, taxonomy_id)
        if taxonomy:
            return taxonomy

        try:
            response = (
                self._client.table("taxonomies").insert(data.model_dump()).execute()
            )
            return TaxonomyData.model_validate(response.data[0])
        except Exception as e:
            return str(e)

    def check_mapping(self, source_id: int, target_id: int):
        try:
            response = (
                self._client.table("taxonomy_mapping")
                .select("*")
                .eq("source_id", source_id)
                .eq("target_id", target_id)
                .maybe_single()
                .execute()
            )
            return TaxonomyMappingData.model_validate(response.data)
        except Exception:
            return False

    def mapping(self, data: List[TaxonomyMappingData]):
        existing_data: List[TaxonomyMappingData] = []
        non_existing_data: List[TaxonomyMappingData] = []
        for item in data:
            mapping = self.check_mapping(item.source_id, item.target_id)
            if mapping:
                existing_data.append(mapping)
            else:
                non_existing_data.append(item)
        if len(non_existing_data) == 0:
            return existing_data

        response: List[TaxonomyMappingData] = []
        try:
            response = (
                self._client.table("taxonomy_mapping")
                .insert([item.model_dump() for item in non_existing_data])
                .execute()
            )
            return existing_data + [
                TaxonomyMappingData.model_validate(item) for item in response.data
            ]
        except Exception as e:
            return str(e)


class SupaAddWebHandler(Supabase):
    def check_web(self, data: dict):
        url = data.get("url")
        web_response, _ = self._client.table("web").select("*").eq("url", url).execute()
        web = web_response[1]
        is_exists = len(web) > 0
        if is_exists:
            return web[0]
        return None

    def check_web_config(self, web_id, key):
        # check if url already exists
        web_response, _ = (
            self._client.table("web_config")
            .select("*")
            .eq("web_id", web_id)
            .eq("key", key)
            .execute()
        )
        web_config = web_response[1]
        is_exists = len(web_config) > 0
        if is_exists:
            return web_config[0]
        return None

    def check_taxonomies(self, web_id, taxonomy_id):
        # check if url already exists
        web_response, _ = (
            self._client.table("taxonomies")
            .select("*")
            .eq("taxonomy_id", taxonomy_id)
            .eq("web_id", web_id)
            .execute()
        )
        taxonomies = web_response[1]
        is_exists = len(taxonomies) > 0
        if is_exists:
            return taxonomies[0]
        return None

    def check_taxonomies_mapping(self, source_id, target_id):
        tax_mapping, _ = (
            self._client.table("taxonomy_mapping")
            .select("*")
            .eq("source_id", source_id)
            .eq("target_id", target_id)
            .execute()
        )
        tax_mapping_data = tax_mapping[1]
        is_exists = len(tax_mapping_data) > 0
        if is_exists:
            return tax_mapping_data[0]
        return None

    def add_web(self, role, data: dict):
        default_lang = "english" if role == "source" else "indonesia"
        is_exist = self.check_web(data)
        if is_exist:
            return is_exist
        try:
            payload = {
                "url": data.get("url"),
                "api_endpoint": data.get("api_endpoint", "wp-json/wp/v2"),
                "post_type": data.get("post_type", "posts"),
                "role_key": role,
                "language": data.get("language", default_lang),
            }
            # return payload
            response, _ = self._client.table("web").insert(payload).execute()
            return response[1][0]
        except Exception as e:
            return str(e)

    def add_web_config(self, web_id, key, value):
        is_exist = self.check_web_config(web_id, key)
        if is_exist:
            return is_exist
        try:
            response, _ = (
                self._client.table("web_config")
                .insert({"web_id": web_id, "key": key, "value": value})
                .execute()
            )
            return response[1][0]
        except Exception as e:
            return str(e)

    def add_taxonomies(self, web_id, data):
        tax_id = data.get("taxonomy_id")
        term_name = data.get("term_name", "categories")
        is_exist = self.check_taxonomies(web_id, tax_id)
        if is_exist:
            return is_exist
        try:
            response, _ = (
                self._client.table("taxonomies")
                .insert(
                    {
                        "term_name": term_name,
                        "taxonomy_name": data.get("taxonomy_name"),
                        "taxonomy_id": tax_id,
                        "web_id": web_id,
                    }
                )
                .execute()
            )
            return response[1][0]
        except Exception as e:
            return str(e)

    def add_taxonomies_mapping(self, source_id, target_id):
        is_exist = self.check_taxonomies_mapping(source_id, target_id)
        if is_exist:
            return is_exist
        try:
            response, _ = (
                self._client.table("taxonomy_mapping")
                .insert(
                    {
                        "source_id": source_id,
                        "target_id": target_id,
                    }
                )
                .execute()
            )
            return response[1][0]
        except Exception as e:
            return str(e)

    def get_target_config(self, source_host, target_host):
        source, _ = (
            self._client.table("web")
            .select("id, url,language")
            .eq("url", source_host)
            .execute()
        )

        target, _ = (
            self._client.table("web")
            .select("id, url,language")
            .eq("url", target_host)
            .execute()
        )

        if len(target[1]) == 0 and len(source[1]) == 0:
            return None, None, None

        if len(source[1]) > 0:
            source_data = source[1][0]
        else:
            source_data = None

        if len(target) > 0:
            target_data = target[1][0]
            target_id = target_data.get("id")
            web_config = self.get_target_web_config(target_id)
        else:
            target_data = None
            web_config = None

        return source_data, target_data, web_config

    def get_target_web_config(self, web_id):
        result, _ = (
            self._client.table("web_config").select("*").eq("web_id", web_id).execute()
        )
        return result[1]


class SupaListWebHandler(Supabase):
    def get_websites_mapping(self):
        query = (
            "source:source_id(category:taxonomy_name, web: web_id(url))",
            "target:target_id(category:taxonomy_name, web: web_id(url))",
            "articles_mapping(count)",
        )

        mapping, _ = self._client.table("taxonomy_mapping").select(*query).execute()
        web = mapping[1]

        for w in web:
            yield {
                "source_url": w["source"]["web"]["url"],
                "source_category": w["source"]["category"],
                "target_url": w["target"]["web"]["url"],
                "target_category": w["target"]["category"],
                "count": w["articles_mapping"][0]["count"],
            }

    def get_article_by_status(self, status):
        articles, _ = (
            self._client.table("articles").select("*").eq("status", status).execute()
        )
        return articles[1]
