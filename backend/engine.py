"""search engine"""
# -*- encoding: utf-8 -*-
# @Author: RenZihou

import dill as pickle

from processor import process_text


class SearchEngine:
    """search engine"""
    def __init__(self, bm25_pkl: str, tag_index_pkl: str):
        with open(bm25_pkl, 'rb') as bm25, open(tag_index_pkl, 'rb') as ti:
            self.bm25 = pickle.load(bm25)
            self.tag_index = pickle.load(ti)

    def search(self, query: str) -> list:
        """
        search query
        :param query: query string
        # :param tag: tag list
        :return: list of image_id
        """
        words = process_text(query)
        if len(words) == 0:
            return []
        if len(words) == 1 and words[0] in self.tag_index:
            return self.tag_index[words[0]]
        return self.bm25.get(words)


if __name__ == '__main__':
    se = SearchEngine('data/bm25.pkl', 'data/tag_index.pkl')
    print(se.search('a child playing'))
    pass
