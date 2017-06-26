#!/usr/bin/env python
import requests
import json


class redditParser(object):
    '''
    Parses Reddit
    '''

    def getRedditJson(self, url, user):
        '''
        url: Reddit json url
        i.e. https://www.reddit.com/r/AdviceAnimals/top/.json?sort=top&t=week
        returns json object from Reddit json url
        '''
        header = {}
        userAgent = 'app:python:v0.0.0 (by /u/{})'.format(user)
        header['User-agent'] = userAgent
        r = requests.get(url, headers=header)
        _json = json.loads(r.text)
        return _json

    def writeJsonFile(self, _json, f):
        '''
        _json: json object. Use getRedditJson as input
        f: json dump location
        writes Reddit json url to file
        '''
        jsonFile = open(f, 'w')
        jsonFile.write(json.dumps(_json))

    def openJsonFile(self, f):
        '''
        f: json dump file
        reads json dump file and returns json object
        '''
        with open(f) as redditJsonFile:
            _json = json.load(redditJsonFile)
        return _json

    def getParsedRedditJson(self, _json, key):
        '''
        _json: Reddit json object
        key: what you want to parse on
        Good keys to use: subreddit, permalink, author, title, url, thumbnail
        returns generator of parsed out key values
        '''
        children = _json['data']['children']
        for child in children:
            yield child['data'][key]


def main(url, user, key, outFile, jsonFile=None):
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

    output = open(outFile, 'w')
    rp = redditParser()
    if type(jsonFile) is str:
        rp.writeJsonFile(rp.getRedditJson(url, user), jsonFile)
        _json = rp.openJsonFile(jsonFile)
    else:
        _json = rp.getRedditJson(url, user)

    while 'data' not in _json:
        time.sleep(4)
        if type(jsonFile) is str:
            rp.writeJsonFile(rp.getRedditJson(url, user), jsonFile)
            _json = rp.openJsonFile(jsonFile)
        else:
            _json = rp.getRedditJson(url, user)

    rpGenerator = rp.getParsedRedditJson(_json, key)
    for i, k in enumerate(rpGenerator):
        string = "{:02}: {}".format(i, k)
        output.write("{}\n".format(string))
        print(string)
    # os.remove(jsonFile)


if __name__ == '__main__':
    url = 'https://www.reddit.com/r/AdviceAnimals/top/.json?sort=top&t=week'
    user = 'craptionb0t'
    jsonFile = 'reddit.json'
    outFile = 'thumbnails.txt'
    key = 'url'

    main(url, user, key, outFile)
    # main(url, user, key, outFile, jsonFile)
