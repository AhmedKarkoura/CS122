import pandas as pd
import numpy as np

#Now getting principals database
df = pd.read_csv('principals.tsv', sep='\t', low_memory=False) 
df2 = pd.read_csv('data.csv') #(where data.csv has all tconst of movies, excluding series/shows.videos)
df3 = df[df['tconst'].isin(df2['tconst'])] #(want to save this as csv)
df3 = df3.drop(columns=['ordering', 'job', 'characters'])
df3.to_csv('principals.csv', encoding='utf-8',  index=False)  
df3 = df3.sort_values(by='nconst')   

df4 = pd.read_csv('name_basics.tsv', sep='\t') 
df5 = df4[df4['nconst'].isin(df3['nconst'])] #want to save this as csv
df5.to_csv('names', encoding='utf-8',  index=False)

###############################

#To make a databse of just English movies

titles = pd.read_csv('titles.tsv', sep='\t', low_memory=False)
crew = pd.read_csv('crew.tsv', sep='\t') 
#akas = pd.read_csv('akas.tsv', sep='\t', low_memory=False)
ratings = pd.read_csv('ratings.tsv', sep='\t', low_memory=False) 

akas_en =  akas[akas['language'] == 'en']
ratings_en = ratings[ratings['tconst'].isin(akas_en['titleId'])]

titles_ratings = ratings_en.merge(titles, left_on='tconst', right_on='tconst')
df1 = titles_ratings[titles_ratings['titleType'] == 'movie']
df2 = titles_ratings[titles_ratings['titleType'] == 'video']
titles_filtered = pd.concat([df1,df2]).drop_duplicates().reset_index(drop=True)
final_ratings = titles_filtered.merge(crew, left_on='tconst', right_on='tconst')
final_ratings = final_ratings.drop(columns=['endYear','originalTitle'])
final_ratings.to_csv('final_ratings.csv', encoding='utf-8',  index=False)

##################################

principals = pd.read_csv('principals.tsv', sep='\t', low_memory=False) 
principals = principals.drop(columns=['ordering', 'job', 'characters'])
principals = principals[principals['tconst'].isin(final_ratings['tconst'])]
principals.to_csv('final_principals.csv', encoding='utf-8',  index=False)

names = pd.read_csv('name_basics.tsv', sep='\t', low_memory=False)
names = names[names['nconst'].isin(principals['nconst'])]
names = names.drop(columns=['birthYear', 'deathYear'])
names.to_csv('final_names.csv', encoding='utf-8',  index=False)






df1 = full_ratings[full_ratings['titleType'] == 'movie']
df2 = full_ratings[full_ratings['titleType'] == 'video']
titles_filtered = pd.concat([df1,df2]).drop_duplicates().reset_index(drop=True0
titles_filtered.to_csv('imdb_full.csv', encoding='utf-8',  index=False)






