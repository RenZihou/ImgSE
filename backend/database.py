"""database entrance"""
# -*- encoding: utf-8 -*-
# @Author: RenZihou

import sqlite3
from os import path

from settings import DATABASE_PATH


class ImageDB(object):
    """
    connect to the database
    """

    def __init__(self, db: str = DATABASE_PATH):
        self.conn = sqlite3.connect(path.join(path.dirname(__file__), db))
        self.cur = self.conn.cursor()
        self.columns = ('image_id', 'desc')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def get_by_id(self, image_id: str):
        """get image info by id"""
        info = self.cur.execute('SELECT * FROM info WHERE image_id = ?', (image_id,)).fetchone()
        return dict(zip(self.columns, info)) if info else None

    def set_by_id(self, image_id: str, /, desc: str):
        """set image info by id"""
        if self.cur.execute('SELECT * FROM info WHERE image_id = ?', (image_id,)).fetchone():
            self.cur.execute('UPDATE info SET desc = ? WHERE image_id = ?', (desc, image_id))
        else:
            self.cur.execute('INSERT INTO info(image_id, desc) VALUES (?, ?)', (image_id, desc))
