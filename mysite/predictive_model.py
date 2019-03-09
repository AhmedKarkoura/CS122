### ML MODEL ATTEMPT ###
### BIG SCREEN ###

import pandas as pd 
import numpy as np
import os
import csv
import sqlite3
from fuzzywuzzy import fuzz

from sklearn import preprocessing
from sklearn.model_selection import train_test_split
#from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
#from sklearn.linear_model import LinearRegression
#from sklearn.metrics import r2_score, roc_auc_score

def setup():
    matches = pd.read_csv('../sql_filter/old_csvs/database.csv')

    matches = matches.replace('\\N', '')
    matches = matches.replace([np.nan, 'nan', 'NaN'], -1)
    matches.director1 = matches.director1.replace(-1, '')
    matches.director2 = matches.director2.replace(-1, '')

    matches = matches.drop(['short_synopsis', 'url', 'poster_url', 'movie_id',
        'title', 'full_synopsis', 'critics_score', 'audience_score', 'year',
        'genre2', 'genre3', 'oscars_nomination_count', 'imdb_score',
        'writer1', 'writer2', 'writer3'], 
        axis = 1)

    for i in range(3):
        matches['actor' + str(i+1)] = matches.top3actors.apply(lambda x: split_field(x, i, '/'))

    matches = matches.drop(['top3actors'], axis = 1)
    matches.box_office = matches.box_office.astype(str).apply(lambda x: x.replace('$', '').replace(',', '')).astype(int)

    person_cols = ['actor1', 'actor2', 'actor3','director1', 'director2']
    other_cat_cols = ['mpaa', 'studio', 'genre1']

    labelers = {}
    for col in matches.columns:
        if col not in ['runtime', 'box_office']:
            matches[col] = matches[col].astype(str)

    person_le = preprocessing.LabelEncoder()
    person_le.fit(pd.concat([matches[col] for col in person_cols]))
    
    for col in person_cols:
        matches[col] = person_le.transform(matches[col])
        labelers[col] = person_le

    for col in other_cat_cols:
        le = preprocessing.LabelEncoder()
        matches[col] = le.fit_transform(matches[col])
        labelers[col] = le

    reg = DecisionTreeRegressor()
    reg.fit(matches.drop('box_office', axis = 1), matches.box_office)

    return matches, labelers, reg

def split_field(l, i, splitter):
    try:
        l = l.split(splitter)
        val = l[i]
    except Exception as e:
        val = ''

    return val

def classify(ui_dict):
    matches, labelers, reg = setup()

    for i in range(3):
        ui_dict['actor' + str(i + 1)] = split_field(ui_dict.get('actor'), 
            i, ', ')

    for i in range(2):
        ui_dict['director' + str(i + 1)] = split_field(ui_dict.get('director'), 
            i, ', ')

    ui_dict['genre1'] = ui_dict.get('genre')

    cols = ['mpaa', 'runtime', 'studio', 'genre1', 'director1', 'director2',
        'actor1', 'actor2', 'actor3']

    row = [ui_dict.get(col) for col in cols]
    row = ensure_accuracy(row)
    print(row)

    for i, val in enumerate(row):
        if i != 1:
            encoder = labelers.get(cols[i])
            row[i] = encoder.transform([val])[0]

    X_test = pd.DataFrame([row], columns = cols)
    prediction = reg.predict(X_test)[0]

    if prediction == -1:
        prediction = np.mean(matches.box_office[matches.box_office != -1])

    return '${:,.2f}'.format(prediction)

def ensure_accuracy(row):
    check_row = row[4:]

    connection = sqlite3.connect('final_complete.db')
    connection.create_function("fuzz", 2, fuzz.ratio)
    c = connection.cursor()

    for i, item in enumerate(check_row):
        s = 'SELECT name, fuzz(name, ?) as f from names ORDER BY f DESC LIMIT 1'

        if item != -1 and item != '':
            r = c.execute(s, (item,))
            check_row[i] = r.fetchall()[0][0]

    row[4:] = check_row

    return row

### NO LONGER NECESSARY###
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