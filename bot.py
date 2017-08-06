#!/usr/bin/env python
import praw
from get_text import GetText


class Bot(object):
    ''' Reddit bot to post meme text
    '''

    def __init__(self, bot_name, lang, tess_dir):
        ''' lang: language for tesseract
        tess_dir: tesseract training directory
        initialize a reddit and get text object
        '''
        self.reddit = praw.Reddit(bot_name)
        self.gt = GetText(lang, tess_dir)
        self.DISCLAIMER = ("^^*These* ^^*craptions* ^^*aren't* ^^*guaranteed* "
                           "^^*to* ^^*be* ^^*correct.*")

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

    def has_commented(self, submission, comment_limit):
        ''' submission: submission
        return True if already commented on submission
        return False if has not commented on submissionyet
        '''
        username = self.reddit.config.username
        submission.comments.replace_more(limit=comment_limit)
        for top_level_comment in submission.comments:
            if top_level_comment.author == username:
                return True
        return False

    def pretty_print(self, index, submission, text, meme_type):
        ''' index: index of enumeration
        submission: submission
        meme_type: type of meme
        text: meme text
        '''
        divider = '-' * 50
        print(divider)
        print(f'{index:02}')
        print(f'{submission.shortlink}')
        print(f'{submission.url}')
        print(meme_type)
        print(text)
        print('')

    def get_text(self, subreddit, filter_type, time_filter=all, limit=25):
        ''' subreddit: subreddit
        filter_type: hot, new, rising, controversial, top
        time_filter: all, day, hour, month, week, year (default: all)
        limit: positive int or None (default: 25)
        print subreddit's meme text
        '''
        submissions = self.get_submissions(subreddit, filter_type,
                                           time_filter, limit)

        for i, submission in enumerate(submissions):
            text, meme_type = self.gt.get_meme_text(submission.url)
            self.pretty_print(i, submission, text, meme_type)

    def post_text(self, subreddit, filter_type, time_filter=all, limit=25,
                  comment_limit=None):
        ''' subreddit: subreddit
        filter_type: hot, new, rising, controversial, top
        time_filter: all, day, hour, month, week, year (default: all)
        limit: positive int or None (default: 25)
        post text to submission
        '''
        submissions = self.get_submissions(subreddit, filter_type,
                                           time_filter, limit)

        for i, submission in enumerate(submissions):
            if not self.has_commented(submission, comment_limit):
                text, meme_type = self.gt.get_meme_text(submission.url)
                if text is not None:
                    if meme_type is not None:
                        post_text = f'**{meme_type}**\n\n>{text}\n\n'
                        post_text += f'{self.DISCLAIMER}'
                    else:
                        post_text = f'>{text}\n\n{self.DISCLAIMER}'
                    submission.reply(post_text)
                    self.pretty_print(i, submission, text, meme_type)


if __name__ == '__main__':
    import os

    subreddit = 'adviceanimals'
    filter_type = 'rising'
    time_filter = 'day'

    subreddit = 'craptionb0t_test'
    filter_type = 'hot'
    time_filter = 'day'
    limit = 25
    limit = 25

    bot_name = 'bot0'
    lang = 'joh'
    tess_dir = os.path.dirname(os.path.realpath(__file__))
    tess_dir += 'tessdata'

    b = Bot(bot_name, lang, tess_dir)
    b.post_text(subreddit, filter_type, time_filter, limit)
    # b.get_text(subreddit, filter_type, time_filter, limit)
