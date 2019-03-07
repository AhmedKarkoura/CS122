import sqlite3
import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz
import csv
import actor_director_posters as adp

def merge(movie_level_csv, all_page_csv):
    '''
    Merge movie level csv data with pages level csv data and writes csv file 
    with merged data

    Inputs: 
        movie_level_csv: movie level csv filename
        all_page_csv: page level csv filename
    '''

    movie_level_df = pd.read_csv(movie_level_csv)
    all_page_df = pd.read_csv(all_page_csv, sep = '|', header = None)
    all_page_df.columns = ['movie_id', 'top3actors', 'all_page_runtime', 
                           'short_syn', 'all_page_title', 'url', 'poster_url']
    merged_df = all_page_df.merge(movie_level_df, left_on='movie_id', 
                                                  right_on='movie_id')
    merged_df.to_csv('merged_all.csv', index = False)


def get_oscar_nomination_count(oscars_awards_csv, acting_nominees_csv, 
                               merged_csv):
    '''
    Add total oscar nomination count column to merged data csv

    Inputs:
        oscars_awards_csv: oscars award csv filename; file contains all oscars
            nominations except for nominations for acting awards
        acting_nominations_csv: acting nominations csv filename; file contains 
            all acting nominations
    '''

    acting_nominees_df = pd.read_csv(acting_nominees_csv)
    oscars_awards_df = pd.read_csv(oscars_awards_csv)
    merged_df = pd.read_csv(merged_csv)

    acting_nomination_count_df = acting_nominees_df.groupby(['movie', 'year'])\
                                 .size().reset_index(name = 'acting_count')
    oscars_nominations_count_df = oscars_awards_df.groupby(['entity', 'year'])\
                              .size().reset_index(name = 'other_awards_count')
    nominations_df = pd.merge(oscars_nominations_count_df, 
        acting_nomination_count_df, how = 'outer', left_on= ['entity', 'year'],
        right_on = ['movie','year'])
    nominations_df['movie'] = nominations_df['movie'].\
                              fillna(nominations_df['entity'])
    nominations_df = nominations_df.drop(columns = 'entity')
    nominations_df = nominations_df.fillna(0)
    nominations_df['acting_count'] = nominations_df.acting_count.astype(int)
    nominations_df['other_awards_count'] = nominations_df.other_awards_count\
                                           .astype(int)
    nominations_df['total_nomination_count'] = nominations_df['acting_count']\
                                       + nominations_df['other_awards_count']

    merged_df['lower_case_title'] = merged_df['primaryTitle'].str.lower()\
                                                          .str.strip(' ')
    nominations_df['lower_case_title'] = nominations_df['movie'].str.lower()\
                                                             .str.strip(' ')
    merged_df = merged_df.merge(nominations_df, how = 'left', 
        left_on = ['lower_case_title', 'year'], 
        right_on = ['lower_case_title', 'year'])
    merged_df['total_nomination_count'] = merged_df['total_nomination_count']\
                                          .fillna(0)
    merged_df['total_nomination_count'] = merged_df['total_nomination_count']\
                                          .astype(int)

    merged_df.to_csv('database.csv', index = False)


def clean_csv(csv_file_name):
    '''
    Clean merged data csv (change column types, drop unneccessary columns, etc)

    Inputs:
        csv_file_name: csv filename for file that contains all the merged data
    '''

    ratings = pd.read_csv(csv_file_name)
    ratings = ratings[['top3actors', 'short_syn', 'url', 'poster_url', 
                       'tconst', 'averageRating', 'title', 'directors_y', 
                       'genre', 'box_office', 'mpaa', 'runtime', 'studio', 
                       'writer', 'full_synop', 'all_reviewers_average', 
                       'user_rating', 'year', 'total_nomination_count']]
    
    ratings.user_rating = ratings.user_rating.astype(str)
    ratings.user_rating = ratings.user_rating.apply(lambda x: x.split('/')[0])
    ratings.all_reviewers_average = ratings.all_reviewers_average.astype(str)
    ratings.all_reviewers_average = ratings.all_reviewers_average\
                                             .apply(lambda x: x.split('/')[0])
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
    ratings.box_office = ratings.box_office.astype(str).apply(lambda x: \
                              x.replace('$', '').replace(',', '')).astype(int)

    ratings = ratings[['top3actors', 'short_syn', 'url', 'poster_url', 
                       'tconst', 'averageRating', 'title', 'box_office', 
                       'mpaa', 'runtime', 'studio', 'full_synop',
                       'all_reviewers_average', 'user_rating', 'year', 
                       'genre1', 'genre2', 'genre3', 'director1', 'director2', 
                       'writer1', 'writer2', 'writer3',
                       'total_nomination_count']]

    ratings.columns = ['top3actors', 'short_synopsis', 'url', 'poster_url', 
                       'movie_id', 'imdb_score', 'title', 'box_office', 
                       'mpaa', 'runtime', 'studio', 'full_synopsis',
                       'critics_score', 'audience_score', 'year', 'genre1', 
                       'genre2', 'genre3', 'director1', 'director2', 
                       'writer1', 'writer2', 'writer3', 
                       'oscars_nomination_count']

    ratings.to_csv('database.csv', index = False)

