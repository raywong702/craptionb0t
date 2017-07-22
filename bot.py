#!/usr/bin/env python
import praw
from get_text import GetText


class Bot(object):
    def __init__(self, lang, tess_dir):
        self.reddit = praw.Reddit('bot0')
        self.gt = GetText(lang, tess_dir)

    def get_all_meme_text(self, subreddit):
        _subreddit = self.reddit.subreddit(subreddit)
        divider = '-' * 50
        print(divider)
        for i, submission in enumerate(_subreddit.top('week', limit=25)):
            print(f'{i:02}')
            print(f'{submission.url}')
            print(self.gt.get_meme_text(submission.url))
            print('')
            print(divider)


if __name__ == '__main__':
    import os

    subreddit = 'adviceanimals'

    lang = 'joh'
    tess_dir = os.path.dirname(os.path.realpath(__file__))
    tess_dir += 'tessdata'

    b = Bot(lang, tess_dir)
    b.get_all_meme_text(subreddit)
