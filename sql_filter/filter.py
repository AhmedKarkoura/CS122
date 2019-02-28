import sqlite3
import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz
import csv

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
    current_SELECT = ['ratings.title', 'ratings.critics_score', 'ratings.audience_score', 'ratings.box_office']
    actual_SELECT = ['ratings.title', 'ratings.genre1', 'ratings.genre2', 'ratings.genre3', 'ratings.director1',
                     'ratings.writer1', 'ratings.top_actors', 'ratings.critics_score', 'ratings.audience_score', 
                     'ratings.imdb_score', 'ratings.box_office', 'ratings.poster_url', 'ratings.short_syn', 
                     'ratings.runtime']
    query_SELECT = 'SELECT DISTINCT ' + ', '.join(current_SELECT)
    
    return query_SELECT


def get_from(ui_dict):
    query_FROM = " FROM ratings JOIN principal JOIN names ON ratings.movie_id = principal.movie_id AND principal.name_id = names.name_id"
    '''
    "JOIN awards JOIN acting_nominees" + \
           "ON ratings.tconst = principal.tconst AND principal.nconst = names.nconst " + \
           "AND ratings.tconst = oscars.tconst AND principal.nconst = acting_nominees.nconst " + \
           "AND principal.tconst = acting_nominees.tconst"
    '''

    return query_FROM

def get_where_params(ui_dict):
    WHERE_DICT = {"genre": "(ratings.genre1 == ? OR ratings.genre2 == ? OR ratings.genre3 == ?)",
                  "actor": "(fuzz(names.name, ?) >= 80 and (principal.category == 'actor' or principal.category == 'actress'))",
                  "director": "(fuzz(names.name, ?) >= 80 and principal.category == 'director')",
                  "studio": "studio = ?",
                  "rating": "rating = ?",
                  "runtime": "runtime <= ?"}
    WHERE = []
    params = []

    for arg in ui_dict:
        if arg in WHERE_DICT:
            WHERE.append(WHERE_DICT[arg])
            if arg == 'genre':    
                params += 3 * [ui_dict[arg][:]]
            elif arg in ['actor', 'director', 'studio']:
                params.append(ui_dict[arg].title())
            else: 
                params.append(ui_dict[arg])

    query_WHERE = " WHERE " + " AND ".join(WHERE)

    return query_WHERE, params

def get_orderby(ui_dict):
    ORDERBY_DICT = {"oscar_winners": "",
                    "critics_score": "ratings.critics_score DESC",
                    "audience_score": "ratings.audience_score DESC",
                    "box_office": "ratings.box_office DESC"}
    
    query_ORDERBY = "ORDER BY " + ORDERBY_DICT[ui_dict['order_by']]

    return query_ORDERBY

TEST_0 = {'genre': 'Drama',
          'actor': "TOM CRUISE",
          'order_by': 'critics_score'}

TEST_1 = {
    'genre': 'Drama',
    'actor': 'Matt Damon',
    'studio': 'Universal',
    'runtime': 150,
    'mpaa': "PG-13",
    'order_by': 'audience_score'}

