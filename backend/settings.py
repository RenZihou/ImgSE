"""define constants here"""
# -*- encoding: utf-8 -*-
# @Author: RenZihou

IMAGE_PATH = 'D:/storage/images/'
BM25_PATH = 'C:/users/alex/projects/ImgSE/backend/data/bm25.pkl'
TAG_INDEX_PATH = 'C:/users/alex/projects/ImgSE/backend/data/tag_index.pkl'
DATABASE_PATH = 'C:/users/alex/projects/ImgSE/backend/data/info.sqlite'

IMAGE_PIXELS_THRESHOLD = {
    'xs': (0, 600_000),
    's': (600_000, 2_000_000),
    'm': (2_000_000, 5_000_000),
    'l': (5_000_000, 10_000_000),
    'xl': (10_000_000, 100_000_000),
}
