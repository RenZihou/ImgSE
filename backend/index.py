"""inverted index engine"""
# -*- encoding: utf-8 -*-
# @Author: RenZihou

from collections import defaultdict

import dill as pickle
from rank_bm25 import BM25Okapi
from sklearn.neighbors import BallTree
import numpy as np


class IndexEngine:
    """(inverted) index engine"""

    def __init__(self):
        self.index = defaultdict(set)

    def add_doc(self, doc_id: str, doc_words: list):
        """add a new document"""
        for word in doc_words:
            self.index[word].add(doc_id)

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

    def add_doc(self, doc_id: str, doc_words: list):
        """add a new document"""
        self.doc_id.append(doc_id)
        self.tokenized_corpus.append(doc_words)

    def build_index(self):
        """parse tokenized corpus"""
        self.bm25 = BM25Okapi(self.tokenized_corpus)
        self.doc_id = tuple(self.doc_id)
        del self.tokenized_corpus
        return self

    def get(self, tokenized_query: list, n: int = 20):
        """get results from BM25"""
        return self.bm25.get_top_n(tokenized_query, self.doc_id, n=n)

    def save(self, filename: str):
        """save the BM25 engine to a file"""
        with open(filename, 'wb') as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)


class BallTreeEngine:
    """ball tree"""

    def __init__(self):
        self.ball_tree = None
        self.img_id = []
        self.img_vec = []

    def add_img(self, img_id: str, img_vec: np.array):
        """add a new image"""
        self.img_id.append(img_id)
        self.img_vec.append(img_vec)

    def build_tree(self):
        """build tree"""
        self.ball_tree = BallTree(self.img_vec)
        self.img_id = tuple(self.img_id)
        del self.img_vec
        return self

    def get(self, query_vec: np.array, n: int = 20):
        """get results from ball tree"""
        _, result = self.ball_tree.query((query_vec,), k=n)
        return list(map(lambda x: self.img_id[x], result[0]))

    def save(self, filename: str):
        """save the ball tree to a file"""
        with open(filename, 'wb') as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)
