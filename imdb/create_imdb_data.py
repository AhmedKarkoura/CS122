import pandas as pd
import numpy as np

#Importing large TSVs as pandas dataframe (One at once because they
#are very large and would always kill the python terminal)
principals = pd.read_csv('principals.tsv', sep='\t', low_memory=False) 
titles = pd.read_csv('titles.tsv', sep='\t', low_memory=False)
crew = pd.read_csv('crew.tsv', sep='\t') 
akas = pd.read_csv('akas.tsv', sep='\t', low_memory=False)
ratings = pd.read_csv('ratings.tsv', sep='\t', low_memory=False) 

#Create imdb_full of movies and videos (no other filters)
titles_ratings = ratings.merge(titles, left_on='tconst', right_on='tconst')
full_ratings = titles_ratings.merge(crew, left_on='tconst', right_on='tconst')
full_ratings = final_ratings.drop(columns=['endYear','originalTitle'])
df1 = full_ratings[full_ratings['titleType'] == 'movie']
df2 = full_ratings[full_ratings['titleType'] == 'video']
imdb_full = pd.concat([df1,df2]).drop_duplicates().reset_index(drop=True0
imdb_full.to_csv('imdb_full.csv', encoding='utf-8',  index=False)

# Creating final_names of crew in movies in full_ratings_en
principals = pd.read_csv('principals.tsv', sep='\t', low_memory=False) 
principals = principals.drop(columns=['ordering', 'job', 'characters'])
principals = principals[principals['tconst'].isin(imdb_full['tconst'])]
principals.to_csv('final_principals.csv', encoding='utf-8',  index=False)

names = pd.read_csv('name_basics.tsv', sep='\t', low_memory=False)
names = names[names['nconst'].isin(principals['nconst'])]
names = names.drop(columns=['birthYear', 'deathYear'])
names.to_csv('final_names.csv', encoding='utf-8',  index=False)


#Creating final_ratings_en (only entries with the language EN but not used after all
#because we have realized that a lot of english movies were not labelled with 
#the EN language)
akas_en =  akas[akas['language'] == 'en']
ratings_en = ratings[ratings['tconst'].isin(akas_en['titleId'])]
titles_ratings_en = ratings_en.merge(titles, left_on='tconst', right_on='tconst')
full_ratings_en = titles_ratings_en.merge(crew, left_on='tconst', right_on='tconst')
full_ratings_en = full_ratings_en.drop(columns=['endYear','originalTitle'])
df1 = full_ratings_en[full_ratings_en['titleType'] == 'movie']
df2 = full_ratings_en[full_ratings_en['titleType'] == 'video']
full_ratings_en = pd.concat([df1,df2]).drop_duplicates().reset_index(drop=True)
full_ratings_en = full_ratings_en.drop(columns=['endYear','originalTitle'])
full_ratings_en.to_csv('full_ratings_en.csv', encoding='utf-8',  index=False)




