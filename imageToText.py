#!/usr/bin/env python
import requests
import pytesseract
from io import BytesIO
from PIL import Image
from PIL import ImageOps
# from textblob import TextBlob


class imageToText(object):
    '''
    Gets text from images
    '''

    def getImage(self, url):
        '''
        url: url of image
        returns image object of url
        '''
        return Image.open(BytesIO(requests.get(url).content))

    def getTopOfText(self, image, limit=250):
        '''
        image: image object
        limit: threshold to scan for
        returns top most pixel of image >= limit
        '''
        width, height = image.size
        top = height
        pixelMap = image.load()
        for x in range(width):
            for y in range(height):
                if pixelMap[x, y] >= limit and y < top:
                    top = y
        return top

    def getBottomOfText(self, image, limit=250):
        '''
        image: image object
        limit: threshold to scan for
        returns bottom most pixel of image >= limit
        '''
        width, height = image.size
        bottom = 0
        pixelMap = image.load()
        for x in range(width):
            for y in range(height):
                if pixelMap[x, y] >= limit and y > bottom:
                    bottom = y
        return bottom

    def getLeftOfText(self, image, limit=250):
        '''
        image: image object
        limit: threshold to scan for
        returns left most pixel of image >= limit
        '''
        width, height = image.size
        left = width
        pixelMap = image.load()
        for x in range(width):
            for y in range(height):
                if pixelMap[x, y] >= limit and x < left:
                    left = x
        return left

    def getRightOfText(self, image, limit=250):
        '''
        image: image object
        limit: threshold to scan for
        returns right most pixel of image >= limit
        '''
        width, height = image.size
        right = 0
        pixelMap = image.load()
        for x in range(width):
            for y in range(height):
                if pixelMap[x, y] >= limit and x > right:
                    right = x
        return right

    def getCoordinates(self, url):
        '''
        url: url of image
        assumes text of image is in top and bottom quarter
        returns two tuples surrounding the top and bottom text of image
        '''
        # get image, greyscale, make text black
        image = self.getImage(url)
        image = ImageOps.grayscale(image)
        image = ImageOps.invert(image)

        width, height = image.size
        middleOfWidth = width // 2
        quarterOfWidth = width // 4
        quarterOfHeight = height // 4
        bottomQuarterY = height - quarterOfHeight
        bottomQuarterLX = middleOfWidth - quarterOfWidth
        bottomQuarterRX = middleOfWidth + quarterOfWidth

        topLeft = image.crop((0, 0, middleOfWidth, quarterOfHeight))
        topRight = image.crop((middleOfWidth, 0, width, quarterOfHeight))

        # Skip watermarks
        bottomCenter = image.crop((bottomQuarterLX, bottomQuarterY,
                                   bottomQuarterRX, height))
        bottomBottomPixel = (bottomQuarterY +
                             self.getBottomOfText(bottomCenter))

        bottomLeft = image.crop((0, bottomQuarterY, middleOfWidth,
                                 bottomBottomPixel))
        bottomRight = image.crop((middleOfWidth, bottomQuarterY, width,
                                  bottomBottomPixel))

        topLeftPixel = self.getLeftOfText(topLeft)
        topRightPixel = middleOfWidth + self.getRightOfText(topRight)
        topTopPixel = min(self.getTopOfText(topLeft),
                          self.getTopOfText(topRight))
        topBottomPixel = max(self.getBottomOfText(topLeft),
                             self.getBottomOfText(topRight))

        bottomLeftPixel = self.getLeftOfText(bottomLeft)
        bottomRightPixel = middleOfWidth + self.getRightOfText(bottomRight)
        bottomTopPixel = (bottomQuarterY +
                          min(self.getTopOfText(bottomLeft),
                              self.getTopOfText(bottomRight)))

        padding = 10
        if topLeftPixel - padding > 0:
            topLeftPixel -= padding
        if topRightPixel + padding < width:
            topRightPixel += padding
        if topTopPixel - padding > 0:
            topTopPixel -= padding
        else:
            topTopPixel = 0
        if topBottomPixel + padding < height:
            topBottomPixel += padding
        if bottomLeftPixel - padding > 0:
            bottomLeftPixel -= padding
        if bottomRightPixel + padding < width:
            bottomRightPixel += padding
        if bottomTopPixel - padding > 0:
            bottomTopPixel -= padding
        if bottomBottomPixel + padding < height:
            bottomBottomPixel += padding

        return [(topLeftPixel, topTopPixel, topRightPixel, topBottomPixel),
                (bottomLeftPixel, bottomTopPixel, bottomRightPixel,
                 bottomBottomPixel)]

    def splitImage(self, url):
        '''
        url: url of image
        assumes text of image is in top and bottom quarter
        returns top and bottom image objects containing the text
        '''
        image = self.getImage(url)
        topCoordinates, bottomCoordinates = self.getCoordinates(url)

        top = image.crop(topCoordinates)
        bottom = image.crop(bottomCoordinates)
        # top.save('top.png')
        # bottom.save('bottom.png')

        return top, bottom

    def processImage(self, image, lang=None, tessDir=None):
        '''
        image: image object
        returns top most pixel of image >= limit
        '''
        width, height = image.size
        top = height
        pixelMap = image.load()
        for x in range(width):
            for y in range(height):
                if pixelMap[x, y] >= limit and y < top:
                    top = y
        return top

    def getBottomOfText(self, image, limit=250):
        '''
        image: image object
        limit: threshold to scan for
        returns bottom most pixel of image >= limit
        '''
        width, height = image.size
        bottom = 0
        pixelMap = image.load()
        for x in range(width):
            for y in range(height):
                if pixelMap[x, y] >= limit and y > bottom:
                    bottom = y
        return bottom

    def getLeftOfText(self, image, limit=250):
        '''
        image: image object
        limit: threshold to scan for
        returns left most pixel of image >= limit
        '''
        width, height = image.size
        left = width
        pixelMap = image.load()
        for x in range(width):
            for y in range(height):
                if pixelMap[x, y] >= limit and x < left:
                    left = x
        return left

    def getRightOfText(self, image, limit=250):
        '''
        image: image object
        limit: threshold to scan for
        returns right most pixel of image >= limit
        '''
        width, height = image.size
        right = 0
        pixelMap = image.load()
        for x in range(width):
            for y in range(height):
                if pixelMap[x, y] >= limit and x > right:
                    right = x
        return right

    def getCoordinates(self, url):
        '''
        url: url of image
        assumes text of image is in top and bottom quarter
        returns two tuples surrounding the top and bottom text of image
        '''
        # get image, greyscale, make text black
        image = self.getImage(url)
        image = ImageOps.grayscale(image)
        image = ImageOps.invert(image)

        width, height = image.size
        middleOfWidth = width // 2
        quarterOfWidth = width // 4
        quarterOfHeight = height // 4
        bottomQuarterY = height - quarterOfHeight
        bottomQuarterLX = middleOfWidth - quarterOfWidth
        bottomQuarterRX = middleOfWidth + quarterOfWidth

        topLeft = image.crop((0, 0, middleOfWidth, quarterOfHeight))
        topRight = image.crop((middleOfWidth, 0, width, quarterOfHeight))

        # Skip watermarks
        bottomCenter = image.crop((bottomQuarterLX, bottomQuarterY,
                                   bottomQuarterRX, height))
        bottomBottomPixel = (bottomQuarterY +
                             self.getBottomOfText(bottomCenter))

        bottomLeft = image.crop((0, bottomQuarterY, middleOfWidth,
                                 bottomBottomPixel))
        bottomRight = image.crop((middleOfWidth, bottomQuarterY, width,
                                  bottomBottomPixel))

        topLeftPixel = self.getLeftOfText(topLeft)
        topRightPixel = middleOfWidth + self.getRightOfText(topRight)
        topTopPixel = min(self.getTopOfText(topLeft),
                          self.getTopOfText(topRight))
        topBottomPixel = max(self.getBottomOfText(topLeft),
                             self.getBottomOfText(topRight))

        bottomLeftPixel = self.getLeftOfText(bottomLeft)
        bottomRightPixel = middleOfWidth + self.getRightOfText(bottomRight)
        bottomTopPixel = (bottomQuarterY +
                          min(self.getTopOfText(bottomLeft),
                              self.getTopOfText(bottomRight)))

        padding = 10
        if topLeftPixel - padding > 0:
            topLeftPixel -= padding
        if topRightPixel + padding < width:
            topRightPixel += padding
        if topTopPixel - padding > 0:
            topTopPixel -= padding
        else:
            topTopPixel = 0
        if topBottomPixel + padding < height:
            topBottomPixel += padding
        if bottomLeftPixel - padding > 0:
            bottomLeftPixel -= padding
        if bottomRightPixel + padding < width:
            bottomRightPixel += padding
        if bottomTopPixel - padding > 0:
            bottomTopPixel -= padding
        if bottomBottomPixel + padding < height:
            bottomBottomPixel += padding

        return [(topLeftPixel, topTopPixel, topRightPixel, topBottomPixel),
                (bottomLeftPixel, bottomTopPixel, bottomRightPixel,
                 bottomBottomPixel)]

    def splitImage(self, url):
        '''
        url: url of image
        assumes text of image is in top and bottom quarter
        returns top and bottom image objects containing the text
        '''
        image = self.getImage(url)
        topCoordinates, bottomCoordinates = self.getCoordinates(url)

        top = image.crop(topCoordinates)
        bottom = image.crop(bottomCoordinates)
        # top.save('top.png')
        # bottom.save('bottom.png')

        return top, bottom

    def processImage(self, image, lang=None, tessDir=None):
        '''
        image: image object
        lang: tesseract language
        tessDir: tesseract config dir
        converts image to black and white
        returns text of image
        '''
        width, height = image.size
        for x in range(width):
            for y in range(height):
                pixel = image.getpixel((x, y))
                if pixel >= (240, 240, 240):
                    image.putpixel((x, y), (255, 255, 255))
                else:
                    image.putpixel((x, y), (0, 0, 0))

        if type(lang) is str and type(tessDir) is str:
            tessDir = '--tessdata-dir "{}"'.format(tessDir)
            result = pytesseract.image_to_string(image, lang=lang,
                                                 config=tessDir)
        elif type(lang) is str and type(tessDir) is None:
            result = pytesseract.image_to_string(image, lang=lang)
        elif type(lang) is None and type(tessDir) is str:
            result = pytesseract.image_to_string(image, config=tessDir)
        else:
            result = pytesseract.image_to_string(image)
        return result

    def print(self, url, lang=None, tessDir=None):
        '''
        url: url of image
        lang: tesseract language
        tessDir: tesseract config dir
        prints text of image through top/bottom split and through full image
        commented out autocorrect prints
        '''
        print('-' * 40)
        i = imageToText()
        top, bottom = i.splitImage(url)
        topText = i.processImage(top, lang, tessDir)
        bottomText = i.processImage(bottom, lang, tessDir)
        topText = topText.replace('\r', '').replace('\n', '')
        bottomText = bottomText.replace('\r', '').replace('\n', '')
        print(topText)
        print(bottomText)
        print('-' * 40)
        # print(TextBlob(topText).correct())
        # print(TextBlob(bottomText).correct())
        # print('-' * 40)
        full = i.getImage(url)
        # full.save('full.png')
        text = i.processImage(i.getImage(url), lang, tessDir)
        text = text.replace('\r', '').replace('\n', '')
        print(text)
        print('-' * 40)
        # print(TextBlob(text).correct())
        # print('-' * 40)
        # print(spell(text))


def main(imageToText, url, lang=None, tessDir=None):
    '''
    url: url of image
    lang: tesseract language
    tessDir: tesseract config dir
    prints text of image for debugging
    '''
    imageToText.print(url, lang, tessDir)


if __name__ == '__main__':
    import os

    lang = 'joh'
    tessDir = os.path.dirname(os.path.realpath(__file__))
    tessDir += 'tessdata'
    # url = 'https://b.thumbs.redditmedia.com/'
    # url += '70S2ljgfXlUd0wzZmP8kL92Rlp4mI5TzVfuwDREq-8A.jpg'
    # url = 'https://i.imgur.com/Kr6Gz5Q.jpg'
    # url = 'https://i.redd.it/rwu3smidtv3z.jpg'
    url = 'http://i.imgur.com/QrCwD5n.jpg'
    main(imageToText(), url, lang, tessDir)
