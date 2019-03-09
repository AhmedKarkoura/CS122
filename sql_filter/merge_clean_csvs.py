'''
Merge and Clean CSVs to create database
'''
import pandas as pd
import numpy as np
import csv

def merge(movie_level_csv, all_page_csv):
    '''
    Merge movie level csv data with pages level csv data and writes csv file 
    with merged data

    Inputs: 
        movie_level_csv: movie level csv filename
        all_page_csv: page level csv filename
    '''

    movie_level_df = pd.read_csv(movie_level_csv)
    all_page_df = pd.read_csv(all_page_csv, sep='|', header=None)
    all_page_df.columns = ['movie_id', 'top3actors', 'all_page_runtime', 
                           'short_syn', 'all_page_title', 'url', 'poster_url']
    merged_df = all_page_df.merge(movie_level_df, left_on='movie_id', 
                                                  right_on='movie_id')

    merged_df.to_csv('movie_level_all_pages.csv', index=False)

    return merged_df

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

    acting_noms_df = pd.read_csv(acting_nominees_csv)
    oscars_awards_df = pd.read_csv(oscars_awards_csv)
    merged_df = pd.read_csv(merged_csv)

    acting_nom_count_df = acting_noms_df.groupby(['movie', 'year'])\
                         .size().reset_index(name='acting_count')
    oscars_nom_count_df = oscars_awards_df.groupby(['entity', 'year'])\
                         .size().reset_index(name='other_awards_count')
    noms_df = pd.merge(oscars_nom_count_df, acting_nom_count_df, 
        how='outer', left_on=['entity', 'year'], right_on=['movie','year'])
    noms_df['movie'] = noms_df['movie'].fillna(noms_df['entity'])
    noms_df = noms_df.drop(columns='entity')
    noms_df = noms_df.fillna(0)
    noms_df['acting_count'] = noms_df.acting_count.astype(int)
    noms_df['other_awards_count'] = noms_df.other_awards_count.astype(int)
    noms_df['total_nomination_count'] = noms_df['acting_count'] + \
                                        noms_df['other_awards_count']

    merged_df['lower_case_title'] = merged_df['primaryTitle'].str.lower()\
                                                          .str.strip(' ')
    noms_df['lower_case_title'] = noms_df['movie'].str.lower().str.strip(' ')
    merged_df = merged_df.merge(noms_df, how='left', 
        left_on=['lower_case_title', 'year'], 
        right_on = ['lower_case_title', 'year'])
    merged_df['total_nomination_count'] = merged_df['total_nomination_count']\
                                          .fillna(0)
    merged_df['total_nomination_count'] = merged_df['total_nomination_count']\
                                          .astype(int)

    merged_df.to_csv('merged_oscar_count.csv', index = False)

    return merged_df

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

    ratings.user_rating = ratings.user_rating.fillna(0)
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

    ratings.to_csv('ratings.csv', index = False)

    return ratings