#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup
from ocr import OCR


class GetText(object):
    def __init__(self, lang, tess_dir):
        self._ocr = OCR()
        self.lang = lang
        self.tess_dir = tess_dir
        self.EXTENSIONS = ('.jpg',
                           '.png',
                           '.gif'
                           )

    def strip_text(self, text):
        return text.replace('\r', '').replace('\n', '')

    def process_image(self, img):
        text = self._ocr.process_image(self._ocr.get_image(img), self.lang,
                                       self.tess_dir)
        return self.strip_text(text)

    ########################################
    # imgflip
    def is_imgflip_direct_url(self, url):
        if 'i.imgflip' in url:
            return True
        return False

    def transform_imgflip_url(self, url):
        if self.is_imgflip_direct_url(url):
            prefix = url[:url.index('i')]
            suffix = url[url.rindex('/'):url.rindex('.')]
            return prefix + 'imgflip.com/i' + suffix
        else:
            return url

    def get_imgflip(self, url):
        page = requests.get(url).text
        soup = BeautifulSoup(page, 'lxml')
        img = soup.find('img', {'id': 'im'})
        # index 0 is meme
        # index 1 is text
        meme = img.attrs['alt'].split('|')
        return (meme[0].strip(), meme[1].strip())

    ########################################
    # makeameme
    def is_makeameme_direct_url(self, url):
        if 'media.makeameme' in url:
            return True
        return False

    def transform_makeameme_url(self, url):
        if self.is_makeameme_direct_url(url):
            prefix = url[:url.index('media')]
            suffix = url[url.rindex('/'):url.rindex('.')]
            return prefix + 'makeameme.org/meme' + suffix
        else:
            return url

    def get_makeameme(self, url):
        page = requests.get(url).text
        soup = BeautifulSoup(page, 'lxml')
        div = soup.findAll('div', {'class': 'small-12 text-center'})
        meme = []
        for text in div[len(div) - 1].text.split('\n'):
            if len(text) > 0 and 'add your own captions' not in text:
                meme.append(text.strip())
        # index 0 is meme
        # index 1 is text
        return meme

    ########################################
    # livememe
    def is_livememe_direct_url(self, url):
        if 'lvme.me' in url or any(ext in url for ext in self.EXTENSIONS):
            return True
        return False

    def transform_livememe_url(self, url):
        if self.is_livememe_direct_url(url):
            suffix = url[url.rindex('/'):url.rindex('.')]
            return 'http://www.livememe.com' + suffix
        else:
            return url

    def get_livememe(self, url):
        page = requests.get(url).text
        soup = BeautifulSoup(page, 'lxml')
        style1 = 'word-wrap: break-word; font-weight: bold;'
        style2 = 'word-wrap: break-word; margin-top: 11px;'
        text = []
        try:
            meme_type = soup.findAll('div', {'style': style1})[0].text.strip()
        except IndexError:
            meme_type = None
        memeText = soup.findAll('div', {'style': style2})
        for i in memeText:
            text.append(i.text.upper().strip())
        # index 0 is meme
        # index 1 is text
        return (meme_type, text)

    ########################################
    # memecaptain
    def is_memecaptain_direct_url(self, url):
        if any(ext in url for ext in self.EXTENSIONS):
            return True
        return False

    def transform_memecaptain_url(self, url):
        if self.is_livememe_direct_url(url):
            suffix = url[url.rindex('/'):url.rindex('.')]
            return 'https://memecaptain.com/gend_image_pages' + suffix
        else:
            return url

    def get_memecaptain(self, url):
        page = requests.get(url).text
        soup = BeautifulSoup(page, 'lxml')
        text = []
        try:
            meme_type = soup.findAll('small')[0].text.strip()
        except IndexError:
            meme_type = None
        memeText = soup.findAll('h1')
        for i in memeText:
            text.append(i.text.upper().strip())
        return (meme_type, text)

    ########################################
    # memegen
    def is_memegen_direct_url(self, url):
        if any(ext in url for ext in self.EXTENSIONS):
            return True
        return False

    def transform_memegen_url(self, url):
        if self.is_livememe_direct_url(url):
            suffix = url[url.rindex('/'):url.rindex('.')]
            return 'http://memegen.com/meme' + suffix
        else:
            return url

    def get_memegen(self, url):
        page = requests.get(url).text
        soup = BeautifulSoup(page, 'lxml')
        img = soup.find('img', {'class': 'img-polaroid'})
        meme = img.attrs['alt']
        try:
            meme_type = meme[:meme.index(':')].strip()
        except:
            meme_type = None
        try:
            text = meme[meme.index(':') + 1:meme.rindex('-')].strip()
        except:
            text = None
        return (meme_type, text)

    ########################################
    # imgur
    def get_imgur(self, url):
        page = requests.get(url).text
        soup = BeautifulSoup(page, 'lxml')
        img = soup.find('link', {'rel': 'image_src'}).attrs['href']
        return img

    ########################################
    def get_meme_text(self, imageUrl):
        if 'imgflip' in imageUrl:
            img_flip_url = self.transform_imgflip_url(imageUrl)
            meme_list = self.get_imgflip(img_flip_url)
            meme_type = meme_list[0]
            text = meme_list[1]
            return text
        elif 'makeameme' in imageUrl:
            makeameme_url = self.transform_makeameme_url(imageUrl)
            meme_list = self.get_makeameme(makeameme_url)
            meme_type = meme_list[0]
            text = meme_list[1]
            return text
        elif 'livememe' in imageUrl or 'lvme.me' in imageUrl:
            livememe_url = self.transform_livememe_url(imageUrl)
            meme_list = self.get_livememe(livememe_url)
            meme_type = meme_list[0]
            meme_text = meme_list[1]
            text = ''
            for i in meme_text:
                text += i.strip() + '\n'
            return text
        elif 'memecaptain' in imageUrl:
            memecaptain_url = self.transform_memecaptain_url(imageUrl)
            meme_list = self.get_memecaptain(memecaptain_url)
            meme_type = meme_list[0]
            meme_text = meme_list[1]
            text = ''
            for i in meme_text:
                text += i.strip() + '\n'
            return text
        elif 'memegen' in imageUrl:
            memegen_url = self.transform_memegen_url(imageUrl)
            meme_list = self.get_memegen(memegen_url)
            meme_type = meme_list[0]
            text = meme_list[1]
            if text is None and self.is_memegen_direct_url(imageUrl):
                text = self.process_image(imageUrl)
            return text
        # imgur webpage. get direct image and run ocr
        elif '//imgur' in imageUrl:
            img = self.get_imgur(imageUrl)
            return self.process_image(img)
        # direct image urls. primarily imgur and i.redd.it
        elif any(ext in imageUrl for ext in self.EXTENSIONS):
            return self.process_image(imageUrl)
        # website urls. need to get text if exists or img to run ocr on
        else:
            return '*' * 10
