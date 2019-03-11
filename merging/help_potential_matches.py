'''
Get more matches between RT database and Imdb database
'''

import pandas as pd

# full imdb movies dataframe
imdb = pd.read_csv('../imdb/imdb_full.csv', low_memory=False)
# full imdb names dataframe
names = pd.read_csv('../imdb/final_names.csv', low_memory=False)

# find all unmatched movies in rt
# matches dataframe
merged = pd.read_csv('final_merged.csv')
merged = merged[['movie_id','title' ,'directors_y', 'genre','theater_date',
                 'stream_date', 'box_office','mpaa','runtime', 'studio',
                 'writer','full_synop', 'all_reviewers_average',
                 'num_all_reviewers', 'num_all_fresh','num_all_rotten',
                 'top_reviewers_average','num_top_reviewers',
                 'num_top_fresh','num_top_rotten','user_rating','num_users']]
merged.columns = ['movie_id','title' ,'directors', 'genre','theater_date',
                  'stream_date', 'box_office','mpaa','runtime', 'studio',
                  'writer','full_synop', 'all_reviewers_average',
                  'num_all_reviewers', 'num_all_fresh','num_all_rotten',
                  'top_reviewers_average','num_top_reviewers',
                  'num_top_fresh','num_top_rotten','user_rating','num_users']
# full rotten tomatoes dataframe
rt = pd.read_csv('../rt_scraper/sql_db_files/all_movies.csv', sep = "|", 
                                                              header = None)
rt.columns = ['movie_id', 'title', 'directors', 'genre', 'theater_date',
              'stream_date', 'box_office', 'mpaa', 'runtime', 'studio', 
              'writer', 'full_synop', 'all_reviewers_average', 
              'num_all_reviewers', 'num_all_fresh', 'num_all_rotten', 
              'top_reviewers_average', 'num_top_reviewers', 'num_top_fresh', 
              'num_top_rotten', 'user_rating', 'num_users']
rt['movie_id'] = rt['movie_id'].astype(int)

# dataframe of movies in rt dataframe that haven't yet been matched with 
# movies in imdb dataframe
not_matched = pd.concat([rt, merged, merged]).drop_duplicates('movie_id',
                                                              keep=False)

# movies in imdb datafram that have same title as movies in unmatched dataframe
imdb_same_title = imdb[imdb['primaryTitle'].isin(not_matched['title'])]

# try to match on title and yearplus1 and yearminus1
not_matched['year'] = not_matched['theater_date'].str[-4:]
imdb_same_title['yearplus1'] = imdb['startYear'] + 1
matches_yearplus1 = imdb_same_title.merge(not_matched, 
          left_on=['primaryTitle', 'yearplus1'], right_on=['title', 'year'])
imdb_same_title['yearminus1'] = imdb['startYear'] - 1
matches_yearminus1 = imdb_same_title.merge(not_matched, 
          left_on=['primaryTitle', 'yearminus1'], right_on=['title', 'year'])

# updated unmatched dataframe 
not_matched = pd.concat([not_matched, matches_yearplus1, matches_yearplus1, 
                        matches_yearminus1, matches_yearminus1]).\
                 drop_duplicates('movie_id', keep=False)

# try to match on rt_director1, rt_director2, rt_director3
imdb_same_title['director_id'] = imdb['directors'].str.split(',').str[0]
not_matched['director1'] = not_matched['directors'].str.split(', ').str[0]
not_matched['director2'] = not_matched['directors'].str.split(', ').str[1]
not_matched['director3'] = not_matched['directors'].str.split(', ').str[2]

# get name of primary imdb director from nconst in imdb movie dataframe 
# and name from names dataframe
imdb_same_title_director = imdb_same_title.merge(names, left_on='director_id',
                                                        right_on='nconst')
matches_director1 = imdb_same_title_director.merge(not_matched, 
      left_on=['primaryTitle','primaryName'], right_on=['title','director1'])
