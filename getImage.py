#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup


class getImage(object):
    def getImgFlip(self, url):
        page = requests.get(url).text
        soup = BeautifulSoup(page, 'lxml')
        img = soup.find('img', {'id': 'im'})
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
