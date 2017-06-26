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

    def getMemeText(self, url, user, key):
        _json = self.rp.getRedditJson(url, user)
        while 'data' not in _json:
            time.sleep(4)
            _json = redditParser.getRedditJson(url, user)

        gen = self.rp.getParsedRedditJson(_json, key)
        divider = '-' * 50
        print(divider)
        for i, k in enumerate(gen):
            if any(ext in k for ext in self.extensions):
                text = self.itt.processImage(self.itt.getImage(k), self.lang,
                                             self.tessDir)
                text = text.replace('\r', '').replace('\n', '')
                print(f'{i:02}')
                print(f'{k}')
                print(f'{text}')
                print('')
                print(divider)
            else:
                if 'imgflip' in k:
                    print(f'{i:02}')
                    print(f'{k}')
                    print(self.gi.getImgFlip(k)[1].strip())
                    print('')
                    print(divider)
                else:
                    print(f'{i:02}')
                    print(f'{k}')
                    print('')
                    print(divider)


if __name__ == '__main__':
    import os

    url = 'https://www.reddit.com/r/AdviceAnimals/top/.json?sort=top&t=week'
    user = 'craptionb0t'
    key = 'url'

    lang = 'joh'
    tessDir = os.path.dirname(os.path.realpath(__file__))
    tessDir += 'tessdata'

    b = bot(lang, tessDir)
    b.getMemeText(url, user, key)
