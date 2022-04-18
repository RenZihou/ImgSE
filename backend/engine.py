"""search engine"""
# -*- encoding: utf-8 -*-
# @Author: RenZihou

from typing import Optional, Tuple

import dill as pickle

from database import ImageDB
from processor import process_text
from settings import IMAGE_PIXELS_THRESHOLD


class SearchEngine:
    """search engine"""

    def __init__(self, bm25_pkl: str, tag_index_pkl: str):
        with open(bm25_pkl, 'rb') as bm25, open(tag_index_pkl, 'rb') as ti:
            self.bm25 = pickle.load(bm25)
            self.tag_index = pickle.load(ti)

    def search(self, query: str, /,
               tags: Optional[list] = None, pixels: Optional[list] = None,
               n: int = 20, continue_from: int = 0) -> Tuple[list, int]:
        """
        search query
        :param query: query string
        :param tags: tag list
        :param pixels: pixels size list
        :param n: number of results
        :param continue_from: continue from which bm25 result index
        :return: list of image_id
        """
        if tags is None:
            tags = []
        words = process_text(query)
        if len(words) == 0 and len(tags) == 0:
            return [], 0
        if query in self.tag_index.index and query not in tags:
            tags.append(query)
        results = self.bm25.get(words, n=-1)[continue_from:]
        abstracts, count = self._abstract(results, tags=tags, pixels=pixels, n=n)
        return abstracts, count + continue_from

    def _abstract(self, results: list, /,
                  tags: Optional[list] = None, pixels: Optional[list] = None,
                  n: int = 20) -> Tuple[list, int]:
        """
        generate abstract from result image_id list
        :param results: image id list
        :return: abstract result
        """
        tag_filter = set.intersection(*[set(self.tag_index.get(tag)) for tag in tags])\
            if tags else None
        abstracts = []
        count = 0
        valid = 0
        with ImageDB() as db:
            for image_id in results:
                valid += 1
                if tag_filter and image_id not in tag_filter:
                    continue
                info = db.get_by_id(image_id)
                if all((info is not None,
                        self._meet_pixels_threshold(info, pixels),)):
                    abstracts.append(info)
                    count += 1
                    if count >= n:
                        break
        return abstracts, count

    @staticmethod
    def _meet_pixels_threshold(image_info: dict, pixels_threshold: list) -> bool:
        """
        judge whether given image meet pixels' threshold
        :param image_info:
        :param pixels_threshold:
        :return:
        """
        if pixels_threshold is None:
            return True
        return any([
            IMAGE_PIXELS_THRESHOLD[th][0] <= image_info['pixels'] < IMAGE_PIXELS_THRESHOLD[th][1]
            for th in pixels_threshold])
