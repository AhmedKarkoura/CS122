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

    db = sqlite3.connect('rotten_tomatoes.db')
    
    c = db.cursor()
    r = c.execute(s)

    urls = r.fetchall()

    db.close()

    movie_level_dict = {}

    current_url= 'https://www.rottentomatoes.com/'

    for title, movie_id, url in urls:
        url = util.convert_if_relative_url(current_url, url)
        
        print(title, movie_id)

        r = util.get_request('https://www.rottentomatoes.com/m/the_grinch')
        print("gotten")
        html = util.read_request(r) # THERE'S AN ISSUE HERE BUT I'M NOT SURE WHY
        print("issue passed reading")
        soup = bs4.BeautifulSoup(html, features = 'html5lib')
        print("issue passed soup")

        return soup