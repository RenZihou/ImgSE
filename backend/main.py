"""search entrance"""
# -*- encoding: utf-8 -*-
# @Author: RenZihou

from os import path
from typing import Union

from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from engine import TextSearchEngine, ImageSearchEngine
from settings import IMAGE_PATH, TAG_INDEX_PATH, BM25_PATH, BALL_TREE_PATH

app = FastAPI()
tse = TextSearchEngine(BM25_PATH, TAG_INDEX_PATH)
ise = ImageSearchEngine(BALL_TREE_PATH, TAG_INDEX_PATH)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:8080', 'http://localhost:3000'],
    allow_credentials=True,
    allow_methods=['GET', 'POST'],
    allow_headers=['Origin,Content-Type,Accept'],
)


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
    results, count = tse.search(query,
                                tags=tags.replace('+', ' ').split(',') if tags else None,
                                pixels=pixels.split(',') if pixels else None,
                                color=color,
                                continue_from=continue_from if continue_from else 0)
    return {'code': 0, 'data': results, 'continue_from': count}


@app.post('/search')
async def search_by_image(query: Union[str, UploadFile] = Form(...)):
    """
    search by image
    :param query: query image file
    :return:
    """
    results = ise.search(path.join(IMAGE_PATH, f'{query}.jpg') if isinstance(query, str)
                         else query.file)
    return {'code': 0, 'data': results}


@app.get('/image/{image_id}')
async def get_image(image_id: str):
    """
    get image by image id
    :param image_id: image id
    :return:
    """
    return FileResponse(path.join(IMAGE_PATH, f'{image_id}.jpg'))
