import os
from src.search.client import Search
from src.utils import insert_into_db
from src.collection import ArticleCollection
import sqlite3
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--api_key", default=None)
    parser.add_argument("--from_year", type=int)
    parser.add_argument("--search", action="append")
    parser.add_argument("--count", type=int, default=30)
    parser.add_argument("--get_all", type=bool, default=False)
    args = parser.parse_args()

    articles = {}
    article_collection = ArticleCollection()
    searcher = Search(count=args.count, get_all=args.get_all)
    if  args.api_key:
    # scopus
        articles["scopus"] = searcher.search_scopus(
            api_key=args.api_key,
            keywords=args.search,
            from_year=args.from_year,
            searching_index="scopus",
        )
        article_collection.process_article_scopus(articles["scopus"].results)

    # paperswithml
    articles["paperswithml"] = searcher.search_on_paperswithml(
        query=" ".join(args.search)
    )
    article_collection.process_articles_paperswithml(
        articles["paperswithml"]["results"]
    )

    articles = article_collection.to_df()

    # transform
    articles["search_tags"] = ", ".join(args.search)

    # load
    insert_into_db("articles", articles)
    pass
