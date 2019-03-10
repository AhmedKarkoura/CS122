from django.shortcuts import render
from django.http import HttpResponse
from functools import reduce
from operator import and_
from django import forms
from filter import find_movies
import json
import traceback
import sys
import csv
import os


NOPREF_STR = 'No preference'

COLUMN_NAMES = dict(
    genre='Genre',
    actor='Actor/Actress',
    director='Director',
    studio='Studio',
    rating='Rating',
    runtime='Runtime')

genres_lst = ['', 'Action & Adventure', 'Classics', 'Art House & International', 'Drama',
'Musical & Performing Arts', 'Animation', 'Comedy', 'Western',
'Documentary', 'Horror', 'Mystery & Suspense', 'Cult Movies', 'Kids & Family',
'Science Fiction & Fantasy', 'Romance', 'Sports & Fitness', 'Special Interest',
'Gay & Lesbian', 'Television', 'Faith & Spirituality', 'Anime & Manga']
ratings_lst = ['', 'NR', 'PG-13', 'PG', 'G', 'R', 'NC17']
studios_lst = ['','IFC Films','Warner Bros. Pictures','Universal Pictures',
'20th Century Fox','Magnolia Pictures','Sony Pictures Classics',
'Paramount Pictures','Sony Pictures','Netflix','Focus Features',
'Warner Home Video','Walt Disney Pictures','MGM' ,'MGM Home Entertainment'
,'Lionsgate Films','Lionsgate','Roadside Attractions','Samuel Goldwyn Films'
,'WARNER BROTHERS PICTURES','First Run Features','The Weinstein Company'
,'Freestyle Releasing','Gravitas Ventures','Anchor Bay Entertainment'
,'Fox Searchlight Pictures','New Line Cinema','Strand Releasing'
,'Warner Bros.']
order_by_lst = ['','oscars_nominations', 'critics_score', 'audience_score',
 'box_office']


def _build_dropdown(options):
    """Convert a list to (value, caption) tuples."""
    return [(x, x) if x is not None else ('', NOPREF_STR) for x in options]

def _valid_result(res):
    """Validate results returned by find_movies."""
    (header, results) = [0, 1]
    n = len(res[header])
    if not (isinstance(res, (tuple, list)) and
          len(res) == 2 and
          isinstance(res[header], (tuple, list)) and
          isinstance(res[results], (tuple, list))):
        return False
    def _valid_row(row):
        return isinstance(row, (tuple, list)) and len(row) == n
    return reduce(and_, (_valid_row(x) for x in res[results]), True)

GENRES = _build_dropdown(genres_lst)
RATINGS = _build_dropdown(ratings_lst)
STUDIOS = _build_dropdown(studios_lst)
ORDER = _build_dropdown(order_by_lst)


class SearchForm(forms.Form):

    genre = forms.ChoiceField(label='Genre', choices=GENRES, required=False)
    actor = forms.CharField(label='Actor/Actress', required = False)
    director = forms.CharField(label='Director', required=False)
    studio = forms.ChoiceField(label='Studio', choices=STUDIOS, required=False)
    rating = forms.ChoiceField(label='MPAA Rating', choices=RATINGS, required=False)
    runtime = forms.IntegerField(label='Runtime', required=False)
    order_by = forms.ChoiceField(label='Order By', choices=ORDER, required=False)
    #ADD help_text about the order_by oscars


def home(request):
    context = {}
    res = None

    #cretaing a form and populating it with data after the request is filled
    if request.method != 'GET':
        form = SearchForm()
    if request.method == 'GET':
        form = SearchForm(request.GET)

        if form.is_valid():
            args = {}
            genre = form.cleaned_data['genre']
            actor = form.cleaned_data['actor']
            director = form.cleaned_data['director']
            studio =  form.cleaned_data['studio']
            rating = form.cleaned_data['rating']
            runtime = form.cleaned_data['runtime'] 
            order_by = form.cleaned_data['order_by']

            if genre:
                args['genre'] = genre

            if actor:
                args['actor'] = actor

            if director:
                args['director'] = director

            if studio:
                args['studio'] = studio

            if rating:
                args['mpaa'] = rating

            if runtime:
                args['runtime'] = runtime

            if order_by:
                args['order_by'] = order_by

            try:
                res = find_movies(args)
            except Exception as e:
                print('Exception caught')
                if args.get('order_by'):
                    res = None

                else:
                    res = 'Please fill the order by field'

    if res is None:
        context['result'] = None
    
    elif isinstance(res, str):
        context['result'] = None
        context['err'] = res
        result = None

    elif not _valid_result(res):
        context['result'] = None
        context['err'] = ('Format of the return of find_movies is incorrect')

    else:
        columns, result = res
       
        #if args['order_by'] == 'oscars_nominations':
        columns = ['Title', 'Genre 1', 'Genre 2', 'Genre 3', 'Director',' Writer',
        'Top 3 Actors', 'Critics Score (/10)', "Audience Score (/5)", 'Box Office', 
        'Short Synopsis', 'Runtime', 'MPAA Rating','Oscar Nominations',
        'Movie Poster', 'Actor Poster', 'Director Poster']
            
        # else:
        #     columns = ['Title', 'Genre 1', 'Genre 2', 'Genre 3', 'Director',' Writer',
        #     'Top 3 Actors', 'Critics Score (/10)', "Audience Score (/5)", 'Box Office', 
        #     'Short Synopsis', 'Runtime', 'MPAA Rating',
        #     'Movie Poster', 'Actor Poster', 'Director Poster']

        context['result'] = result
        context['num_results'] = len(result)
        context['columns'] = [COLUMN_NAMES.get(col, col) for col in columns]

    context['form'] = form
    return render(request, 'polls/index.html', context)
   


