import pandas as pd
'''
final_merged = pd.read_csv('final_merged.csv')
potential_matches = pd.read_csv('potential_matches.csv')
potential_matches['director1'] = potential_matches['directors'].str.split(', ').str[0]
potential_matches['director2'] = potential_matches['directors'].str.split(', ').str[1]

#These are RT entries with same exact title in RT and IMDB but didnt match on year
#Or on individual director(IDEA: These mostly have multiple directors, if we match
#one of the directors to one of the directors in the imdb)


rt = pd.read_csv('../rt_scraper/sql_db_files/all_movies.csv', sep = "|", header = None)
rt.columns = columns = ['movie_id','title' ,'directors', 'genre','theater_date','stream_date',
'box_office','mpaa','runtime', 'studio','writer','full_synop',
'all_reviewers_average','num_all_reviewers',
'num_all_fresh','num_all_rotten','top_reviewers_average','num_top_reviewers',
'num_top_fresh','num_top_rotten','user_rating','num_users']
rt['theater_date'] = rt['theater_date'].astype(str)
rt['year'] = rt['theater_date'].apply(lambda x: x[-4:])


imdb = pd.read_csv('../imdb/imdb_full.csv', low_memory=False)
imdb['director_id1'] = imdb['directors'].str.split(',').str[0]
imdb['director_id2'] = imdb['directors'].str.split(',').str[1]

imdb_names = pd.read_csv('updated_names.csv')


#Look at the shapes of each. (BEST case scenario: final_merged contains all of rt)


#find all unmatched movies in rt
merged = pd.read_csv('final_merged.csv')
merged = merged[['movie_id','title' ,'directors_y', 'genre','theater_date','stream_date',                                                                
    'box_office','mpaa','runtime', 'studio','writer','full_synop',
    'all_reviewers_average','num_all_reviewers',                                 
    'num_all_fresh','num_all_rotten','top_reviewers_average','num_top_reviewers',
    'num_top_fresh','num_top_rotten','user_rating','num_users']]
merged.columns = ['movie_id','title' ,'directors', 'genre','theater_date','stream_date'                                                                 
    'box_office','mpaa','runtime', 'studio','writer','full_synop',
    'all_reviewers_average','num_all_reviewers',                                 
    'num_all_fresh','num_all_rotten','top_reviewers_average','num_top_reviewers',
    'num_top_fresh','num_top_rotten','user_rating','num_users']
rt = pd.read_csv('../rt_scraper/sql_db_files/all_movies.csv', sep = "|", header = None)
rt.columns = ['movie_id', 'title', 'directors', 'genre', 'theater_date',
       'stream_date', 'box_office', 'mpaa', 'runtime', 'studio', 'writer',
       'full_synop', 'all_reviewers_average', 'num_all_reviewers',
       'num_all_fresh', 'num_all_rotten', 'top_reviewers_average',
       'num_top_reviewers', 'num_top_fresh', 'num_top_rotten', 'user_rating',
       'num_users']
rt['movie_id'] = rt['movie_id'].astype(int)
not_matched = pd.concat([rt, merged, merged]).drop_duplicates('movie_id',keep=False)
not_matched['simple_title'] = not_matched['title'].str.split(" \(").str[0]
unmatched_same_title = not_matched[not_matched['title'].isin(imdb['primaryTitle'])]
not_matched['year'] = not_matched['theater_date'].str[-4:]
unmatched_same_title.merge(imdb, how='left', left_on = ['simple_title', 'year'], right_on = ['primaryTitle', 'startYear'])
imdb_same_title = imdb[imdb['primaryTitle'].isin(unmatched_same_title['title'])]
imdb_same_title['yearplus1'] = imdb_same_title['startYear'] + 1
imdb_same_title['yearminus1'] = imdb_same_title['startYear'] - 1
more_matches_yearminus1 = unmatched_same_title.merge(imdb_same_title, how='inner', left_on = ['title', 'year'], right_on = ['primaryTitle', 'yearminus1'])
more_matches_yearplus1 = unmatched_same_title.merge(imdb_same_title, how='inner', left_on = ['title', 'year'], right_on = ['primaryTitle', 'yearminus1'])
more_matches_director1 = rt_same_title3.merge(imdb_same_title3_director, how='inner', left_on = ['title', 'director_1'], right_on= ['primaryTitle', 'primaryName'])
more_matches_director1 = rt_same_title3.merge(imdb_same_title3_director, how='inner', left_on = ['title', 'director_2'], right_on= ['primaryTitle', 'primaryName'])
imdb_same_title_4_writers = imdb_same_title_4.merge(names, left_on = 'writer1', right_on = 'nconst')
rt_same_title_4['writer_1'] = rt_same_title_4['writer'].str.split(', ').str[0]
more_matches_writer1 = rt_same_title_4.merge(imdb_same_title_4_writers, how='inner', left_on = ['title', 'writer_1'], right_on= ['primaryTitle', 'primaryName'])
matches_yearminus1 = imdb_same_title.merge(not_matched, left_on = ['primaryTitle', 'yearminus1'], right_on = ['simple_title', 'year'])
'''
# try to match on title, yearplus1, yearminus1
# try to match on title, rt_director1, rt_director2, rt_director3
# try to match on title, rt_writer1, rt_writer2, rt_writer3
# try the same matches on rt_simple_title (remove text in parenthesis)

