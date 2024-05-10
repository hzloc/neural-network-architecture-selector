from typing import Optional
from elsapy import elsclient, elssearch
import requests


class Search:
    def __init__(self, count: int = 25, get_all: bool = False):
        self.get_all = get_all
        self.count = count

    def search_scopus(
        self,
        api_key: str,
        keywords: list[str],
        from_year: int = 2018,
        searching_index: str = "scopus",
    ):
        keywords = " AND ".join(keywords)
        els_auth = elsclient.ElsClient(api_key)
        search = elssearch.ElsSearch(
            f"""TITLE-ABS-KEY({keywords}) AND PUBYEAR > {from_year} AND LANGUAGE(ENGLISH)""",
            searching_index,
        )
        search.execute(
            els_auth,
            get_all=self.get_all,
            count=self.count,
        )
        return search

    def search_on_paperswithml(self, query: str, page: int = 1):
        if page < 1:
            raise Exception("Invalid page number!")

        url = "https://paperswithcode.com/api/v1/search"
        resp = requests.get(
            url, params={"q": query, "items_per_page": self.count, "page": page}
        )
        return resp.json()
