#!/usr/bin/env python
import time
import praw
from get_text import GetText


class Bot(object):
    ''' Reddit bot to post meme text
    '''

    def __init__(self, bot_name, lang, tess_dir):
        ''' bot_name: config to use from praw.ini
        lang: language for tesseract
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
        comment_limit: The ammount of replace_more in comments
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
        prints index, submission shortlink, submission url, meme type and  text
        '''
        divider = '-' * 50
        now = time.strftime("%Y/%m/%d %H:%M:%S")
        print(divider)
        print('')
        print(f'{index:02}')
        print(now)
        print(f'{submission.shortlink}')
        print(f'{submission.url}')
        print(meme_type)
        print(text)
        print('')

    def get_text(self, index, submission):
        ''' index: index of enumeration
        submission: submission
        pretty prints submissions
        returns (text, meme_type)
        '''
        text, meme_type = self.gt.get_meme_text(submission.url)
        self.pretty_print(index, submission, text, meme_type)
        return (text, meme_type)

    def get_text_once(self, subreddit, filter_type, time_filter=all,
                      limit=25):
        ''' subreddit: subreddit
        filter_type: hot, new, rising, controversial, top
        time_filter: all, day, hour, month, week, year (default: all)
        limit: positive int or None (default: 25)
        print subreddit's meme text
        '''
        submissions = self.get_submissions(subreddit, filter_type,
                                           time_filter, limit)

        for i, submission in enumerate(submissions):
            self.get_text(i, submission)

    def get_text_stream(self, subreddit):
        ''' subreddit: subreddit
        print subreddit's meme text as new submissions come in
        '''
        _subreddit = self.reddit.subreddit(subreddit)

        for i, submission in enumerate(_subreddit.stream.submissions()):
            self.get_text(i, submission)

    def post_text(self, index, submission, comment_limit=None):
        ''' index: index of enumeration
        submission: submission
        pretty prints text if not commented on already
        pretty prints already commented if commented on already
        returns True if posted comment
        returns False if already commented
        '''
        if not self.has_commented(submission, comment_limit):
            text, meme_type = self.get_text(index, submission)
            if text is not None:
                if meme_type is not None:
                    _post_text = f'**{meme_type}**\n\n>{text}\n\n'
                    _post_text += f'{self.DISCLAIMER}'
                else:
                    _post_text = f'>{text}\n\n{self.DISCLAIMER}'
                try:
                    submission.reply(_post_text)
                except praw.exceptions.APIException as e:
                    print('-' * 50)
                    print(e)
                    print('-' * 50)
                    print(dir(e))
                    print('-' * 50)
                    print(vars(e))
                    print('-' * 50)
                    time.sleep(600)
                    submission.reply(_post_text)
                return True
        comment_block = '#' * 5
        text = f'{comment_block} Already commented {comment_block}'
        self.pretty_print(index, submission, text, text)
        return False

    def post_text_once(self, subreddit, filter_type, time_filter=all, limit=25,
                       comment_limit=None):
        ''' subreddit: subreddit
        filter_type: hot, new, rising, controversial, top
        time_filter: all, day, hour, month, week, year (default: all)
        limit: positive int or None (default: 25)
        comment_limit: The ammount of replace_more in comments (default: None)
        pretty prints text if not commented on already
        pretty prints already commented if commented on already
        post text to submissions if not commented on already
        '''
        submissions = self.get_submissions(subreddit, filter_type,
                                           time_filter, limit)

        for i, submission in enumerate(submissions):
            self.post_text(i, submission, comment_limit)

    def post_text_stream(self, subreddit, comment_limit=None):
        ''' subreddit: subreddit
        comment_limit: The ammount of replace_more in comments (default: None)
        note: takes about 5 upvotes for rate limit to disipate
        '''
        _subreddit = self.reddit.subreddit(subreddit)

        for i, submission in enumerate(_subreddit.stream.submissions()):
            self.post_text(i, submission, comment_limit)


if __name__ == '__main__':
    import os

    subreddit = 'adviceanimals'
    filter_type = 'rising'
    filter_type = 'top'
    time_filter = 'day'
    time_filter = 'hour'
    limit = 25
    comment_limit = None

    bot_name = 'bot0'
    lang = 'joh'
    tess_dir = os.path.dirname(os.path.realpath(__file__))
    tess_dir += 'tessdata'

    b = Bot(bot_name, lang, tess_dir)
    # b.get_text_once(subreddit, filter_type, time_filter, limit)
    # b.get_text_stream(subreddit)
    # b.post_text_once(subreddit, filter_type, time_filter, limit, comment_limit)
    b.post_text_stream(subreddit, comment_limit)
