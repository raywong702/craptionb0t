#!/usr/bin/env python
import requests
import json


class RedditParser(object):
    '''
    Parses Reddit
    '''

    def get_reddit_json(self, url, user):
        '''
        url: Reddit json url
        i.e. https://www.reddit.com/r/AdviceAnimals/top/.json?sort=top&t=week
        returns json object from Reddit json url
        '''
        header = {}
        user_agent = 'app:python:v0.0.0 (by /u/{})'.format(user)
        header['User-agent'] = user_agent
        r = requests.get(url, headers=header)
        _json = json.loads(r.text)
        return _json

    def write_json_file(self, _json, f):
        '''
        _json: json object. Use getRedditJson as input
        f: json dump location
        writes Reddit json url to file
        '''
        json_file = open(f, 'w')
        json_file.write(json.dumps(_json))

    def open_json_file(self, f):
        '''
        f: json dump file
        reads json dump file and returns json object
        '''
        with open(f) as reddit_json_file:
            _json = json.load(reddit_json_file)
        return _json

    def get_parsed_reddit_json(self, _json, key):
        '''
        _json: Reddit json object
        key: what you want to parse on
        Good keys to use: subreddit, permalink, author, title, url, thumbnail
        returns generator of parsed out key values
        '''
        children = _json['data']['children']
        for child in children:
            yield child['data'][key]


def main(url, user, key, out_file, json_file=None):
    '''
    url: Reddit json url
    i.e. https://www.reddit.com/r/AdviceAnimals/top/.json?sort=top&t=week
    jsonFile: Reddit json dump if you do not want to call Reddit multiple times
    outputFile: Output of parsed key values
    key: what you want to parse on
    Good keys to use: subreddit, permalink, author, title, url, thumbnail, id,
    name
    Prints index and key values to stdout and to outFile. If jsonFile is
    passed, saves json to file
    '''
    import time
    # import os

    output = open(out_file, 'w')
    rp = RedditParser()
    if type(json_file) is str:
        rp.write_json_file(rp.get_reddit_json(url, user), json_file)
        _json = rp.open_json_file(json_file)
    else:
        _json = rp.get_reddit_json(url, user)

    while 'data' not in _json:
        time.sleep(4)
        if type(json_file) is str:
            rp.write_json_file(rp.get_reddit_json(url, user), json_file)
            _json = rp.open_json_file(json_file)
        else:
            _json = rp.get_reddit_json(url, user)

    rpGenerator = rp.get_parsed_reddit_json(_json, key)
    for i, k in enumerate(rpGenerator):
        string = "{:02}: {}".format(i, k)
        output.write("{}\n".format(string))
        print(string)
    # os.remove(jsonFile)


if __name__ == '__main__':
    url = 'https://www.reddit.com/r/AdviceAnimals/top/.json?sort=top&t=week'
    # url = 'https://www.reddit.com/r/AdviceAnimals/comments/6k5onz/'
    # url += 'think_of_the_children_you_savage/.json'
    user = 'craptionb0t'
    json_file = 'reddit.json'
    out_file = 'thumbnails.txt'
    key = 'url'

    main(url, user, key, out_file)
    # main(url, user, key, out_file, json_file)
