from django.shortcuts import render
from django.http import HttpResponse
import json
import traceback
import sys
import csv
import os
from functools import reduce
from operator import and_
from django import forms
from predictive_model import setup, classify 

NOPREF_STR = 'No preference'

# COLUMN_NAMES = dict(
#     genre='Genre',
#     actor='Actor/Actress',
#     director='Director',
#     studio='Studio',
#     rating='Rating',
#     runtime='Runtime')
COLUMN_NAMES = ['Title', 'Genre 1', 'Genre 2', 'Genre 3', 'Director', 'Writer', ' Top 3 Actors'
        'Critics Score', "Audience Score", 'Box Office',  'Poster', 'Short Synopsis', 
        'Runtime', 'MPAA Rating']

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



GENRES = _build_dropdown(genres_lst)
RATINGS = _build_dropdown(ratings_lst)
STUDIOS = _build_dropdown(studios_lst)
ORDER = _build_dropdown(order_by_lst)

class SearchForm(forms.Form):

    genre = forms.ChoiceField(label='Genre', choices=GENRES, required=True)
    actor = forms.CharField(
        label='Actor/Actress',
        help_text='e.g. Johnny Depp or  e.g. Johnny Depp,Ben Affleck',
        required=True)
    director = forms.CharField(
        label='Director',
        help_text='e.g. Christopher Nolan or e.g. Christopher Nolan, Ron Howard',
        required=True)
    studio = forms.ChoiceField(label='Studio', choices=STUDIOS, required=True)
    rating = forms.ChoiceField(label='MPAA Rating', choices=RATINGS, required=True)

    runtime = forms.IntegerField(label='Runtime', 
        help_text='Maximum duration of movie in minutes',
        required=True)
    # order_by = forms.ChoiceField(label='Order By', choices=ORDER, required=True)
    #ADD help_text about the order_by oscars

    show_args = forms.BooleanField(label='Show args_to_ui',
                                   required=False)

def home(request):
    context = {}
    res = None
    if request.method == 'GET':
        # create a form instance and populate it with data from the request:
        form = SearchForm(request.GET)
        # check whether it's valid:
        if form.is_valid():


            args = {}
            if form.cleaned_data['genre']:
                args['genre'] = form.cleaned_data['genre']
           

            genre = form.cleaned_data['genre']
            actor = form.cleaned_data['actor']
            director = form.cleaned_data['director']
            studio =  form.cleaned_data['studio']
            rating = form.cleaned_data['rating']
            runtime = form.cleaned_data['runtime'] 
            # order_by = form.cleaned_data['order_by']

            # if genre:
            #     args['genre'] = genre

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

            # if order_by:
            #     args['order_by'] = order_by

            if form.cleaned_data['show_args']:
                context['args'] = 'args_to_ui = ' + json.dumps(args, indent=2)


            try:
                res = classify(args)
            except Exception as e:
                print('Exception caught')
    else:
        form = SearchForm()

    # Handle different responses of res
    # if res is None:
    #     context['result'] = None
    
    # elif isinstance(res, str):
    #     context['result'] = None
    #     context['err'] = res
    #     result = None

    # elif not _valid_result(res):
    #     context['result'] = None
    #     context['err'] = ('Return of find_movies has the wrong data type. '
    #                       'Should be a tuple of length 4 with one string and '
    #                       'three lists.')

    # else:
    #     columns, result = res
    #     columns = ['Title', 'Genre 1', 'Genre 2', 'Genre 3', 'Director', 'Writer', ' Top 3 Actors'
    #     'Critics Score', "Audience Score", 'Box Office',  'Poster', 'Short Synopsis', 
    #     'Runtime', 'MPAA Rating']

    #     # Wrap in tuple if result is not already
    #     if result and isinstance(result[0], str):
    #         result = [(r,) for r in result]

        # context['result'] = res
        # context['num_results'] = len(res)
        # context['columns'] = ['Title', 'Genre 1', 'Genre 2', 'Genre 3', 'Director', 'Writer', ' Top 3 Actors'
        # 'Critics Score', "Audience Score", 'Box Office',  'Poster', 'Short Synopsis', 
        # 'Runtime', 'MPAA Rating']

    #context['num_results'] = len(res)
    context['result'] = res
    context['form'] = form
    return render(request, 'model/index.html', context)
   

