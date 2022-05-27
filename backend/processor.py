"""text and image processors"""
# -*- encoding: utf-8 -*-
# @Author: RenZihou

import cv2
import numpy as np

from settings import STOP_WORDS, COLORS, HLS_BINS


def process_text(text: str) -> list:
    """
    1. split words
    2. lowercase
    3. remove stop words and punctuation
    :param text: string to process
    :return: filtered words
    """
    return list(filter(lambda w: w not in STOP_WORDS,
                       map(lambda w: w.lower(), text.split())))


def extract_image_info(image) -> tuple:
    """
    1. find pixels number
    2. find dominant color and classify it
    :param image: PIL.Image object
    :return: (pixels, color)
    """
    w, h = image.size
    color_rgb = image.convert('RGB').resize((1, 1), resample=0).getpixel((0, 0))
    distance = {k: sum(map(lambda x: abs(x[0] - x[1]), zip(color_rgb, v)))
                for k, v in COLORS.items()}
    color = min(
        distance,
        key=distance.get
    )
    return w * h, color


# credit: https://github.com/sherlockchou86/cbir-image-search
def extract_image_color_feature(image) -> np.array:
    """
    extract image region-based color histogram feature
    :param image: PIL.Image object
    :return:
    """
    features = np.array([])
    try:
        image_hls = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2HLS)
    except cv2.error:
        return None
    h, w = image_hls.shape[:2]
    ch, cw = h // 2, w // 2
    # top-left, top-right, bottom-left, bottom-right regions
    segments = [(0, cw, 0, ch), (cw, w, 0, ch), (cw, w, ch, h), (0, cw, ch, h)]
    # central elliptical region
    mask_e = np.zeros(image_hls.shape[:2], dtype=np.uint8)
    cv2.ellipse(mask_e, (cw, ch), (3 * w // 8, 3 * h // 8), 0, 0, 360, 255, -1)
    for x1, x2, y1, y2 in segments:
        # extract histogram for each corner region
        mask = np.zeros(image_hls.shape[:2], dtype=np.uint8)
        cv2.rectangle(mask, (x1, y1), (x2, y2), 255, -1)
        mask = cv2.subtract(mask, mask_e)
        hist = cv2.calcHist((image_hls,), (0, 1, 2), mask, HLS_BINS, (0, 180, 0, 255, 0, 255))
        hist = cv2.normalize(hist, hist).flatten()
        features = np.hstack((features, hist))
    # extract histogram for central elliptical region
    hist = cv2.calcHist((image_hls,), (0, 1, 2), mask_e, HLS_BINS, (0, 180, 0, 255, 0, 255))
    hist = cv2.normalize(hist, hist).flatten()
    features = np.hstack((features, hist))
    return features
