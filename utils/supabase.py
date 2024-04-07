import os
from dotenv import load_dotenv
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

load_dotenv()


class Supabase:
    def __init__(self):
        self.__url: str = os.environ.get("SUPABASE_URL")
        self.__key: str = os.environ.get("SUPABASE_KEY")
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


class SupaSeedTarget(Supabase):
    def add(self, data: dict):
        try:
            response = self._client.table("seed_target").insert(data).execute()
            return response.data
        except Exception as e:
            return str(e)

    def getAll(self):
        try:
            response = self._client.table("seed_target").select("*").execute()
            return response.data
        except Exception as e:
            return str(e)


class SupaSeedTaxonomy(Supabase):
    def check(self, taxonomy_id: int, target_id: int):
        try:
            response = (
                self._client.table("seed_taxonomies")
                .select("*")
                .eq("taxonomy_id", taxonomy_id)
                .eq("target_id", target_id)
                .maybe_single()
                .execute()
            )
            return response.data
        except Exception:
            return False

    def add(self, data: dict, target_id: int = 0):
        if target_id != 0:
            is_exist = self.check(data["taxonomy_id"], target_id)
        else:
            is_exist = False

        if is_exist:
            return is_exist
        try:
            data = {**data, "target_id": target_id}
            response = self._client.table("seed_taxonomies").insert(data).execute()
            return response.data[0]
        except Exception as e:
            return str(e)

    def getAll(self):
        try:
            response = self._client.table("seed_taxonomies").select("*").execute()
            return response.data
        except Exception as e:
            return str(e)


class SupaSeedKeywords(Supabase):
    def add(self, data: dict):
        try:
            response = self._client.table("seed_keywords").insert(data).execute()
            return response.data
        except Exception as e:
            return str(e)

    def addBulk(self, data: List[dict]):
        try:
            response = self._client.table("seed_keywords").insert(data).execute()
            return response.data
        except Exception as e:
            return str(e)

    def getAll(self):
        try:
            response = self._client.table("seed_keywords").select("*").execute()
            return response.data
        except Exception as e:
            return str(e)

    def getSpecific(
        self,
        status: str = None,
        target: str = None,
        per_page: int = 30,
        page: int = 1,
    ):

        query = (
            "keywords",
            "rewrite_date",
            "rewrite_mode",
            "status",
            "language",
            "public_url",
            "web: target_id!inner(url,username)",
            "taxonomy: tax_id!inner(taxonomy_name)",
        )

        try:
            response = self._client.table("seed_keywords").select(*query, count="exact")
            if status:
                response = response.eq("status", status)
            if target:
                response = response.like("web.url", f"%{target}%")

            response = response.limit(per_page).offset((page - 1) * per_page)

            response = response.execute()
            return response.data, response.count
        except Exception as e:
            return str(e)
