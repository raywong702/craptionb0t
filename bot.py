#!/usr/bin/env python
import praw
from get_text import GetText


class Bot(object):
    ''' Reddit bot to post meme text
    '''
    def __init__(self, lang, tess_dir):
        ''' lang: language for tesseract
        tess_dir: tesseract training directory
        initialize a reddit and get text object
        '''
        self.reddit = praw.Reddit('bot0')
        self.gt = GetText(lang, tess_dir)

    def get_submissions(self, subreddit, filter_type,
                        time_filter=all, limit=25):
        ''' subreddit: subreddit
        filter_type: hot, new, rising, controversial, top
        time_filter: all, day, hour, month, week, year (default: all)
        limit: positive int or None (default: 25)
        return generator for subreddit
        '''
        _subreddit = self.reddit.subreddit(subreddit)
        if filter_type == 'hot':
            return _subreddit.hot(limit=limit)
        elif filter_type == 'new':
            return _subreddit.new(limit=limit)
        elif filter_type == 'rising':
            return _subreddit.rising(limit=limit)
        elif filter_type == 'controversial':
            return _subreddit.controversial(time_filter, limit=limit)
        elif filter_type == 'top':
            return _subreddit.top(time_filter, limit=limit)

    def get_all_text(self, subreddit, filter_type, time_filter=all, limit=25):
        ''' subreddit: subreddit
        filter_type: hot, new, rising, controversial, top
        time_filter: all, day, hour, month, week, year (default: all)
        limit: positive int or None (default: 25)
        print subreddit's meme text
        '''
        _subreddit = self.reddit.subreddit(subreddit)
        divider = '-' * 50
        submissions = self.get_submissions(subreddit, filter_type,
                                           time_filter, limit)
        print(divider)
        for i, submission in enumerate(submissions):
            text = self.gt.get_meme_text(submission.url)
            print(f'{i:02}')
            print(f'{submission.url}')
            print(text)
            print('')
            print(divider)

    def post_text(self, subreddit, filter_type, time_filter=all, limit=25):
        ''' subreddit: subreddit
        filter_type: hot, new, rising, controversial, top
        time_filter: all, day, hour, month, week, year (default: all)
        limit: positive int or None (default: 25)
        post text to submission
        '''
        _subreddit = self.reddit.subreddit(subreddit)
        divider = '-' * 50
        submissions = self.get_submissions(subreddit, filter_type,
                                           time_filter, limit)
        print(divider)
        for i, submission in enumerate(submissions):
            text = self.gt.get_meme_text(submission.url)
            print(f'{i:02}')
            print(f'{submission.url}')
            print(text)
            submission.reply('>' + text)
            print('')
            print(divider)


if __name__ == '__main__':
    import os

    subreddit = 'adviceanimals'
    filter_type = 'top'
    time_filter = 'week'
    limit = 25

    subreddit = 'craptionb0t_test'
    filter_type = 'hot'
    time_filter = 'all'
    limit = None

    lang = 'joh'
    tess_dir = os.path.dirname(os.path.realpath(__file__))
    tess_dir += 'tessdata'

    b = Bot(lang, tess_dir)
    b.post_text(subreddit, filter_type, time_filter, limit)
