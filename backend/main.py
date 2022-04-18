"""search entrance"""
# -*- encoding: utf-8 -*-
# @Author: RenZihou

from os import path

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse

from settings import IMAGE_PATH, TAG_INDEX_PATH, BM25_PATH
from engine import SearchEngine

app = FastAPI()
se = SearchEngine(BM25_PATH, TAG_INDEX_PATH)


@app.get('/search')
async def search(query: str = '', tags: str = '', pixels: str = '', color: str = '',
                 continue_from: int = 0):
    """
    search by text query
    :param query: query string
    :param tags: tag list
    :param pixels: pixel option list
    :param color: color name
    :param continue_from: continue filter from which index of bm25 result
    :return:
    """
    results, count = se.search(query,
                               tags=tags.replace('+', ' ').split(',') if tags else None,
                               pixels=pixels.split(',') if pixels else None,
                               color=color,
                               continue_from=continue_from if continue_from else 0)
    return {'code': 0, 'data': results, 'continue_from': count}


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
    resp.headers['Access-Control-Allow-Methods'] = 'GET'
    resp.headers['Access-Control-Allow-Headers'] = 'Origin,Content-Type,Accept'
    resp.headers['Access-Control-Allow-Credentials'] = 'true'
    return resp
