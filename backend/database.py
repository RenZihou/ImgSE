"""database entrance"""
# -*- encoding: utf-8 -*-
# @Author: RenZihou

import sqlite3
from os import path
import json

from settings import DATABASE_PATH


class ImageDB(object):
    """
    connect to the database
    """

    def __init__(self, db: str = DATABASE_PATH):
        self.conn = sqlite3.connect(path.join(path.dirname(__file__), db))
        self.cur = self.conn.cursor()
        self.columns = ('image_id', 'desc', 'tags')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def get_by_id(self, image_id: str):
        """get image info by id"""
        info = self.cur.execute('SELECT * FROM info WHERE image_id = ?', (image_id,)).fetchone()
        if info:
            result = dict(zip(self.columns, info))
            result['tags'] = json.loads(result['tags'])
            return result
        return None

    def set_desc(self, image_id: str, desc: str):
        """set image desc by id"""
        if self.cur.execute('SELECT * FROM info WHERE image_id = ?', (image_id,)).fetchone():
            self.cur.execute('UPDATE info SET desc = ? WHERE image_id = ?', (desc, image_id))
        else:
            self.cur.execute('INSERT INTO info(image_id, desc) VALUES (?, ?)', (image_id, desc))

    def set_tags(self, image_id: str, tags: list, append: bool = False):
        """
        set image tags by id
        :param image_id: image id
        :param tags: tags list
        :param append: whether append to (otherwise replace) existing tags
        """
        old = self.cur.execute('SELECT tags FROM info WHERE image_id = ?', (image_id,)).fetchone()
        if old:
            tags = list(set(json.loads(old[0]) + tags)) if append else tags
            self.cur.execute('UPDATE info SET tags = ? WHERE image_id = ?',
                             (json.dumps(tags), image_id))
        else:
            self.cur.execute('INSERT INTO info(image_id, tags) VALUES (?, ?)',
                             (image_id, json.dumps(tags)))
