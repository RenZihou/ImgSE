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
