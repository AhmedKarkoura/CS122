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
from sklearn.metrics import r2_score, roc_auc_score

import pydotplus
from sklearn.externals.six import StringIO  
from IPython.display import Image  
from sklearn.tree import export_graphviz


def setup():
    matches = pd.read_csv('../../sql_filter/merged_oscar_count.csv')

    matches = matches.replace('\\N', '')

    matches = matches.replace([np.nan, 'nan', 'NaN'], -1)
    matches.user_rating = matches.user_rating.astype(str)
    matches.user_rating = matches.user_rating.apply(lambda x: x.split('/')[0])

    matches = matches.drop(['startYear', 'runtimeMinutes', 'stream_date',
        'writers', 'full_synop', 'num_all_fresh', 'num_all_rotten', 'num_top_fresh',
        'num_top_rotten', 'genre', 'primaryTitle', 'writer', 'directors_x', 'user_rating', 'num_users',
        'num_top_reviewers', 'num_all_reviewers', 'tconst', 'movie_id', 'title', 'year',
        'numVotes', 'top_reviewers_average', 'theater_date', 'all_page_runtime', 'all_page_title',
        'all_page_title2', 'short_syn', 'poster_url', 'isAdult', 'other_awards_count',
        'acting_count', 'total_nomination_count', 'movie'], axis = 1)

    # matches.theater_date = matches.theater_date.astype(str).apply(lambda x: x[-4:]).astype(int)

    for i in range(3):
        matches['genre' + str(i)] = matches.genres.apply(lambda x: split_field(x, i, ','))

    for i in range(2):
        matches['director' + str(i)] = matches.directors_y.astype(str).apply(lambda x: split_field(x, i, ','))

    for i in range(3):
        matches['actor' + str(i)] = matches.top3actors.astype(str).apply(lambda x: split_field(x, i, '/'))
    ## STILL NEED TO DO THE SAME FOR ACTORS, mpaa?

    matches = matches.drop(['genres', 'directors_y', 'top3actors'], axis = 1)
    matches.box_office = matches.box_office.astype(str).apply(lambda x: x.replace('$', '').replace(',', '')).astype(int)

    matches['mpaa'] = matches.mpaa.astype(str).apply(lambda x: x.split(' (')[0])
    cat_cols = ['genre0', 'genre1', 'genre2', 'director0', 'director1', 'studio', 
        'averageRating', 'all_reviewers_average', 'actor0', 'actor1', 'actor2', 'mpaa']
    

    labelers = {}

    for col in cat_cols:
        matches[col] = matches[col].astype(str)
        le = preprocessing.LabelEncoder()
        le.fit(matches[col])
        matches[col] = le.transform(matches[col])

        labelers[col] = le

    ys = ['box_office', 'averageRating', 'all_reviewers_average']

    rf = RandomForestClassifier(n_estimators = 100)
    rf.fit(matches.drop(ys, axis = 1), matches.box_office)

    return matches, labelers, rf

def split_field(l, i, splitter):
    l = l.split(splitter)
    try:
        val = l[i]
    except Exception as e:
        val = ''

    return val

def classify(ui_dict):
    matches, labelers, rf = setup()

    for key, val in ui_dict.items():
        encoder = labelers.get(key)

        ui_dict[key] = encoder.transform(val)

    X_test = pd.DataFrame(ui_dict)

    return rf.predict(X_test)

def classifications():
    matches, labelers = setup()

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

        reg = LinearRegression()
        reg.fit(X_train, y_train)
        y_pred = reg.predict(X_test)
        print('LinReg R2: ', r2_score(y_test, y_pred))
        print('LinReg SCORE: ', reg.score(X_test, y_test))
        print()

        nb = GaussianNB()
        nb.fit(X_train, y_train)
        y_pred = nb.predict(X_test)
        print('NB R2: ', r2_score(y_test, y_pred))
        print('NB SCORE: ', nb.score(X_test, y_test))
        print()

        rf = RandomForestClassifier(n_estimators = 100)
        rf.fit(X_train, y_train)
        y_pred = rf.predict(X_test)
        print('RF R2: ', r2_score(y_test, y_pred))
        print('RF SCORE: ', rf.score(X_test, y_test))
        print()