def find_movies(ui_dict):
    '''
    Finds movies that satisfy given criteria from ui_dict
    Inputs: 
        Key, value pairs in ui_dict:
            genre = string
            actor/actress = string
            director = string
            studio = string
            rating = string
            runtime <= int
            order by = ['oscar_winners', 'critics_score', 'audience_score', 
            'box_office']

    Return: 
        header, movies that fit the filter criteria
    '''

    if not ui_dict:
        return ([], [])

    else:
        connection = sqlite3.connect('final_complete.db')
        c = connection.cursor()
        connection.create_function("fuzz", 2, fuzz.ratio)
        connection.create_function("format_box_office", 1, format_box_office)
        connection.create_function("format_top3actors", 1, format_top3actors)
        connection.create_function("format_genre", 1, format_genre)
        connection.create_function("format_poster_url", 1, format_poster_url)
        #connection.create_function("get_people_pics", 1, actor_director_posters.get_picture_url)
        params = get_where_params(ui_dict)[1]
        query = get_query(ui_dict)
        r = c.execute(query, params)
        movies = r.fetchall() 
        connection.close()
        if len(movies) == 0:
            return ([],[])
        else:
            final = []
            for movie in movies:
                url = movie[-1]
                movie = tuple(movie[:len(movie)-1])
                movie += adp.get_person_posters(url)

                final.append(movie)
            
            return (get_header(r) + ['hello'], final)

def format_genre(genre):
    if not genre:
        return "N/A"
    else: 
        return genre

def format_box_office(box_office):
    if box_office == '-1':
        return "Not Available"
    else: 
        return "$" + "{:,}".format(int(box_office))

def format_top3actors(top3actors):
    top3actors = top3actors.split('/') 
    return '\n'.join(top3actors)

def format_poster_url(poster_url):
    img_url = "<img src=" + '"' + poster_url + '">'
    return img_url 

def get_header(cursor):
    '''
    Given a cursor object, returns the appropriate header (column names)
    '''
    desc = cursor.description
    header = ()

    for i in desc:
        header = header + (clean_header(i[0]),)

    return list(header)

def clean_header(s):
    '''
    Removes table name from header
    '''
    for i, _ in enumerate(s):
        if s[i] == ".":
            s = s[i + 1:]
            break

    return s


def get_query(ui_dict):
    QUERY = get_select(ui_dict) + get_from(ui_dict) + \
            get_where_params(ui_dict)[0] + get_orderby(ui_dict) + " LIMIT 10"

    return QUERY

def get_select(ui_dict):
    actual_SELECT = ["ratings.title", "ratings.genre1", 
                     "format_genre(ratings.genre2) AS genre2", 
                     "format_genre(ratings.genre3) AS genre3", 
                     "ratings.director1", "ratings.writer1", 
                     "format_top3actors(ratings.top3actors) AS top3actors", 
                     "ratings.critics_score", 
                     "ratings.audience_score", 
<<<<<<< HEAD
                     "format_box_office(ratings.box_office) AS money", 
                     "ratings.poster_url AS poster_url", "ratings.short_synop", 
                     "ratings.runtime||' minutes' AS runtime", "ratings.mpaa"]
=======
                     "format_box_office(ratings.box_office) AS box_office", 
                     "ratings.short_synop", "ratings.runtime||' minutes' AS runtime", 
                     "ratings.mpaa", "ratings.poster_url AS poster_url", "url"]
>>>>>>> d02d631a115b1a5024074d1207b98e1da3f9b8ab
                     #"get_people_pics(ratings.url) AS pics"]
    if ui_dict['order_by'] == "oscars_nominations":
        actual_SELECT.append("ratings.oscar_nomination_count||' nominations'"\
                             + " AS oscars_nominations")
    query_SELECT = 'SELECT DISTINCT ' + ', '.join(actual_SELECT)
    
    return query_SELECT


def get_from(ui_dict):
    FROM = ['ratings', 'principal', 'names']
    ON = ['ratings.movie_id = principal.movie_id', 'principal.name_id = names.name_id']
    '''

    if ui_dict['order_by'] == 'oscars_nominations':
        FROM.append(("(SELECT awards.movie, awards_num + acting_num AS total_nominations, awards.year "
        "FROM (SELECT awards.movie, COUNT(*) AS awards_num, awards.year "
        "FROM awards GROUP BY awards.movie, awards.year) AS awards "
        "LEFT JOIN (SELECT acting_nominees.movie, COUNT(*) AS acting_num, acting_nominees.year "
        "FROM acting_nominees GROUP BY acting_nominees.movie, acting_nominees.year) "
        "AS acting_nominees ON awards.movie = acting_nominees.movie) as oscars"))
        ON += ["ratings.title = oscars.movie", "ratings.year = oscars.year"]
    '''

    query_FROM = " FROM " + ' JOIN '.join(FROM) + " ON " + ' AND '.join(ON)
    return query_FROM

def get_where_params(ui_dict):
    WHERE_DICT = {
        "genre": "(ratings.genre1 == ? OR ratings.genre2 == ? OR ratings.genre3 == ?)",
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
    ORDERBY_DICT = {"oscars_nominations": "ratings.oscar_nomination_count DESC",
                    "critics_score": "ratings.critics_score DESC",
                    "audience_score": "ratings.audience_score DESC",
                    "box_office": "ratings.box_office DESC"}
    
    query_ORDERBY = " ORDER BY " + ORDERBY_DICT[ui_dict['order_by']]

    return query_ORDERBY

TEST_2 = {'actor': 'emma stone , matt damon',  
          'director': 'woody allen, damien chazelle',
          'order_by': 'box_office',
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

