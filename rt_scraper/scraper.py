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

def get_movie_links(start = 1):
    '''
    Gets all movie links, short synopsis, runtime, three main actors, and id
    '''
    movie_dict = {}

    start_url = ("https://www.rottentomatoes.com/api/private/v2.0/browse?"
                 "maxTomato=100&maxPopcorn=100&services=amazon;hbo_go;itunes;"
                 "netflix_iw;vudu;amazon_prime;fandango_now&certified&sortBy="
                 "release&type=dvd-streaming-all&page=")

    for i in range(start, 312):
        r = util.get_request(start_url + str(i))
        result = r.json()

        for movie in result.get("results"):
            new_movie = {}

            print(i, movie.get("title"))
            movie_id = movie.get("id")

            new_movie["actors"] = movie.get("actors")
            new_movie["runtime_h"] = movie.get("runtime")
            new_movie["short_synopsis"] = movie.get("synopsis")
            new_movie["title"] = movie.get("title")
            new_movie["relative_url"] = movie.get('url')

            movie_dict[movie_id] = new_movie

    return movie_dict

def all_movies_page_csv(start = 1, index_filename):
    with open

def go(num_pages_to_crawl, index_filename):
    pass