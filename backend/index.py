"""inverted index engine"""
# -*- encoding: utf-8 -*-
# @Author: RenZihou

from collections import defaultdict

import dill as pickle
from rank_bm25 import BM25Okapi


class IndexEngine:
    """(inverted) index engine"""
    def __init__(self, alias_map: dict = None):
        self.index = defaultdict(set)
        if alias_map is None:
            self.alias_map = lambda x: x
        else:
            self.alias_map = lambda x: alias_map.get(x, default=None) or x

    def add_doc(self, doc_id, doc_words):
        """add a new document"""
        for word in doc_words:
            self.index[self.alias_map(word)].add(doc_id)

    def get(self, word: str):
        """get the documents that contain the word"""
        return self.index[word]

    def save(self, filename: str):
        """save the inverted index to a file"""
        with open(filename, 'wb') as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)


class BM25Engine:
    """BM25 engine"""
    def __init__(self):
        self.bm25 = None
        self.doc_id = []
        self.tokenized_corpus = []

    def add_doc(self, doc_id, doc_words):
        """
        add a new document
        :param doc_id:
        :param doc_words:
        :return:
        """
        self.doc_id.append(doc_id)
        self.tokenized_corpus.append(doc_words)

    def parse_corpus(self):
        """
        parse tokenized corpus
        :return:
        """
        self.bm25 = BM25Okapi(self.tokenized_corpus)
        self.tokenized_corpus = []
        return self

    def get(self, tokenized_query: list, n: int = 20):
        """get results from BM25"""
        return self.bm25.get_top_n(tokenized_query, self.doc_id, n=n)

    def save(self, filename: str):
        """save the BM25 engine to a file"""
        with open(filename, 'wb') as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)
