#!/usr/bin/env python
import requests
import pytesseract
from io import BytesIO
from PIL import Image
from PIL import ImageOps
# from textblob import TextBlob


class ImageToText(object):
    '''
    Gets text from images
    '''

    def get_image(self, url):
        '''
        url: url of image
        returns image object of url
        '''
        return Image.open(BytesIO(requests.get(url).content))

    def get_top_of_text(self, image, limit=250):
        '''
        image: image object
        limit: threshold to scan for
        returns top most pixel of image >= limit
        '''
        width, height = image.size
        top = height
        pixel_map = image.load()
        for x in range(width):
            for y in range(height):
                if pixel_map[x, y] >= limit and y < top:
                    top = y
        return top

    def get_bottom_of_text(self, image, limit=250):
        '''
        image: image object
        limit: threshold to scan for
        returns bottom most pixel of image >= limit
        '''
        width, height = image.size
        bottom = 0
        pixel_map = image.load()
        for x in range(width):
            for y in range(height):
                if pixel_map[x, y] >= limit and y > bottom:
                    bottom = y
        return bottom

    def get_left_of_text(self, image, limit=250):
        '''
        image: image object
        limit: threshold to scan for
        returns left most pixel of image >= limit
        '''
        width, height = image.size
        left = width
        pixel_map = image.load()
        for x in range(width):
            for y in range(height):
                if pixel_map[x, y] >= limit and x < left:
                    left = x
        return left

    def get_right_of_text(self, image, limit=250):
        '''
        image: image object
        limit: threshold to scan for
        returns right most pixel of image >= limit
        '''
        width, height = image.size
        right = 0
        pixel_map = image.load()
        for x in range(width):
            for y in range(height):
                if pixel_map[x, y] >= limit and x > right:
                    right = x
        return right

    def get_coordinates(self, url):
        '''
        url: url of image
        assumes text of image is in top and bottom quarter
        returns two tuples surrounding the top and bottom text of image
        '''
        # get image, greyscale, make text black
        image = self.get_image(url)
        image = ImageOps.grayscale(image)
        image = ImageOps.invert(image)

        width, height = image.size
        middle_of_width = width // 2
        quarter_of_width = width // 4
        quarter_of_height = height // 4
        bottom_quarter_y = height - quarter_of_height
        bottom_quarter_lx = middle_of_width - quarter_of_width
        bottom_quarter_rx = middle_of_width + quarter_of_width

        top_left = image.crop((0, 0, middle_of_width, quarter_of_height))
        top_right = image.crop((middle_of_width, 0, width, quarter_of_height))

        # Skip watermarks
        bottom_center = image.crop((bottom_quarter_lx, bottom_quarter_y,
                                   bottom_quarter_rx, height))
        bottom_bottom_pixel = (bottom_quarter_y
                               + self.get_bottom_of_text(bottom_center))

        bottom_left = image.crop((0, bottom_quarter_y, middle_of_width,
                                 bottom_bottom_pixel))
        bottom_right = image.crop((middle_of_width, bottom_quarter_y, width,
                                  bottom_bottom_pixel))

        top_left_pixel = self.get_left_of_text(top_left)
        top_right_pixel = middle_of_width + self.get_right_of_text(top_right)
        top_top_pixel = min(self.get_top_of_text(top_left),
                            self.get_top_of_text(top_right))
        top_bottom_pixel = max(self.get_bottom_of_text(top_left),
                               self.get_bottom_of_text(top_right))

        bottom_left_pixel = self.get_left_of_text(bottom_left)
        bottom_right_pixel = (middle_of_width
                              + self.get_right_of_text(bottom_right))
        bottom_top_pixel = (bottom_quarter_y
                            + min(self.get_top_of_text(bottom_left),
                                  self.get_top_of_text(bottom_right)))

        padding = 10
        if top_left_pixel - padding > 0:
            top_left_pixel -= padding
        if top_right_pixel + padding < width:
            top_right_pixel += padding
        if top_top_pixel - padding > 0:
            top_top_pixel -= padding
        else:
            top_top_pixel = 0
        if top_bottom_pixel + padding < height:
            top_bottom_pixel += padding
        if bottom_left_pixel - padding > 0:
            bottom_left_pixel -= padding
        if bottom_right_pixel + padding < width:
            bottom_right_pixel += padding
        if bottom_top_pixel - padding > 0:
            bottom_top_pixel -= padding
        if bottom_bottom_pixel + padding < height:
            bottom_bottom_pixel += padding

        top_box = (top_left_pixel,
                   top_top_pixel,
                   top_right_pixel,
                   top_bottom_pixel)

        bottom_box = (bottom_left_pixel,
                      bottom_top_pixel,
                      bottom_right_pixel,
                      bottom_bottom_pixel)

        return [top_box, bottom_box]

    def split_image(self, url):
        '''
        url: url of image
        assumes text of image is in top and bottom quarter
        returns top and bottom image objects containing the text
        '''
        image = self.get_image(url)
        top_coordinates, bottom_coordinates = self.get_coordinates(url)

        top = image.crop(top_coordinates)
        bottom = image.crop(bottom_coordinates)
        # top.save('top.png')
        # bottom.save('bottom.png')

        return top, bottom

    def process_image(self, image, lang=None, tess_dir=None):
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

        if type(lang) is str and type(tess_dir) is str:
            tess_dir = '--tessdata-dir "{}"'.format(tess_dir)
            result = pytesseract.image_to_string(image, lang=lang,
                                                 config=tess_dir)
        elif type(lang) is str and type(tess_dir) is None:
            result = pytesseract.image_to_string(image, lang=lang)
        elif type(lang) is None and type(tess_dir) is str:
            result = pytesseract.image_to_string(image, config=tess_dir)
        else:
            result = pytesseract.image_to_string(image)
        return result

    def print(self, url, lang=None, tess_dir=None):
        '''
        url: url of image
        lang: tesseract language
        tessDir: tesseract config dir
        prints text of image through top/bottom split and through full image
        commented out autocorrect prints
        '''
        print('-' * 40)
        i = ImageToText()
        top, bottom = i.split_image(url)
        top_text = i.process_image(top, lang, tess_dir)
        bottom_text = i.process_image(bottom, lang, tess_dir)
        top_text = top_text.replace('\r', '').replace('\n', '')
        bottom_text = bottom_text.replace('\r', '').replace('\n', '')
        print(top_text)
        print(bottom_text)
        print('-' * 40)
        # print(TextBlob(top_text).correct())
        # print(TextBlob(bottom_text).correct())
        # print('-' * 40)
        full = i.get_image(url)
        # full.save('full.png')
        text = i.process_image(i.get_image(url), lang, tess_dir)
        text = text.replace('\r', '').replace('\n', '')
        print(text)
        print('-' * 40)
        # print(TextBlob(text).correct())
        # print('-' * 40)
        # print(spell(text))


def main(imageToText, url, lang=None, tess_dir=None):
    '''
    url: url of image
    lang: tesseract language
    tessDir: tesseract config dir
    prints text of image for debugging
    '''
    imageToText.print(url, lang, tess_dir)


if __name__ == '__main__':
    import os

    lang = 'joh'
    tess_dir = os.path.dirname(os.path.realpath(__file__))
    tess_dir += 'tessdata'
    # url = 'https://b.thumbs.redditmedia.com/'
    # url += '70S2ljgfXlUd0wzZmP8kL92Rlp4mI5TzVfuwDREq-8A.jpg'
    # url = 'https://i.imgur.com/Kr6Gz5Q.jpg'
    # url = 'https://i.redd.it/rwu3smidtv3z.jpg'
    url = 'http://i.imgur.com/QrCwD5n.jpg'
    main(ImageToText(), url, lang, tess_dir)
