#!/usr/bin/env python
import time
import requests
from bs4 import BeautifulSoup
from imageExtensions import imageExtensions
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
        self.EXTENSIONS = imageExtensions().EXTENSIONS

    def textStrip(self, text):
        return text.replace('\r', '').replace('\n', '')

    def processImage(self, img):
        text = self.itt.processImage(self.itt.getImage(img), self.lang,
                                     self.tessDir)
        return self.textStrip(text)

    def getMemeText(self, imageUrl):
            # special case for imgflip. get text from alt attr of image
            if 'imgflip' in imageUrl:
                imgFlipUrl = self.gi.imgFlipUrlTransform(imageUrl)
                memeList = self.gi.getImgFlip(imgFlipUrl)
                memeType = memeList[0]
                text = memeList[1]
                return text
            # special case for makeameme. get text from body
            elif 'makeameme' in imageUrl:
                makeAMemeUrl = self.gi.makeAMemeTransform(imageUrl)
                memeList = self.gi.getMakeAMeme(makeAMemeUrl)
                memeType = memeList[0]
                text = memeList[1]
                return text
            elif 'livememe' in imageUrl or 'lvme.me' in imageUrl:
                liveMemeUrl = self.gi.liveMemeTransform(imageUrl)
                memeList = self.gi.getLiveMeme(liveMemeUrl)
                memeType = memeList[0]
                memeText = memeList[1]
                text = ''
                for i in memeText:
                    text += i.strip() + '\n'
                return text
            elif 'i.memecaptain' in imageUrl:
                pass
            elif 'memecaptain' in imageUrl:
                pass
            elif 'm.memegen' in imageUrl:
                pass
            elif 'memegen' in imageUrl:
                pass
            # imgur webpage. get direct image and run ocr
            elif '//imgur' in imageUrl:
                img = self.gi.getImgur(imageUrl)
                return self.processImage(img)
            # direct image urls. primarily imgur and i.redd.it
            elif any(ext in imageUrl for ext in self.EXTENSIONS):
                return self.processImage(imageUrl)
            # website urls. need to get text if exists or img to run ocr on
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
    # subredditUrl = 'https://www.reddit.com/domain/livememe.com/.json'
    user = 'craptionb0t'
    key = 'url'

    lang = 'joh'
    tessDir = os.path.dirname(os.path.realpath(__file__))
    tessDir += 'tessdata'

    b = bot(lang, tessDir)
    b.getMemeTextAll(subredditUrl, user, key)
