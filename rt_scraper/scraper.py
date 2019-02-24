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
import time

def get_movie_links():
    '''
    Gets all movie links, short synopsis, runtime, three main actors, and id
    '''
    movie_dict = {}

    start_url = ('https://www.rottentomatoes.com/api/private/v2.0/browse?'
                 'maxTomato=100&maxPopcorn=100&services=amazon;hbo_go;itunes;'
                 'netflix_iw;vudu;amazon_prime;fandango_now&certified&sortBy='
                 'release&type=dvd-streaming-all&page=')

    for i in range(312):
        r = util.get_request(start_url + str(i))
        result = r.json()

        count = result.get('counts').get('count')
        if count != 32:
            print("HEY, THIS ONE IS DIFFERENT:", count)

        for movie in result.get('results'):
            new_movie = {}

            print(i, movie.get('title'))
            movie_id = movie.get('id')

            new_movie['actors'] = movie.get('actors')
            new_movie['h_runtime'] = movie.get('runtime')
            new_movie['short_synopsis'] = movie.get('synopsis')
            new_movie['title'] = movie.get('title')
            new_movie['relative_url'] = movie.get('url')
            new_movie['poster_url'] = movie.get('posters').get('primary')

            movie_dict[movie_id] = new_movie

    return movie_dict

def all_movies_page_csv(index_filename):
    movie_dict = get_movie_links()

    with open(index_filename, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter = '|')

        for movie_id, movie in movie_dict.items():
            writer.writerow([movie_id, '/'.join(movie.get('actors')), 
                             movie.get('h_runtime'), movie.get('short_synopsis'),
                             movie.get('title'), movie.get('relative_url'),
                             movie.get('poster_url')])

def movie_level_data(index_filename, i = 0):
    s = 'SELECT title, movie_id, url FROM all_page'
    db = sqlite3.connect('sql_db_files/rotten_tomatoes.db')
    
    c = db.cursor()
    r = c.execute(s)

    urls = r.fetchall()[i:]

    db.close()

    current_url = 'https://www.rottentomatoes.com/'

    with open(index_filename + '_' + str(i), 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter = '|')
    
        for title, movie_id, url in urls:
            url = util.convert_if_relative_url(current_url, url)
        
            print(i, title, movie_id)
            i += 1

            r = url_request(index_filename, i, url)
            html = r.read()
            soup = bs4.BeautifulSoup(html, features = 'html5lib')

            movie = data_collector(soup)

            if movie.get('Runtime:'):
                movie['Runtime:'] = movie.get('Runtime:').strip('minutes ')

            if movie.get('In Theaters:'):
                movie['In Theaters:'] = re.search('[a-zA-Z]{3} [0-9,]+ [0-9]{4}', 
                    movie.get('In Theaters:')).group()

            writer.writerow([movie_id,
                             title, 
                             movie.get('Directed By:'),
                             movie.get('Genre:'),
                             movie.get('In Theaters:'),
                             movie.get('On Disc/Streaming:'),
                             movie.get('Rating:'),
                             movie.get('Runtime:'),
                             movie.get('Studio:'),
                             movie.get('Written By:'),
                             movie.get('full_synop'),
                             movie.get('all_reviewers_average'),
                             movie.get('num_reviewers'),
                             movie.get('all_fresh'),
                             movie.get('all_rotten'),
                             movie.get('top_reviewers_average'),
                             movie.get('num_top_reviewers'),
                             movie.get('top_fresh'),
                             movie.get('top_rotten'),
                             movie.get('user_rating'),
                             movie.get('num_users')])

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

    ratings = soup.find_all('div', class_ = 'superPageFontColor')

    rp = '\d(\.\d)?\/\d+'
    np = '\d+'

    if len(ratings) == 10:
        match = re.search(rp, ratings[4].text)
        if match:
            movie_info['top_reviewers_average'] = match.group()

        match = re.search(np, ratings[5].text)
        if match:
            movie_info['num_top_reviewers'] = match.group()

        match = re.search(np, ratings[6].text)
        if match:
            movie_info['top_fresh'] = match.group()

        match = re.search(np, ratings[7].text)
        if match:
            movie_info['top_rotten'] = match.group()

        match = re.search(rp, ratings[9].text)
        if match:
            movie_info['user_rating'] = match.group()

        match = re.search('[0-9,]*[0-9,]*[0-9]{2,}', ratings[9].text)
        if match:
            movie_info['num_users'] = match.group()

    else:
        match = re.search(rp, ratings[5].text)
        if match:
            movie_info['user_rating'] = match.group()

        match = re.search('[0-9,]*[0-9,]*[0-9]{2,}', ratings[5].text)
        if match:
            movie_info['num_users'] = match.group()

    match = re.search(rp, ratings[0].text)
    if match:
        movie_info['all_reviewers_average'] = match.group()

    match = re.search(np, ratings[1].text)
    if match:
        movie_info['num_reviewers'] = match.group()

    match = re.search(np, ratings[2].text)
    if match:
        movie_info['all_fresh'] = match.group()

    match = re.search(np, ratings[3].text)
    if match:
        movie_info['all_rotten'] = match.group()

    return movie_info

N_MAX = 5

def url_request(index_filename, i, url, n = 1):
    try:
        r = urllib.request.urlopen(url)

    except Exception as e:
        print('Trying again: this is try ', n + 1)
        if n < N_MAX:
            time.sleep(5)
            r = url_request(index_filename, i, url, n + 1)

        else:
            movie_level_data(index_filename, i = i+1)

    return r

