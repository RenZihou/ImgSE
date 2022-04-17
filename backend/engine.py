"""search engine"""
# -*- encoding: utf-8 -*-
# @Author: RenZihou

from typing import Optional

import dill as pickle

from processor import process_text


class SearchEngine:
    """search engine"""
    def __init__(self, bm25_pkl: str, tag_index_pkl: str):
        with open(bm25_pkl, 'rb') as bm25, open(tag_index_pkl, 'rb') as ti:
            self.bm25 = pickle.load(bm25)
            self.tag_index = pickle.load(ti)

    def search(self, query: str, /, tags: Optional[list] = None, n: int = 20) -> list:
        """
        search query
        :param query: query string
        :param tags: tag list
        :param n: number of results
        :return: list of image_id
        """
        if tags is None:
            tags = []
        words = process_text(query)
        if len(words) == 0 and len(tags) == 0:
            return []
        if query in self.tag_index.index and query not in tags:
            tags.append(query)
        results = self.bm25.get(words, n=-1)
        return self._filter(results, tags=tags)[:n]

    def _filter(self, results: list, /, tags: Optional[list] = None) -> list:
        """
        filter search results
        :param results: original search results
        :param tags: tag list
        :return: filtered results, also list of image_id
        """
        if tags:
            tag_filter = set.intersection(*[set(self.tag_index.get(tag)) for tag in tags])
            return [r for r in results if r in tag_filter]
        else:
            return results


if __name__ == '__main__':
    se = SearchEngine('data/bm25.pkl', 'data/tag_index.pkl')
    print(se.search('a child playing'))
    pass
