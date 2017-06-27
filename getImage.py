#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup


class getImage(object):
    def imgflipDirectUrl(self, imgflipUrl):
        if 'i.imgflip' in imgflipUrl:
            return True
        return False

    def imgflipUrlTransform(self, imgflipUrl):
        if self.imgflipDirectUrl(imgflipUrl):
            prefix = imgflipUrl[:imgflipUrl.index('i')]
            suffix = imgflipUrl[imgflipUrl.rindex('/'):imgflipUrl.rindex('.')]
            return prefix + 'imgflip.com/i' + suffix
        else:
            return imgflipUrl

    def getImgFlip(self, url):
        page = requests.get(url).text
        soup = BeautifulSoup(page, 'lxml')
        img = soup.find('img', {'id': 'im'})
        # index 0 is meme
        # index 1 is text
        return img.attrs['alt'].split('|')

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
    url = 'https://imgflip.com/i/1r4za5'
    gi = getImage()
    print(gi.getImgFlip(url))
