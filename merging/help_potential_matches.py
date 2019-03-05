final_merged = pd.read_csv('final_merged.csv')

potential_matches = pd.read_csv('potential_matches.csv')

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
imdb_names = pd.read_csv('updated_names.csv')
#Look at the shapes of each. (BEST case scenrio: final_merged contains all of rt)