FILES_TO_CONCAT = ['more_matches_1.csv','more_matches_2.csv', 'more_matches_9.csv', 'more_matches_16.csv', 'more_matches_19.csv', 'more_matches_29.csv',
    'more_matches_34.csv', 'more_matches_39.csv', 'more_matches_152.csv', 'more_matches_168.csv', 'more_matches_342.csv', 'more_matches_writer_1.csv',
    'more_matches_writer_1_2.csv']

SWAP_DIRECTOR_X_WITH_Y = ['more_matches_1.csv', 'more_matches_16.csv', 'more_matches_19.csv', 'more_matches_34.csv', 'more_matches_39.csv', 'more_matches_168.csv',
                          'more_matches_342.csv']

def clean_and_concat(files_to_concat, old_merged_file):
    old_merged = pd.read_csv(old_merged_file)
    columns_needed = list(old_merged.columns)
    #new_merged = pd.DataFrame()
    new_merged = old_merged
    for file in files_to_concat:
        file_df = pd.read_csv(file)
        if 'year' not in file_df.columns:
            print(file)
            file_df['theater_date'] = file_df['theater_date'].astype(str)
            file_df['year'] = file_df['theater_date'].str[-4:]
        file_df = file_df[columns_needed]
        file_df.columns = ['tconst', 'averageRating', 'numVotes', 'primaryTitle', 'isAdult',
       'startYear', 'runtimeMinutes', 'genres', 'directors_x', 'writers',
       'movie_id', 'title', 'directors_y', 'genre', 'theater_date',
       'stream_date', 'box_office', 'mpaa', 'runtime', 'studio', 'writer',
       'full_synop', 'all_reviewers_average', 'num_all_reviewers',
       'num_all_fresh', 'num_all_rotten', 'top_reviewers_average',
       'num_top_reviewers', 'num_top_fresh', 'num_top_rotten', 'user_rating',
       'num_users', 'year']
        if file in SWAP_DIRECTOR_X_WITH_Y:
            file_df.columns = ['tconst', 'averageRating', 'numVotes', 'primaryTitle', 'isAdult',
            'startYear', 'runtimeMinutes', 'genres', 'directors_y', 'writers',
       'movie_id', 'title', 'directors_x', 'genre', 'theater_date',
       'stream_date', 'box_office', 'mpaa', 'runtime', 'studio', 'writer',
       'full_synop', 'all_reviewers_average', 'num_all_reviewers',
       'num_all_fresh', 'num_all_rotten', 'top_reviewers_average',
       'num_top_reviewers', 'num_top_fresh', 'num_top_rotten', 'user_rating',
       'num_users', 'year']
        new_merged = pd.concat([new_merged, file_df], sort=False)
    new_merged = new_merged.drop_duplicates('movie_id')
    new_merged.to_csv('fixed_8709_merged.csv', index = False)
    return new_merged
