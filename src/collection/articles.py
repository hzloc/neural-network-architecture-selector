import pandas as pd

import json
from typing import Optional, Union, List
from dataclasses import dataclass, field
from collections.abc import Collection


@dataclass(slots=True)
class Article:
    id: str
    title: str
    creator: Union[str, List]
    cover_date: str
    url: str
    sources: str
    created_at = None
    cite_count: Optional[str] = field(default=None)
    doi: Optional[str] = field(default=None)
    document_type: Optional[str] = field(default=None)

    def to_tuple(self):
        return tuple(
            [
                self.id,
                self.title,
                self.creator,
                self.cover_date,
                self.cite_count,
                self.doi,
                self.url,
                self.document_type,
                self.sources,
            ]
        )


class ArticleCollection(Collection):

    def __init__(self):
        self.articles: [Article] = []

    def __contains__(self, __x):
        if __x in self.articles:
            return True
        return False

    def __iter__(self):
        return self.articles.__iter__()

    def __len__(self):
        return len(self.articles)

    def __getitem__(self, item):
        return self.articles[item]

    def process_article_scopus(self, raw_articles: [dict]):
        if not raw_articles:
            return None
        for article in raw_articles:
            id = article["eid"]
            title = article["dc:title"]
            creator = article.get("dc:creator")
            cover_date = article.get("prism:coverDate")
            cite_count = article["citedby-count"]
            doi = article.get("prism:doi")
            url = article["prism:url"]
            document_type = article["subtypeDescription"]
            sources = "scopus"
            self.articles.append(
                Article(
                    id,
                    title,
                    creator,
                    cover_date,
                    cite_count,
                    doi,
                    url,
                    document_type,
                    sources,
                )
            )

    def process_articles_paperswithml(self, raw_articles: [dict]):
        if not raw_articles:
            return None
        for article in raw_articles:
            paper = article["paper"]
            id = paper["id"]
            title = paper["title"]
            cover_date = paper["published"]
            url = paper["url_pdf"]
            creator = paper.get("authors", None)
            if creator is not None:
                creator = ", ".join(creator)
            sources = "paperwithml"
            self.articles.append(
                Article(
                    id=id,
                    title=title,
                    cover_date=cover_date,
                    url=url,
                    creator=creator,
                    sources=sources,
                )
            )

    def to_df(self):
        articles = pd.DataFrame(self.articles, columns=Article.__slots__)
        return articles
