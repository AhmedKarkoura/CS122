import pandas as pd
import numpy as np

#create the needed dataframes
rt = pd.read_csv('../rt_scraper/sql_db_files/all_movies.csv', sep = "|", header = None)
rt.columns = columns = ['movie_id','title' ,'directors', 'genre','theater_date','stream_date',
'box_office','mpaa','runtime', 'studio','writer','full_synop',
'all_reviewers_average','num_all_reviewers',
'num_all_fresh','num_all_rotten','top_reviewers_average','num_top_reviewers',
'num_top_fresh','num_top_rotten','user_rating','num_users']
rt['theater_date'] = rt['theater_date'].astype(str)
rt['year'] = rt['theater_date'].apply(lambda x: x[-4:])

imdb = pd.read_csv('../imdb/imdb_full.csv', low_memory=False)
names = pd.read_csv('../imdb/final_names.csv', low_memory=False)
names_full = pd.read_csv('../imdb/name_basics.tsv', sep='\t', low_memory=False) 

imdb['primaryTitle'] = imdb['primaryTitle'].str.title()
rt['title'] = rt['title'].str.title()


#movie_imdb = imdb[imdb['titleType'] == 'movie']

#######################
#IMDB has a lot of duplicates--> Choose the movie with most votes therefore the most
#famous one

n_maxes = imdb.groupby(['primaryTitle']).numVotes.transform(max)
imdb_dup = imdb.loc[imdb.numVotes == n_maxes]
imdb_dup['primaryTitle'] = imdb_dup['primaryTitle'].str.title()

#rt[rt['title'].isin(imdb['primaryTitle'])].shape

merged_matched = imdb_dup.merge(rt, left_on='primaryTitle', right_on='title')
merged_matched[merged_matched['startYear'] == merged_matched['year']].shape
new_merge = merged_matched[merged_matched['startYear'] == merged_matched['year']]
#new_merge.to_csv('merged_matched.csv', encoding='utf-8',  index=False)


#Now I have a dataset of 5101 movies with identical year and name
#want to remove these movies from rt and imdb_dup and try again to find matches

unmatched_rt = rt[rt['movie_id'].isin(new_merge['movie_id'])==False]


# unmatched_imdb = imdb[imdb['tconst'].isin(new_merge['movie_id'])==False]

merged_unmatched = imdb.merge(unmatched_rt, left_on='primaryTitle', 
    right_on='title') #doing it again with non duplicates


# merged_unmatched.to_csv('merged_unmatched.csv', encoding='utf-8',  index=False)

matches_unmatched = merged_unmatched[merged_unmatched['startYear'] == merged_unmatched['year']]

total_matched = pd.concat([new_merge,matches_unmatched]).reset_index(drop=True)

total_matched.to_csv('5681_matches.csv', encoding='utf-8',  index=False)

imdb_names = imdb.merge(names, left_on='directors', right_on='nconst')
unmatched_rt_2 = rt[rt['movie_id'].isin(total_matched['movie_id'])==False]



















unmatched_rt_2 = rt[rt['movie_id'].isin(total_matched['movie_id'])==False]
unmatched_imdb_2 = imdb[imdb['tconst'].isin(total_matched['tconst'])==False]

another_merge = imdb_dup.merge(unmatched_rt_2, left_on='primaryTitle',right_on='title')
