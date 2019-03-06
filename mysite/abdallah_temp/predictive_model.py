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

def setup():
    matches = pd.read_csv('../../sql_filter/database.csv')

    matches = matches.replace('\\N', '')
    matches = matches.replace([np.nan, 'nan', 'NaN'], -1)

    matches = matches.drop(['short_synopsis', 'url', 'poster_url', 'movie_id',
        'title', 'full_synopsis', 'critics_score', 'audience_score', 'year',
        'genre2', 'genre3', 'oscars_nomination_count', 'imdb_score',
        'writer1', 'writer2', 'writer3'], 
        axis = 1)

    for i in range(3):
        matches['actor' + str(i+1)] = matches.top3actors.apply(lambda x: split_field(x, i, '/'))

    matches = matches.drop(['top3actors'], axis = 1)
    matches.box_office = matches.box_office.astype(str).apply(lambda x: x.replace('$', '').replace(',', '')).astype(int)

    cat_cols = ['genre1', 'director1', 'director2', 'studio', 'actor1', 
        'actor2', 'actor3', 'mpaa']
    
    labelers = {}

    for col in cat_cols:
        matches[col] = matches[col].astype(str)
        le = preprocessing.LabelEncoder()
        le.fit(matches[col])
        matches[col] = le.transform(matches[col])

        labelers[col] = le

    print('done cleaning, now building RandomForestClassifier')
    rf = RandomForestClassifier(n_estimators = 50)
    rf.fit(matches.drop('box_office', axis = 1), matches.box_office)

    return matches, labelers, rf

def split_field(l, i, splitter):
    try:
        l = l.split(splitter)
        val = l[i]
    except Exception as e:
        val = ''

    return val

def classify(ui_dict):
    matches, labelers, rf = setup()

    for i in range(3):
        ui_dict['actor' + str(i)] = split_field(ui_dict.get('actor'), i, ',')

    for i in range(2):
        ui_dict['director' + str(i)] = split_field(ui_dict.get('director'), i, ',')




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


# args_to_ui = {
#   "genre": "Musical & Performing Arts",
#   "director": "Christopher Nolan",
#   "studio": "Walt Disney Pictures",
#   "order_by": "box_office",
#   "mpaa": "PG-13",
#   "runtime": 150,
#   "actor": "Johnny Depp"
# }






