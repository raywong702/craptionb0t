#!/usr/bin/env python
import time
import requests
from bs4 import BeautifulSoup
from image_extensions import ImageExtensions
from reddit_parser import RedditParser
from image_to_text import ImageToText
from get_image_text import GetImage


class Bot(object):
    def __init__(self, lang, tess_dir):
        self.rp = RedditParser()
        self.itt = ImageToText()
        self.gi = GetImage()
        self.lang = lang
        self.tess_dir = tess_dir
        self.EXTENSIONS = ImageExtensions().EXTENSIONS

    def strip_text(self, text):
        return text.replace('\r', '').replace('\n', '')

    def process_image(self, img):
        text = self.itt.process_image(self.itt.get_image(img), self.lang,
                                      self.tess_dir)
        return self.strip_text(text)

    def get_meme_text(self, imageUrl):
            # special case for imgflip. get text from alt attr of image
            if 'imgflip' in imageUrl:
                img_flip_url = self.gi.transform_imgflip_url(imageUrl)
                meme_list = self.gi.get_imgflip(img_flip_url)
                meme_type = meme_list[0]
                text = meme_list[1]
                return text
            # special case for makeameme. get text from body
            elif 'makeameme' in imageUrl:
                makeameme_url = self.gi.transform_makeameme_url(imageUrl)
                meme_list = self.gi.get_makeameme(makeameme_url)
                meme_type = meme_list[0]
                text = meme_list[1]
                return text
            elif 'livememe' in imageUrl or 'lvme.me' in imageUrl:
                livememe_url = self.gi.transform_livememe_url(imageUrl)
                meme_list = self.gi.get_livememe(livememe_url)
                meme_type = meme_list[0]
                meme_text = meme_list[1]
                text = ''
                for i in meme_text:
                    text += i.strip() + '\n'
                return text
            elif 'memecaptain' in imageUrl:
                memecaptain_url = self.gi.transform_memecaptain_url(imageUrl)
                meme_list = self.gi.get_memecaptain(memecaptain_url)
                meme_type = meme_list[0]
                meme_text = meme_list[1]
                text = ''
                for i in meme_text:
                    text += i.strip() + '\n'
                return text
            elif 'memegen' in imageUrl:
                memegen_url = self.gi.transform_memegen_url(imageUrl)
                meme_list = self.gi.get_memegen(memegen_url)
                meme_type = meme_list[0]
                text = meme_list[1]
                if text is None and self.gi.is_memegen_direct_url(imageUrl):
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

    subreddit_url = 'https://www.reddit.com/r/AdviceAnimals/top/'
    subreddit_url += '.json?sort=top&t=week'
    # subreddit_url = 'https://www.reddit.com/domain/memegen.com/.json'
    user = 'craptionb0t'
    key = 'url'

    lang = 'joh'
    tess_dir = os.path.dirname(os.path.realpath(__file__))
    tess_dir += 'tessdata'

    b = Bot(lang, tess_dir)
    b.get_all_meme_text(subreddit_url, user, key)
