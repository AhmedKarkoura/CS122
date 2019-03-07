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
merged = merged[['movie_id','title' ,'directors_y', 'genre','theater_date','stream_date'                                                                 
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
