'''
Rotten Tomatoes Scraper for Project Big Screen

Functions available from util.py:
    - get_request(url)
    - read_request(request)
    - get_request_url(request)
    - convert_if_relative_url(current_url, new_url)
'''

import re
import util
import bs4
import queue
import json
import sys
import csv
import sqlite3
import urllib.request

def get_movie_links():
    '''
    Gets all movie links, short synopsis, runtime, three main actors, and id
    '''
    movie_dict = {}

    start_url = ('https://www.rottentomatoes.com/api/private/v2.0/browse?'
                 'maxTomato=100&maxPopcorn=100&services=amazon;hbo_go;itunes;'
                 'netflix_iw;vudu;amazon_prime;fandango_now&certified&sortBy='
                 'release&type=dvd-streaming-all&page=')

    for i in range(1, 312):
        r = util.get_request(start_url + str(i))
        result = r.json()

        for movie in result.get('results'):
            new_movie = {}

            print(i, movie.get('title'))
            movie_id = movie.get('id')

            new_movie['actors'] = movie.get('actors')
            new_movie['h_runtime'] = movie.get('runtime')
            new_movie['short_synopsis'] = movie.get('synopsis')
            new_movie['title'] = movie.get('title')
            new_movie['relative_url'] = movie.get('url')

            movie_dict[movie_id] = new_movie

    return movie_dict

def all_movies_page_csv(index_filename):
    movie_dict = get_movie_links()

    with open(index_filename, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter = '|')

        for movie_id, movie in movie_dict.items():
            writer.writerow([movie_id, '/'.join(movie.get('actors')), 
                             movie.get('h_runtime'), movie.get('short_synopsis'),
                             movie.get('title'), movie.get('relative_url')])

def movie_level_data():
    s = 'SELECT title, movie_id, url FROM all_movies_page'
    db = sqlite3.connect('sql_db_files/rotten_tomatoes.db')
    
    c = db.cursor()
    r = c.execute(s)

    urls = r.fetchall()

    db.close()

    movie_level_dict = {}

    current_url= 'https://www.rottentomatoes.com/'
    
    i = 1 # For keeping track of movie out of 9500-ish
    for title, movie_id, url in urls:
        url = util.convert_if_relative_url(current_url, url)
        
        print(i, title, movie_id)
        i += 1

        r = urllib.request.urlopen(url)
        html = r.read()
        soup = bs4.BeautifulSoup(html, features = 'html5lib')

        movie_level_dict[movie_id] = data_collector(soup)

    return movie_level_dict

def movie_level_csv(index_filename):
    movie_dict = movie_level_data()

    with open(index_filename, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter = '|')

        for movie_id, movie in movie_dict.items():
            writer.writerow([movie_id, 
                             movie.get('Directed by:'),
                             movie.get('Genre:'),
                             movie.get('In Theaters:'),
                             movie.get('On Disc/Streaming:'),
                             movie.get('Rating:'),
                             movie.get('Runtime:'),
                             movie.get('Studio:'),
                             movie.get('Written By:'),
                             movie.get('full_synop')])

def data_collector(soup):
    movie_info = {}

    movie_info['full_synop'] = soup.find_all('div', 
        class_ = "movie_synopsis")[0].text.strip()

    tags = soup.find_all('li', class_ = 'meta-row clearfix')
    for tag in tags:
        divs = tag.find_all('div')
        label = divs[0].text.strip()
        value = divs[1]
        links = value.find_all('a')
        
        if links:
            s = ''
            n = len(links)
            for i, link in enumerate(links):
                s += link.text + (', ' if i < n - 1 else '')

        else:
            s = value.text

        movie_info[label] = s.strip()

    return movie_info