matches_director2 = imdb_same_title_director.merge(not_matched, 
      left_on=['primaryTitle','primaryName'], right_on=['title','director2'])
matches_director3 = imdb_same_title_director.merge(not_matched, 
      left_on=['primaryTitle','primaryName'], right_on=['title','director3'])

not_matched = pd.concat([not_matched, matches_director1, more_matches_director1,
                         matches_director2, matches_director2, 
                         matches_director3, matches_director3]).\
                 drop_duplicates('movie_id', keep=False)

#try to match on rt_writer1, rt_writer2, rt_writer3
imdb_same_title['writer_id'] = imdb['writers'].str.split(',').str[0]
not_matched['writer1'] = not_matched['writer'].str.split(', ').str[0]
not_matched['writer2'] = not_matched['writer'].str.split(', ').str[1]
not_matched['writer3'] = not_matched['writer'].str.split(', ').str[2]

# get name of primary imdb writer from nconst in imdb movie dataframe 
# and name from names dataframe
imdb_same_title_writer = imdb_same_title.merge(names, left_on='writer_id', 
                                                      right_on='nconst')
matches_writer1 = imdb_same_title_writer.merge(not_matched, 
        left_on=['primaryTitle','primaryName'], right_on=['title','writer1'])
matches_writer2 = imdb_same_title_writer.merge(not_matched, 
        left_on=['primaryTitle','primaryName'], right_on=['title','writer2'])
matches_writer3 = imdb_same_title_writer.merge(not_matched, 
        left_on=['primaryTitle','primaryName'], right_on=['title','writer3'])
not_matched = pd.concat([not_matched, matches_writer1, more_matches_writer1, 
                         matches_writer2, matches_writer2, matches_writer3, 
                         matches_writer3]).\
                 drop_duplicates('movie_id', keep=False)

# some titles in rt are translated and contain original title in parentheses
# extract translated title only, "simple title" without original title
not_matched['simple_title'] = not_matched['title'].str.split(" \(").str[0]
imdb_same_simple_title = imdb[imdb['primaryTitle'].isin(not_matched['simple_title'])]

#try to match on simple title and year and yearplus1 and yearminus1
matches_simpleyear = imdb_same_simple_title.merge(not_matched, 
    left_on=['primaryTitle', 'year'], right_on=['simple_title', 'year'])
imdb_same_simple_title['yearplus1'] = imdb['startYear'] + 1
matches_simpleyearplus1 = imdb_same_simple_title.merge(not_matched, 
    left_on=['primaryTitle', 'yearplus1'], right_on=['simple_title', 'year'])
imdb_same_simple_title['yearminus1'] = imdb['startYear'] - 1
matches_simpleyearminus1 = imdb_same__simple_title.merge(not_matched, 
    left_on=['primaryTitle', 'yearminus1'], right_on=['simple_title', 'year'])

not_matched = pd.concat([not_matched, matches_simpleyear, matches_simpleyear, 
                         matches_simpleyearplus1, matches_simpleyearplus1, 
                         matches_simpleyearminus1, matches_simpleyearminus1]).\
                 drop_duplicates('movie_id', keep=False)

#try to match on same simple title and rt_director1, rt_director2, rt_director3
imdb_same_simple_title['director_id'] = imdb['directors'].str.split(',').str[0]
not_matched['director1'] = not_matched['directors'].str.split(', ').str[0]
not_matched['director2'] = not_matched['directors'].str.split(', ').str[1]
not_matched['director3'] = not_matched['directors'].str.split(', ').str[2]
imdb_same_simple_title_director = imdb_same_simple_title.merge(names, 
                                    left_on='director_id', right_on='nconst')
matches_simpledirector1 = imdb_same_simple_title_director.merge(not_matched, 
  left_on=['primaryTitle','primaryName'], right_on=['simple_title','director1'])
matches_simpledirector2 = imdb_same_simple_title_director.merge(not_matched, 
  left_on=['primaryTitle','primaryName'], right_on=['simple_title','director2'])
