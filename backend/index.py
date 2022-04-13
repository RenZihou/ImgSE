"""inverted index engine"""
# -*- encoding: utf-8 -*-
# @Author: RenZihou

from collections import defaultdict
import dill as pickle


class InvertedIndexEngine:
    """inverted index engine"""
    def __init__(self, alias_map: dict = None):
        self.index = defaultdict(set)
        if alias_map is None:
            self.alias_map = lambda x: x
        else:
            self.alias_map = lambda x: alias_map[x] if x in alias_map else x

    def add_doc(self, doc_id, doc_words):
        """add a new document"""
        for word in doc_words:
            self.index[self.alias_map(word)].add(doc_id)

    def get(self, word):
        """get the documents that contain the word"""
        return self.index[word]

    def save(self, filename):
        """save the inverted index to a file"""
        with open(filename, 'wb') as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)
