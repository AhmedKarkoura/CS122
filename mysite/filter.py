import sqlite3
import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz
import csv

def merge(movie_level_csv, all_page_csv):
    movie_level_df = pd.read_csv(movie_level_csv)
    all_page_df = pd.read_csv(all_page_csv, sep = '|', header = None)
    all_page_df.columns = ['movie_id', 'top3actors', 'all_page_runtime', 'short_syn', 'all_page_title',
                           'all_page_title2', 'poster_url']
    merged_df = all_page_df.merge(movie_level_df, left_on='movie_id', right_on='movie_id')
    merged_df.to_csv('merged_all.csv', index = False)

    return merged_df

def clean_csv(csv_file_name):
    ratings = pd.read_csv(csv_file_name)
    ratings = ratings[['tconst', 'averageRating', 'title', 'directors_y', 
    'genre', 'box_office', 'mpaa', 'runtime',  'studio', 'writer', 'full_synop', 
    'all_reviewers_average', 'user_rating', 'year']]

    
    ratings.user_rating = ratings.user_rating.astype(str)
    ratings.user_rating = ratings.user_rating.apply(lambda x: x.split('/')[0])
    ratings.all_reviewers_average = ratings.all_reviewers_average.astype(str)
    ratings.all_reviewers_average = ratings.all_reviewers_average.apply(lambda x: x.split('/')[0])
    ratings['genre1'] = ratings['genre'].str.split(', ').str[0]
    ratings['genre2'] = ratings['genre'].str.split(', ').str[1]
    ratings['genre3'] = ratings['genre'].str.split(', ').str[2]
    ratings['director1'] = ratings['directors_y'].str.split(', ').str[0]
    ratings['director2'] = ratings['directors_y'].str.split(', ').str[1]
    ratings['writer1'] = ratings['writer'].str.split(', ').str[0]
    ratings['writer2'] = ratings['writer'].str.split(', ').str[1]
    ratings['writer3'] = ratings['writer'].str.split(', ').str[2]
    ratings['studio'] = ratings['studio'].str.split(', ').str[0]
    ratings['mpaa'] = ratings['mpaa'].str.split(' ').str[0]
    ratings.box_office = ratings.box_office.fillna(-1)
    ratings.box_office = ratings.box_office.astype(str).apply(lambda x: x.replace('$', '').replace(',', '')).astype(int)

    ratings = ratings[['tconst', 'averageRating', 'title',
       'box_office', 'mpaa', 'runtime', 'studio', 'full_synop',
       'all_reviewers_average', 'user_rating', 'year', 'genre1', 'genre2',
       'genre3', 'director1', 'director2', 'writer1', 'writer2', 'writer3']]

    ratings.columns = ['movie_id', 'imdb_score', 'title',
       'box_office', 'mpaa', 'runtime', 'studio', 'full_synop',
       'critics_score', 'audience_score', 'year', 'genre1', 'genre2',
       'genre3', 'director1', 'director2', 'writer1', 'writer2', 'writer3']

    ratings.to_csv('cleaned_matches.csv', index = False)

    return ratings

def find_movies(ui_dict):
    '''
    Inputs: 
        Key, value pairs in ui_dict:
            genre = string
            actor/actress = string
            director = string
            studio = string
            rating = string
            runtime <= int
            order by = ['oscar_winners', 'critics_score', 'audience_score', 'box_office']
    '''

    if not ui_dict:
        return ([], [])

    else:
        connection = sqlite3.connect('complete.db')
        c = connection.cursor()
        connection.create_function("fuzz", 2, fuzz.ratio)
        params = get_where_params(ui_dict)[1]
        query = get_query(ui_dict)
        r = c.execute(query, params)
        movies = r.fetchall() 
        connection.close()
        return movies

def get_query(ui_dict):
    QUERY = get_select(ui_dict) + get_from(ui_dict) + \
            get_where_params(ui_dict)[0] + get_orderby(ui_dict)

    return QUERY

