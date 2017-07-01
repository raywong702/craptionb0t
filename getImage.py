#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup
from imageExtensions import imageExtensions


class getImage(object):
    def __init__(self):
        self.EXTENSIONS = imageExtensions().EXTENSIONS

    ########################################
    # imgflip
    def imgFlipDirectUrl(self, url):
        if 'i.imgflip' in url:
            return True
        return False

    def imgFlipUrlTransform(self, url):
        if self.imgFlipDirectUrl(url):
            prefix = url[:url.index('i')]
            suffix = url[url.rindex('/'):url.rindex('.')]
            return prefix + 'imgflip.com/i' + suffix
        else:
            return url

    def getImgFlip(self, url):
        page = requests.get(url).text
        soup = BeautifulSoup(page, 'lxml')
        img = soup.find('img', {'id': 'im'})
        # index 0 is meme
        # index 1 is text
        meme = img.attrs['alt'].split('|')
        return (meme[0].strip(), meme[1].strip())

    ########################################
    # makeameme
    def makeAMemeDirectUrl(self, url):
        if 'media.makeameme' in url:
            return True
        return False

    def makeAMemeTransform(self, url):
        if self.makeAMemeDirectUrl(url):
            prefix = url[:url.index('media')]
            suffix = url[url.rindex('/'):url.rindex('.')]
            return prefix + 'makeameme.org/meme' + suffix
        else:
            return url

    def getMakeAMeme(self, url):
        page = requests.get(url).text
        soup = BeautifulSoup(page, 'lxml')
        div = soup.findAll('div', {'class': 'small-12 text-center'})
        meme = []
        for text in div[len(div)-1].text.split('\n'):
            if len(text) > 0 and 'add your own captions' not in text:
                meme.append(text.strip())
        # index 0 is meme
        # index 1 is text
        return meme

    ########################################
    # livememe
    def liveMemeDirectUrl(self, url):
        if 'lvme.me' in url or any(ext in url for ext in self.EXTENSIONS):
            return True
        return False

    def liveMemeTransform(self, url):
        if self.liveMemeDirectUrl(url):
            suffix = url[url.rindex('/'):url.rindex('.')]
            return 'http://www.livememe.com' + suffix
        else:
            return url

    def getLiveMeme(self, url):
        page = requests.get(url).text
        soup = BeautifulSoup(page, 'lxml')
        style1 = 'word-wrap: break-word; font-weight: bold;'
        style2 = 'word-wrap: break-word; margin-top: 11px;'
        text = []
        try:
            memeType = soup.findAll('div', {'style': style1})[0].text.strip()
        except IndexError:
            memeType = None
        memeText = soup.findAll('div', {'style': style2})
        for i in memeText:
            text.append(i.text.upper().strip())
        # index 0 is meme
        # index 1 is text
        return (memeType, text)

    ########################################
    # memecaptain
    def memeCaptainDirectUrl(self, url):
        if any(ext in url for ext in self.EXTENSIONS):
            return True
        return False

    def memeCaptainTransform(self, url):
        if self.liveMemeDirectUrl(url):
            suffix = url[url.rindex('/'):url.rindex('.')]
            return 'https://memecaptain.com/gend_image_pages' + suffix
        else:
            return url

    def getMemeCaptain(self, url):
        page = requests.get(url).text
        soup = BeautifulSoup(page, 'lxml')
        text = []
        try:
            memeType = soup.findAll('small')[0].text.strip()
        except IndexError:
            memeType = None
        memeText = soup.findAll('h1')
        for i in memeText:
            text.append(i.text.upper().strip())
        return (memeType, text)

    ########################################
    # memegen
    def memeGenDirectUrl(self, url):
        if any(ext in url for ext in self.EXTENSIONS):
            return True
        return False

    def memeGenTransform(self, url):
        if self.liveMemeDirectUrl(url):
            suffix = url[url.rindex('/'):url.rindex('.')]
            return 'http://memegen.com/meme' + suffix
        else:
            return url

    def getMemeGen(self, url):
        page = requests.get(url).text
        soup = BeautifulSoup(page, 'lxml')
        img = soup.find('img', {'class': 'img-polaroid'})
        meme = img.attrs['alt']
        try:
            memeType = meme[:meme.index(':')].strip()
        except:
            memeType = None
        try:
            text = meme[meme.index(':')+1:meme.rindex('-')].strip()
        except:
            text = None
        return (memeType, text)

    ########################################
    # imgur
    def getImgur(self, url):
        page = requests.get(url).text
        soup = BeautifulSoup(page, 'lxml')
        img = soup.find('link', {'rel': 'image_src'}).attrs['href']
        return img

    # makeameme.org
    # media.makeameme.org
    # livememe.com
    # memecaptain.com
    # i.memecaptain.com
    # memegen.com
    # m.memegen.com


if __name__ == '__main__':
    gi = getImage()
    # url = 'https://imgflip.com/i/1r4za5'
    # print(gi.getImgFlip(url))
    # url = 'https://media.makeameme.org/created/you-know-what-594eef.jpg'
    # url = gi.makeAMemeTransform(url)
    # print(gi.getMakeAMeme(url))
    # url = 'http://e.lvme.me/kh3mgv5.jpg'
    # url = 'http://www.livememe.com/g6m9iap'
    # url = gi.liveMemeTransform(url)
    # print(gi.getLiveMeme(url))
    # url = 'https://i.memecaptain.com/gend_images/11iK0Q.gif'
    # url = gi.memeCaptainTransform(url)
    # print(url)
    # print(gi.getMemeCaptain(url))
    url = 'http://m.memegen.com/xsu560.jpg'
    url = gi.memeGenTransform(url)
    print(url)
    print(gi.getMemeGen(url))