matches_simpledirector3 = imdb_same_simple_title_director.merge(not_matched, 
  left_on=['primaryTitle','primaryName'], right_on=['simple_title','director3'])

not_matched = pd.concat([not_matched, matches_simpledirector1, 
                         more_matches_simpledirector1, matches_simpledirector2,
                         matches_simpledirector2, matches_simpledirector3, 
                         matches_simpledirector3]).\
                 drop_duplicates('movie_id', keep=False)

#try to match on same simple title and rt_writer1, rt_writer2, rt_writer3
imdb_same_simple_title['writer_id'] = imdb['writers'].str.split(',').str[0]
not_matched['writer1'] = not_matched['writer'].str.split(', ').str[0]
not_matched['writer2'] = not_matched['writer'].str.split(', ').str[1]
not_matched['writer3'] = not_matched['writer'].str.split(', ').str[2]
imdb_same_simple_title_writer = imdb_same_simple_title.merge(names, 
                                    left_on='writer_id', right_on='nconst')
matches_simplewriter1 = imdb_same_simple_title_writer.merge(not_matched, 
  left_on=['primaryTitle','primaryName'], right_on=['simple_title','writer1'])
matches_simplewriter2 = imdb_same_simple_title_writer.merge(not_matched, 
  left_on=['primaryTitle','primaryName'], right_on=['simple_title','writer2'])
matches_simplewriter3 = imdb_same_simple_title_writer.merge(not_matched, 
  left_on=['primaryTitle','primaryName'], right_on=['simple_title','writer3'])

not_matched = pd.concat([not_matched, matches_simplewriter1, 
                         more_matches_simplewriter1, matches_simplewriter2, 
                         matches_simplewriter2, matches_simplewriter3, 
                         matches_simplewriter3]).\
                 drop_duplicates('movie_id', keep=False)

DFS_TO_CONCAT = [matches_yearplus1, matches_yearminus1, matches_director1,
                 matches_director2, matches_director3, matches_writer1, 
                 matches_writer2, matches_writer3, matches_simpleyear, 
                 matches_simpleyearplus1, matches_simpleyearminus1, 
                 matches_simpledirector1, matches_simpledirector2, 
                 matches_simpledirector3, matches_simplewriter1, 
                 matches_simplewriter2, matches_simplewriter3]


def clean_and_concat(dfs_to_concat, old_merged_file):
    '''
    Remove unnecessary columns and concat all additional matches dataframes.
    Write updates matches csv file

    Inputs:
      dfs_to_concat: additional matches dataframes
      old_merged_file: matched csv file

    Returns: 
      new_merged: new matches between imdb and rt dataframes
    '''
    old_merged = pd.read_csv(old_merged_file)
    columns_needed = list(old_merged.columns)
    new_merged = old_merged
    for df in dfs_to_concat:
        if 'year' not in df.columns:
            df['theater_date'] = df['theater_date'].astype(str)
            df['year'] = df['theater_date'].str[-4:]
        df = df[columns_needed]
        df.columns = ['tconst', 'averageRating', 'numVotes', 'primaryTitle', 
                      'isAdult', 'startYear', 'runtimeMinutes', 'genres', 
                      'directors_y', 'writers', 'movie_id', 'title', 
                      'directors_x', 'genre', 'theater_date', 'stream_date', 
                      'box_office', 'mpaa', 'runtime', 'studio', 'writer', 
                      'full_synop', 'all_reviewers_average', 
                      'num_all_reviewers', 'num_all_fresh', 'num_all_rotten', 
                      'top_reviewers_average','num_top_reviewers', 
                      'num_top_fresh', 'num_top_rotten', 'user_rating',
                      'num_users', 'year']
        new_merged = pd.concat([new_merged, df], sort=False)
    new_merged = new_merged.drop_duplicates('movie_id')
    new_merged.to_csv('fixed_8709_merged.csv', index = False)
    return new_merged

