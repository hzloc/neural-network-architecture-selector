from src.utils.db import read_from_table, get_already_scored_articles
from src.utils.styler import highlight_already_scored_articles
import unittest


class TestDb(unittest.TestCase):
    def test_read_from_database(self):
        res = read_from_table("articles")
        pass

    def test_get_already_scored_articles(self):
        articles = get_already_scored_articles()
        return articles
