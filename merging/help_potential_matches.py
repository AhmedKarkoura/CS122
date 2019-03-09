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

'''
imdb = pd.read_csv('../imdb/imdb_full.csv', low_memory=False)
names = pd.read_csv('../imdb/final_names.csv', low_memory=False)

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
imdb_same_title = imdb[imdb['primaryTitle'].isin(not_matched['title'])]

#try to match on title and yearplus1 and yearminus1
not_matched['year'] = not_matched['theater_date'].str[-4:]
imdb_same_title['yearplus1'] = imdb['startYear'] + 1
matches_yearplus1 = imdb_same_title.merge(not_matched, left_on=['primaryTitle', 'yearplus1'], right_on=['title', 'year'])
imdb_same_title['yearminus1'] = imdb['startYear'] - 1
matches_yearminus1 = imdb_same_title.merge(not_matched, left_on=['primaryTitle', 'yearminus1'], right_on=['title', 'year'])
not_matched = pd.concat(not_matched, matches_yearplus1, matches_yearminus1, matches_yearplus1, matches_yearminus1).drop_duplicates('movie_id', keep=False)

#try to match on rt_director1, rt_director2, rt_director3
imdb_same_title['director_id'] = imdb['directors'].str.split(',').str[0]
not_matched['director1'] = not_matched['directors'].str.split(', ').str[0]
not_matched['director2'] = not_matched['directors'].str.split(', ').str[1]
not_matched['director3'] = not_matched['directors'].str.split(', ').str[2]
imdb_same_title_director = imdb_same_title.merge(names, left_on='director_id', right_on='nconst')
matches_director1 = imdb_same_title_director.merge(not_matched, left_on=['primaryTitle','primaryName'], right_on=['title','director1'])
matches_director2 = imdb_same_title_director.merge(not_matched, left_on=['primaryTitle','primaryName'], right_on=['title','director2'])
matches_director3 = imdb_same_title_director.merge(not_matched, left_on=['primaryTitle','primaryName'], right_on=['title','director3'])
not_matched = pd.concat(not_matched, matches_director1, more_matches_director1, matches_director2, matches_director2, matches_director3, matches_director3).drop_duplicates('movie_id', keep=False)

#try to match on rt_writer1, rt_writer2, rt_writer3
imdb_same_title['writer_id'] = imdb['writers'].str.split(',').str[0]
not_matched['writer1'] = not_matched['writer'].str.split(', ').str[0]
not_matched['writer2'] = not_matched['writer'].str.split(', ').str[1]
not_matched['writer3'] = not_matched['writer'].str.split(', ').str[2]
imdb_same_title_writer = imdb_same_title.merge(names, left_on='writer_id', right_on='nconst')
matches_writer1 = imdb_same_title_writer.merge(not_matched, left_on=['primaryTitle','primaryName'], right_on=['title','writer1'])
matches_writer2 = imdb_same_title_writer.merge(not_matched, left_on=['primaryTitle','primaryName'], right_on=['title','writer2'])
matches_writer3 = imdb_same_title_writer.merge(not_matched, left_on=['primaryTitle','primaryName'], right_on=['title','writer3'])
not_matched = pd.concat(not_matched, matches_writer1, more_matches_writer1, matches_writer2, matches_writer2, matches_writer3, matches_writer3).drop_duplicates('movie_id', keep=False)

not_matched['simple_title'] = not_matched['title'].str.split(" \(").str[0]
imdb_same_simple_title = imdb[imdb['primaryTitle'].isin(not_matched['simple_title'])]

#try to match on simple title and year and yearplus1 and yearminus1
matches_simpleyear = imdb_same_simple_title.merge(not_matched, left_on=['primaryTitle', 'year'], right_on=['simple_title', 'year'])
imdb_same_simple_title['yearplus1'] = imdb['startYear'] + 1
matches_simpleyearplus1 = imdb_same_simple_title.merge(not_matched, left_on=['primaryTitle', 'yearplus1'], right_on=['simple_title', 'year'])
imdb_same_simple_title['yearminus1'] = imdb['startYear'] - 1
matches_simpleyearminus1 = imdb_same__simple_title.merge(not_matched, left_on=['primaryTitle', 'yearminus1'], right_on=['simple_title', 'year'])
not_matched = pd.concat(not_matched, matches_simpleyear, matches_simpleyear, matches_simpleyearplus1, matches_simpleyearminus1, matches_simpleyearplus1, matches_simpleyearminus1).drop_duplicates('movie_id', keep=False)

#try to match on same simple title and rt_director1, rt_director2, rt_director3
imdb_same_simple_title['director_id'] = imdb['directors'].str.split(',').str[0]
not_matched['director1'] = not_matched['directors'].str.split(', ').str[0]
not_matched['director2'] = not_matched['directors'].str.split(', ').str[1]
not_matched['director3'] = not_matched['directors'].str.split(', ').str[2]
imdb_same_simple_title_director = imdb_same_simple_title.merge(names, left_on='director_id', right_on='nconst')
matches_simpledirector1 = imdb_same_simple_title_director.merge(not_matched, left_on=['primaryTitle','primaryName'], right_on=['simple_title','director1'])
matches_simpledirector2 = imdb_same_simple_title_director.merge(not_matched, left_on=['primaryTitle','primaryName'], right_on=['simple_title','director2'])
matches_simpledirector3 = imdb_same_simple_title_director.merge(not_matched, left_on=['primaryTitle','primaryName'], right_on=['simple_title','director3'])
not_matched = pd.concat(not_matched, matches_simpledirector1, more_matches_simpledirector1, matches_simpledirector2, matches_simpledirector2, matches_simpledirector3, matches_simpledirector3).drop_duplicates('movie_id', keep=False)

#try to match on same simple title and rt_writer1, rt_writer2, rt_writer3
imdb_same_simple_title['writer_id'] = imdb['writers'].str.split(',').str[0]
not_matched['writer1'] = not_matched['writer'].str.split(', ').str[0]
not_matched['writer2'] = not_matched['writer'].str.split(', ').str[1]
not_matched['writer3'] = not_matched['writer'].str.split(', ').str[2]
imdb_same_simple_title_writer = imdb_same_simple_title.merge(names, left_on='writer_id', right_on='nconst')
matches_simplewriter1 = imdb_same_simple_title_writer.merge(not_matched, left_on=['primaryTitle','primaryName'], right_on=['simple_title','writer1'])
matches_simplewriter2 = imdb_same_simple_title_writer.merge(not_matched, left_on=['primaryTitle','primaryName'], right_on=['simple_title','writer2'])
matches_simplewriter3 = imdb_same_simple_title_writer.merge(not_matched, left_on=['primaryTitle','primaryName'], right_on=['simple_title','writer3'])
not_matched = pd.concat(not_matched, matches_simplewriter1, more_matches_simplewriter1, matches_simplewriter2, matches_simplewriter2, matches_simplewriter3, matches_simplewriter3).drop_duplicates('movie_id', keep=False)

FILES_TO_CONCAT = ['more_matches_1.csv','more_matches_2.csv', 'more_matches_9.csv', 'more_matches_16.csv', 'more_matches_19.csv', 'more_matches_29.csv',
    'more_matches_34.csv', 'more_matches_39.csv', 'more_matches_152.csv', 'more_matches_168.csv', 'more_matches_342.csv', 'more_matches_writer_1.csv',
    'more_matches_writer_1_2.csv']

SWAP_DIRECTOR_X_WITH_Y = ['more_matches_1.csv', 'more_matches_16.csv', 'more_matches_19.csv', 'more_matches_34.csv', 'more_matches_39.csv', 'more_matches_168.csv',
                          'more_matches_342.csv']

def clean_and_concat(files_to_concat, old_merged_file):
    old_merged = pd.read_csv(old_merged_file)
    columns_needed = list(old_merged.columns)
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
