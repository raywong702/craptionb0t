#!/usr/bin/env python
import time
import requests
from bs4 import BeautifulSoup
from image_extensions import ImageExtensions
from reddit_parser import RedditParser
from image_to_text import ImageToText
from get_image_text import GetImage


class Bot(object):
    def __init__(self, lang, tessDir):
        self.rp = RedditParser()
        self.itt = ImageToText()
        self.gi = GetImage()
        self.lang = lang
        self.tessDir = tessDir
        self.EXTENSIONS = ImageExtensions().EXTENSIONS

    def strip_text(self, text):
        return text.replace('\r', '').replace('\n', '')

    def process_image(self, img):
        text = self.itt.process_image(self.itt.get_image(img), self.lang,
                                      self.tessDir)
        return self.strip_text(text)

    def get_meme_text(self, imageUrl):
            # special case for imgflip. get text from alt attr of image
            if 'imgflip' in imageUrl:
                imgFlipUrl = self.gi.transform_imgflip_url(imageUrl)
                memeList = self.gi.get_imgflip(imgFlipUrl)
                memeType = memeList[0]
                text = memeList[1]
                return text
            # special case for makeameme. get text from body
            elif 'makeameme' in imageUrl:
                makeAMemeUrl = self.gi.transform_makeameme_url(imageUrl)
                memeList = self.gi.get_makeameme(makeAMemeUrl)
                memeType = memeList[0]
                text = memeList[1]
                return text
            elif 'livememe' in imageUrl or 'lvme.me' in imageUrl:
                liveMemeUrl = self.gi.transform_livememe_url(imageUrl)
                memeList = self.gi.get_livememe(liveMemeUrl)
                memeType = memeList[0]
                memeText = memeList[1]
                text = ''
                for i in memeText:
                    text += i.strip() + '\n'
                return text
            elif 'memecaptain' in imageUrl:
                memeCaptainUrl = self.gi.transform_memecaptain_url(imageUrl)
                memeList = self.gi.get_memecaptain(memeCaptainUrl)
                memeType = memeList[0]
                memeText = memeList[1]
                text = ''
                for i in memeText:
                    text += i.strip() + '\n'
                return text
            elif 'memegen' in imageUrl:
                memeGenUrl = self.gi.transform_memegen_url(imageUrl)
                memeList = self.gi.get_memegen(memeGenUrl)
                memeType = memeList[0]
                text = memeList[1]
                if text == None and self.gi.is_memegen_direct_url(imageUrl):
                    text = self.process_image(imageUrl)
                return text
            # imgur webpage. get direct image and run ocr
            elif '//imgur' in imageUrl:
                img = self.gi.get_imgur(imageUrl)
                return self.process_image(img)
            # direct image urls. primarily imgur and i.redd.it
            elif any(ext in imageUrl for ext in self.EXTENSIONS):
                return self.process_image(imageUrl)
            # website urls. need to get text if exists or img to run ocr on
            else:
                return '*' * 10

    def get_all_meme_text(self, subredditUrl, user, key):
        _json = self.rp.get_reddit_json(subredditUrl, user)
        while 'data' not in _json:
            time.sleep(4)
            _json = RedditParser.get_reddit_json(subredditUrl, user)

        gen = self.rp.get_parsed_reddit_json(_json, key)
        divider = '-' * 50
        print(divider)
        for i, urlKey in enumerate(gen):
            print(f'{i:02}')
            print(f'{urlKey}')
            print(self.get_meme_text(urlKey))
            print('')
            print(divider)


if __name__ == '__main__':
    import os

    subredditUrl = 'https://www.reddit.com/r/AdviceAnimals/top/'
    subredditUrl += '.json?sort=top&t=week'
    # subredditUrl = 'https://www.reddit.com/domain/memegen.com/.json'
    user = 'craptionb0t'
    key = 'url'

    lang = 'joh'
    tessDir = os.path.dirname(os.path.realpath(__file__))
    tessDir += 'tessdata'

    b = Bot(lang, tessDir)
    b.get_all_meme_text(subredditUrl, user, key)
