#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import sys  
import re
import urllib2
import json
import requests
from bs4 import BeautifulSoup

def getValidGenres():
    with open('./validgenres.json', 'r') as f:
        return json.loads(f.read())

def getSongLyrics(url):
    print
    print 'Fetching lyrics from url:', url
    page = requests.get(url)
    html = BeautifulSoup(page.content, 'html.parser')
    #remove script tags that they put in the middle of the lyrics
    genre = ""
    metas= html.findAll("meta")


    content = [ meta.get('content') for meta in metas if 'genres' in meta.get('content')]
    genres = set()
    for c in content:
        m = re.search('genres.*?\[(.*?)\]', c)
        genreList = m.group(1).replace('"', '').split(',')
        for genre in genreList: genres.add(genre)

    print 'GENRE:', genres

    validGenres = getValidGenres()
    print 'validgenres:', validGenres


    [h.extract() for h in html('script')]
    #at least Genius is nice and has a tag called 'lyrics'!
    lyrics = html.find('div', attrs={'class': 'lyrics'}).get_text()


    return lyrics

def extendSongDataWithLyrics(songData):
    extended = []

    for song in songData:
        if not song.get('url'): continue
        lyrics = getSongLyrics(song['url'])


    return extended

def loadCredentials(): # TODO: change file format to json
    lines = [line.rstrip('\n') for line in open('credentials.ini')]
    chars_to_strip = " \'\""
    for line in lines:
        if "client_id" in line:
            client_id = re.findall(r'[\"\']([^\"\']*)[\"\']', line)[0]
        if "client_secret" in line:
            client_secret = re.findall(r'[\"\']([^\"\']*)[\"\']', line)[0]
        #Currently only need access token to run, the other two perhaps for future implementation
        if "client_access_token" in line:
            client_access_token = re.findall(r'[\"\']([^\"\']*)[\"\']', line)[0]
    return client_id, client_secret, client_access_token
    
def search(search_term, client_access_token, pageLimit=1):
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
            # except socket.timeout:
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

        print [ song.get('artist') for song in songData ]
        print 

        if page == pageLimit: break
        page+=1

    return songData

def main():
    arguments = sys.argv[1:] #so you can input searches from command line if you want
    search_term = arguments[0].translate(None, "\'\"")
    client_id, client_secret, client_access_token = loadCredentials()
    songData = search(search_term,client_access_token)
    songData = extendSongDataWithLyrics(songData)

if __name__ == '__main__':
    main()
