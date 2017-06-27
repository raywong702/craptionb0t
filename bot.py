#!/usr/bin/env python
import time
import requests
from bs4 import BeautifulSoup
from redditParser import redditParser
from imageToText import imageToText
from getImage import getImage


class bot(object):
    def __init__(self, lang, tessDir):
        self.rp = redditParser()
        self.itt = imageToText()
        self.gi = getImage()
        self.lang = lang
        self.tessDir = tessDir
        self.extensions = ('.jpg',
                           '.png'
                           )

    def textStrip(self, text):
        return text.replace('\r', '').replace('\n', '')

    def processImage(self, img):
        text = self.itt.processImage(self.itt.getImage(img), self.lang,
                                     self.tessDir)
        return self.textStrip(text)

    def getMemeText(self, imageUrl):
            # special case for imgflip. get text from alt attr of image
            if 'imgflip' in imageUrl:
                imgflipUrl = self.gi.imgflipUrlTransform(imageUrl)
                return self.gi.getImgFlip(imgflipUrl)[1].strip()
            # direct image urls that are not imgflip. run ocr
            elif any(ext in imageUrl for ext in self.extensions):
                return self.processImage(imageUrl)
            # website urls. get direct image and run ocr
            else:
                if 'imgur' in imageUrl:
                    img = self.gi.getImgur(imageUrl)
                    return self.processImage(img)
                else:
                    return '*' * 10

    def getMemeTextAll(self, subredditUrl, user, key):
        _json = self.rp.getRedditJson(subredditUrl, user)
        while 'data' not in _json:
            time.sleep(4)
            _json = redditParser.getRedditJson(subredditUrl, user)

        gen = self.rp.getParsedRedditJson(_json, key)
        divider = '-' * 50
        print(divider)
        for i, urlKey in enumerate(gen):
            print(f'{i:02}')
            print(f'{urlKey}')
            print(self.getMemeText(urlKey))
            print('')
            print(divider)


if __name__ == '__main__':
    import os

    subredditUrl = 'https://www.reddit.com/r/AdviceAnimals/top/'
    subredditUrl += '.json?sort=top&t=week'
    user = 'craptionb0t'
    key = 'url'

    lang = 'joh'
    tessDir = os.path.dirname(os.path.realpath(__file__))
    tessDir += 'tessdata'

    b = bot(lang, tessDir)
    b.getMemeTextAll(subredditUrl, user, key)
