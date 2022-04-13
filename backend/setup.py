"""build index"""
# -*- encoding: utf-8 -*-
# @Author: RenZihou

import json

from index import InvertedIndexEngine
from processor import process_text


def build_inverted_index(doc: str, save_path: str):
    """build inverted index from single file"""
    index = InvertedIndexEngine()
    with open(doc, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            index.add_doc(data['image_id'], process_text(data['caption']))
    index.save(save_path)


def build_tag_index(doc: str, tag: str, save_path: str):
    """build tag index from single file"""
    alias_map = {}
    with open(tag, 'r', encoding='utf-8') as f:
        for line in f:
            alias, tag = line.strip().split(',')
            alias_map[alias] = tag
    index = InvertedIndexEngine(alias_map)
    with open(doc, 'r', encoding='utf-8') as f:
        for line in f:
            image_id, alias = line.strip().split(',')
            index.add_doc(image_id, (alias,))
    index.save(save_path)


if __name__ == '__main__':
    build_inverted_index('D:/storage/meta/text-label.jsonl', 'data/index.pkl')
    build_tag_index('D:/storage/meta/class-label.csv', 'D:/storage/meta/class-descriptions.csv',
                    'data/tag_index.pkl')
