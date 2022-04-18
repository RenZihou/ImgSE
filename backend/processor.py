"""text and image processors"""
# -*- encoding: utf-8 -*-
# @Author: RenZihou

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

# credit: https://www.rapidtables.com/web/color/RGB_Color.html
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


def process_image(image) -> tuple:
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
