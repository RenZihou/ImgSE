"""define constants here"""
# -*- encoding: utf-8 -*-
# @Author: RenZihou

IMAGE_PATH = 'D:/storage/images/'
BM25_PATH = 'C:/users/alex/projects/ImgSE/backend/data/bm25.pkl'
TAG_INDEX_PATH = 'C:/users/alex/projects/ImgSE/backend/data/tag_index.pkl'
BALL_TREE_PATH = 'C:/users/alex/projects/ImgSE/backend/data/bt_hist.pkl'
DATABASE_PATH = 'C:/users/alex/projects/ImgSE/backend/data/info.sqlite'

IMAGE_PIXELS_THRESHOLD = {
    'xs': (0, 600_000),
    's': (600_000, 2_000_000),
    'm': (2_000_000, 5_000_000),
    'l': (5_000_000, 10_000_000),
    'xl': (10_000_000, 100_000_000),
}

MAX_RESULT = 500  # max results number of text-to-image search
MAX_IMAGE_RESULT = 50  # max results number of image-to-image search

# credit: https://gist.github.com/sebleier/554280
# set takes O(1) time for `in` operation
STOP_WORDS = {
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself',
    'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its',
    'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom',
    'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
    'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but',
    'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about',
    'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to',
    'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then',
    'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few',
    'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
    'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now',
    '.', ',', ':', ';', '?', '!', '-', '_', '"', '\'', '\\', '/', '|', '@', '#', '$', '%', '^', '&',
    '*', '(', ')', '+', '=', '{', '}', '[', ']', '<', '>', '~', '`',
}

COLORS = {
    'red': (244, 67, 54),
    'orange': (255, 152, 0),
    'yellow': (255, 235, 59),
    'green': (76, 175, 80),
    'teal': (0, 150, 136),
    'blue': (63, 81, 181),
    'purple': (156, 39, 176),
    'pink': (233, 30, 99),
    'white': (255, 255, 255),
    'grey': (158, 158, 158),
    'black': (0, 0, 0),
    'brown': (121, 85, 72),
}

HLS_BINS = (6, 12, 3)