def get_select(ui_dict):
    current_SELECT = ['ratings.title', 'ratings.critics_score', 'ratings.audience_score', 'ratings.box_office',
                      'ratings.director1']
    actual_SELECT = ['ratings.title', 'ratings.genre1', 'ratings.genre2', 'ratings.genre3', 'ratings.director1',
                     'ratings.writer1', 'ratings.top_actors', 'ratings.critics_score', 'ratings.audience_score', 
                     'ratings.imdb_score', 'ratings.box_office', 'ratings.poster_url', 'ratings.short_syn', 
                     'ratings.runtime']
    if ui_dict['order_by'] == 'oscars_nominations':
        current_SELECT.append('oscars.total_nominations')
    query_SELECT = 'SELECT DISTINCT ' + ', '.join(current_SELECT)
    
    return query_SELECT


def get_from(ui_dict):
    FROM = ['ratings', 'principal', 'names']
    ON = ['ratings.movie_id = principal.movie_id', 'principal.name_id = names.name_id']

    if ui_dict['order_by'] == 'oscars_nominations':
        FROM.append(("(SELECT awards.movie, awards_num + acting_num AS total_nominations, awards.year "
        "FROM (SELECT awards.movie, COUNT(*) AS awards_num, awards.year "
        "FROM awards GROUP BY awards.movie, awards.year) AS awards "
        "LEFT JOIN (SELECT acting_nominees.movie, COUNT(*) AS acting_num, acting_nominees.year "
        "FROM acting_nominees GROUP BY acting_nominees.movie, acting_nominees.year) "
        "AS acting_nominees ON awards.movie = acting_nominees.movie) as oscars"))
        ON += ["ratings.title = oscars.movie", "ratings.year = oscars.year"]

    query_FROM = " FROM " + ' JOIN '.join(FROM) + " ON " + ' AND '.join(ON)
    return query_FROM

def get_where_params(ui_dict):
    WHERE_DICT = {"genre": "(ratings.genre1 == ? OR ratings.genre2 == ? OR ratings.genre3 == ?)",
                  "actor": "(fuzz(names.name, ?) >= 80 and (principal.category == 'actor' OR principal.category == 'actress'))",
                  "director": "(fuzz(ratings.director1, ?) >= 80 OR fuzz(ratings.director2, ?) >= 80)",
                  "studio": "studio = ?",
                  "rating": "rating = ?",
                  "runtime": "runtime <= ?"}
    WHERE = []
    params = []

    for arg in ui_dict:
        if arg in WHERE_DICT:
            if arg in ['actor', 'director']:
                searches_where = []
                searches = ui_dict[arg].split(',')
                searches = [search.strip(' ') for search in searches]
                for search in searches:
                    searches_where.append(WHERE_DICT[arg])
                    if arg == 'director':
                        params += 2 * [search.title()]
                    else:
                        params.append(search.title())
                WHERE.append('(' + ' OR '.join(searches_where) + ')')
            else:
                if arg == 'genre':    
                    params += 3 * [ui_dict[arg][:]]
                else:
                    params.append(ui_dict[arg])
                WHERE.append(WHERE_DICT[arg])

    query_WHERE = " WHERE " + " AND ".join(WHERE)

    return query_WHERE, params

def get_orderby(ui_dict):
    ORDERBY_DICT = {"oscars_nominations": "total_nominations DESC",
                    "critics_score": "ratings.critics_score DESC",
                    "audience_score": "ratings.audience_score DESC",
                    "box_office": "ratings.box_office DESC"}
    
    query_ORDERBY = " ORDER BY " + ORDERBY_DICT[ui_dict['order_by']]

     


    return query_ORDERBY

TEST_2 = {'actor': 'emma stone , matt damon',  
          'director': 'woody allen, damien chazelle',
          'order_by': 'oscars_nominations',
          'genre': 'Drama'}

TEST_0 = {'actor': "emma stone",
          'order_by': 'oscars_nominations'}

TEST_1 = {
    'genre': 'Drama',
    'actor': 'Matt Damon',
    'studio': 'Universal',
    'runtime': 150,
    'mpaa': "PG-13",
    'order_by': 'audience_score'}
