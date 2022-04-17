"""search entrance"""
# -*- encoding: utf-8 -*-
# @Author: RenZihou

from os import path

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse

from settings import IMAGE_PATH, TAG_INDEX_PATH, BM25_PATH
from engine import SearchEngine
from database import ImageDB

app = FastAPI()
se = SearchEngine(BM25_PATH, TAG_INDEX_PATH)


@app.get('/search')
async def search(query: str = '', tags: str = None):
    """
    search by text query
    :param query: query string
    :param tags: tag string
    :return:
    """
    image_ids = se.search(query, tags=tags.replace('+', ' ').split(',') if tags else None)
    result = []
    with ImageDB() as db:
        for image_id in image_ids:
            info = db.get_by_id(image_id)
            if info is not None:
                result.append(info)
    return {'code': 0, 'data': result}


@app.get('/image/{image_id}')
async def image(image_id: str):
    """
    get image by image id
    :param image_id: image id
    :return:
    """
    return FileResponse(path.join(IMAGE_PATH, f'{image_id}.jpg'))


@app.middleware('http')
async def add_header(request: Request, call_next):
    """add headers to avoid cors error"""
    resp = await call_next(request)
    resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:8080'
    resp.headers['Access-Control-Allow-Methods'] = 'POST,GET,PUT,DELETE'
    resp.headers['Access-Control-Allow-Headers'] = 'Origin,Content-Type,Accept'
    resp.headers['Access-Control-Allow-Credentials'] = 'true'
    return resp
