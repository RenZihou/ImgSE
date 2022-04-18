"""build index"""
# -*- encoding: utf-8 -*-
# @Author: RenZihou

import json
from collections import defaultdict
from os import path, listdir

from index import IndexEngine, BM25Engine
from processor import process_text, process_image
from database import ImageDB
from PIL import Image

from settings import BM25_PATH, TAG_INDEX_PATH


def build_text(doc_path: str):
    """build inverted index from text file"""
    bm25 = BM25Engine()
    with open(doc_path, 'r', encoding='utf-8') as f, ImageDB() as db:
        for line in f:
            data = json.loads(line)
            bm25.add_doc(data['image_id'], process_text(data['caption']))
            db.set_desc(data['image_id'], desc=data['caption'])
    bm25.parse_corpus().save(BM25_PATH)


def build_tag(tag_label_path: str, tag_desc_path: str):
    """build tag index from single file"""
    alias_map = {}
    tag_map = defaultdict(list)
    with open(tag_desc_path, 'r', encoding='utf-8') as f:
        for line in f:
            alias, tag = line.strip().split(',')
            alias_map[alias] = tag
    with open(tag_label_path, 'r', encoding='utf-8') as f:
        for line in f:
            image_id, alias = line.strip().split(',')
            tag_map[image_id].append(alias_map[alias])
    index = IndexEngine()
    with ImageDB() as db:
        for image_id, tags in tag_map.items():
            db.set_tags(image_id, tags=tags)
            index.add_doc(image_id, tags)
    index.save(TAG_INDEX_PATH)


def build_image(image_path: str):
    """save image info to database"""
    with ImageDB() as db:
        for image_filename in listdir(image_path):
            image = Image.open(path.join(image_path, image_filename))
            pixels, color = process_image(image)
            db.set_pixels(image_filename[:-4], pixels)  # add info of pixel size
            db.set_color(image_filename[:-4], color)  # add info of dominant color


if __name__ == '__main__':
    # build_text('D:/storage/meta/text-label.jsonl')
    # build_tag('D:/storage/meta/class-label.csv', 'D:/storage/meta/class-descriptions.csv')
    build_image('D:/storage/images')
