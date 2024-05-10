import unittest
from src.search.client import Search


class TestSearch(unittest.TestCase):
    def test_search_paper_with_ml(self):
        s = Search(count=30)
        res = s.search_on_paperswithml("Short Term Time Series")
        return res
