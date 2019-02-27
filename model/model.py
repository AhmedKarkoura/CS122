### ML MODEL ATTEMPT ###
### BIG SCREEN ###

import pandas as pd 
import numpy as np
import os
import csv

from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

import pydotplus
from sklearn.externals.six import StringIO  
from IPython.display import Image  
from sklearn.tree import export_graphviz


def setup():
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
    matches = imdb.merge(rt, left_on='primaryTitle', right_on='title')
    matches = matches.replace('\\N', '')

    matches = matches.replace([np.nan, 'nan', 'NaN'], -1)
    matches.user_rating = matches.user_rating.astype(str)
    matches.user_rating = matches.user_rating.apply(lambda x: x.split('/')[0])

    matches = matches.drop(['startYear', 'endYear', 'runtimeMinutes', 'stream_date',
        'writers', 'full_synop', 'num_all_fresh', 'num_all_rotten', 'num_top_fresh',
        'num_top_rotten', 'titleType', 'genre', 'originalTitle', 'primaryTitle',
        'mpaa', 'writer', 'directors_x', 'user_rating', 'num_users',
        'num_top_reviewers', 'num_all_reviewers', 'tconst', 'movie_id', 'title', 'year',
        'numVotes', 'top_reviewers_average', 'theater_date'], axis = 1)

    # matches.theater_date = matches.theater_date.astype(str).apply(lambda x: x[-4:]).astype(int)

    for i in range(3):
        matches['genre' + str(i)] = matches.genres.apply(lambda x: split_field(x, i))

    matches.drop('genres', axis = 1)

    for i in range(2):
        matches['directors' + str(i)] = matches.directors_y.astype(str).apply(lambda x: split_field(x, i))

    ## STILL NEED TO DO THE SAME FOR ACTORS, mpaa?

    matches = matches.drop(['genres', 'directors_y'], axis = 1)
    matches.box_office = matches.box_office.astype(str).apply(lambda x: x.replace('$', '').replace(',', '')).astype(int)

    cat_cols = ['genre0', 'genre1', 'genre2', 'directors0', 'directors1', 'studio', 
        'averageRating', 'all_reviewers_average']
    
    for col in cat_cols:
        matches[col] = matches[col].astype(str)
        le = preprocessing.LabelEncoder()
        le.fit(matches[col])
        matches[col] = le.transform(matches[col])

    return matches

def split_field(l, i):
    l = l.split(',')
    try:
        val = l[i]
    except Exception as e:
        val = ''

    return val

def classifications():
    matches = setup()
    ys = ['box_office', 'averageRating', 'all_reviewers_average']
    for prediction in ys:
        print(prediction)

        X_train, X_test, y_train, y_test = train_test_split(matches.drop(ys, axis = 1), 
            matches[prediction], random_state = 42)

        dt = DecisionTreeClassifier()
        dt.fit(X_train, y_train)
        y_pred = dt.predict(X_test)
        print('DTC R2: ', r2_score(y_test, y_pred))
        print('DTC SCORE: ', dt.score(X_test, y_test))
        print()

        # dot_data = StringIO()
        # export_graphviz(dt, out_file=dot_data,  
        #                 filled=True, rounded=True,
        #                 special_characters=True)
        # graph = pydotplus.graph_from_dot_data(dot_data.getvalue())  
        # Image(graph.create_png())
        # print()
        # print()

        # rf = RandomForestClassifier(n_estimators = 100)
        # rf.fit(X_train, y_train)
        # # y_pred = rf.predict(X_test)
        # # rf_auc = roc_auc_score(y_test, y_pred)
        # # print('RFC AUC: ', rf_auc)
        # print('RFC SCORE: ', rf.score(X_test, y_test))

        # reg = LinearRegression()
        # reg.fit(X_train, y_train)
        # # y_pred = reg.predict(X_test)
        # # reg_auc = roc_auc_score(y_test, y_pred)
        # # print('LinReg AUC: ', reg_auc)
        # print('LinReg SCORE: ', reg.score(X_test, y_test))

        # nb = GaussianNB()
        # nb.fit(X_train, y_train)
        # # y_pred = nb.predict(X_test)
        # # nb_auc = roc_auc_score(y_test, y_pred)
        # # print('NB AUC: ', nb_auc)
        # print('NB SCORE: ', nb.score(X_test, y_test))
        # print()










