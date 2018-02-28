#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import sys  
import re
import urllib2
import json
import requests
from bs4 import BeautifulSoup

import tokenize

SEARCHINFO_FILE = './searchinfo.json'

def getSearchinfoByKey(key=''):
    with open(SEARCHINFO_FILE, 'r') as f:
        searchinfo = json.loads(f.read())
        return searchinfo.get(key)

def getValidGenres():
    return getSearchinfoByKey(key='validGenres')

def getInvalidGenres():
    return getSearchinfoByKey(key='invalidGenres')

def validatePageGenres(pageMetas):
    genreMeta = [ meta.get('content') for meta in pageMetas if 'genres' in meta.get('content')]
    genres = set()
    for c in genreMeta:
        match = re.search('genres.*?\[(.*?)\]', c)
        if match is None: continue

        genreList = match.group(1).replace('"', '').split(',')
        for genre in genreList: genres.add(genre)

    for invalid in getInvalidGenres():
        for genre in genres:
            if invalid.lower() in genre.lower():
                return False

    for valid in getValidGenres():
        for genre in genres:
            if valid.lower() in genre.lower():
                return True

    return False

def validateLyricLang(pageMetas):
    langContent = [ meta.get('content') for meta in pageMetas if 'Lyrics Language' in meta.get('content')]

    if not len(langContent):
        return False

    match = re.search(r'Lyrics Language.*?value":"([A-Za-z]+?)"', langContent[0])

    if match is None:
        return False

    return match.group(1) == 'en' # Only accepts lyrics in english


def getSongLyrics(url):
    # Skip urls that doesn't lead to genius-lyric-pages
    if not url.endswith('-lyrics'):
        return None

    print '\nFetching lyrics from url:', url
    page = requests.get(url)
    html = BeautifulSoup(page.content, 'html.parser')
    
    pageMetas = html.findAll("meta")
    if not validatePageGenres(pageMetas):
        return None
    if not validateLyricLang(pageMetas):
        return None

    #remove script tags that they put in the middle of the lyrics
    [h.extract() for h in html('script')]
    #at least Genius is nice and has a tag called 'lyrics'!
    return html.find('div', attrs={'class': 'lyrics'}).get_text()

def parseSongLyrics(lyricsString):
    # lyricParts = {
    #     'intro': [],
    #     'verses': [],
    #     'hooks': [],
    #     'choruses': [],
    #     'outro': []
    # }


    lyricParts = {}
    songPartTitles = [ 'intro', 'verse', 'hooks', 'chorus', 'outro' ]
    
    parts = lyricsString.split('[')
    for part in parts:
        if not part: continue   
        
        try: 
            partTitle, partLyrics = part.split(']')
        except: continue

        partTitle = partTitle.lower()
        partLyrics = partLyrics.replace('\n', ' ').strip()

        for title in songPartTitles:
            if title in partTitle:
                if not lyricParts.get(title): lyricParts[title] = []
                tokenized = tokenize.tokenizeString(string=partLyrics)
                if not tokenized: continue
                lyricParts[title].append(tokenized)
                # lyricParts[title].append(partLyrics.split()) # basic tokenizer, splits on whitespace

    return lyricParts


def extendSongDataWithLyrics(songData):
    extended = []

    for song in songData:
        if not song.get('url'): continue
        lyrics = getSongLyrics(song['url'])

        if not lyrics: continue

        # TODO: here post-process lyrics with function that divides songs parts into object
        lyrics = parseSongLyrics(lyrics)
        if not len(lyrics.keys()): continue

        extendedSong = song.copy()
        extendedSong['lyrics'] = lyrics
        extended.append(extendedSong)

    return extended

def loadCredentials():
    credentials = getSearchinfoByKey(key='credentials')
    return credentials['client_id'], credentials['client_secret'], credentials['client_access_token']

    
def search(search_term, client_access_token, pageLimit=30):
    #Unfortunately, looks like it maxes out at 50 pages (approximately 1,000 results), roughly the same number of results as displayed on web front end
    page=1
    songData = []
    while True:
        querystring = "http://api.genius.com/search?q=" + urllib2.quote(search_term) + "&page=" + str(page)
        request = urllib2.Request(querystring)
        request.add_header("Authorization", "Bearer " + client_access_token)   
        request.add_header("User-Agent", "curl/7.9.8 (i686-pc-linux-gnu) libcurl 7.9.8 (OpenSSL 0.9.6b) (ipv6 enabled)") #Must include user agent of some sort, otherwise 403 returned
        while True:
            try:
                response = urllib2.urlopen(request, timeout=4) #timeout set to 4 seconds; automatically retries if times out
                raw = response.read()
            except Exception as e:
                print("Timeout raised and caught")
                continue
            break
        json_obj = json.loads(raw)
        body = json_obj["response"]["hits"]

        num_hits = len(body)
        if num_hits==0:
            if page==1:
                print("No results for: " + search_term)
            break      
        print("page {0}; num hits {1}".format(page, num_hits))

        for result in body:
            result_id = result["result"]["id"]
            title = result["result"]["title"]
            url = result["result"]["url"]
            primaryartist_name = result["result"]["primary_artist"]["name"]
            songData.append(dict(id=result_id, title=title, url=url, artist=primaryartist_name))

        if page == pageLimit: break
        page+=1

    print [ song.get('artist') for song in songData ]
    print 
    return songData

def main():
    arguments = sys.argv[1:] #so you can input searches from command line if you want
    search_term = arguments[0].translate(None, "\'\"")
    client_id, client_secret, client_access_token = loadCredentials()
    songData = search(search_term, client_access_token)
    songData = extendSongDataWithLyrics(songData)

    with open('./output.json', 'w') as f:
        f.write(json.dumps(songData, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
