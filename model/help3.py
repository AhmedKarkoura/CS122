import pandas as pd
import numpy as np

rt = pd.read_csv('all_movies.csv', sep = "|", header = None)
rt.columns = columns = ['movie_id','title' ,'directors', 'genre','theater_date','stream_date',
'box_office','mpaa','runtime', 'studio','writer','full_synop',
'all_reviewers_average','num_all_reviewers',
'num_all_fresh','num_all_rotten','top_reviewers_average','num_top_reviewers',
'num_top_fresh','num_top_rotten','user_rating','num_users']
rt['theater_date'] = rt['theater_date'].astype(str)
rt['year'] = rt['theater_date'].apply(lambda x: x[-4:])

imdb = pd.read_csv('imdb_full.csv', low_memory=False)

#matches = imdb[imdb['primaryTitle'].isin(rt['title'])]

rt[rt['title'].isin(imdb['primaryTitle'])].shape

merged_matched = imdb.merge(rt, left_on='primaryTitle', right_on='title')
merged_matched[merged_matched['startYear'] == merged_matched['year']].shape


# merged_matched = imdb.merge(rt, left_on='primaryTitle', right_on='title') 
# new_df = pd.merge(rt, imdb,  how='left', left_on=['title','primaryTitle'], \
#     right_on = ['year','year'])

