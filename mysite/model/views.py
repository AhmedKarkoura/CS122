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



genres_lst = ['', 'Action & Adventure', 'Classics', 'Art House & International', 'Drama',
'Musical & Performing Arts', 'Animation', 'Comedy', 'Western',
'Documentary', 'Horror', 'Mystery & Suspense', 'Cult Movies', 'Kids & Family',
'Science Fiction & Fantasy', 'Romance']
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
    genre = forms.ChoiceField(label='Genre', choices=GENRES, required = False)
    actor = forms.CharField(label='Actor/Actress', required = False)
    director = forms.CharField(label='Director', required = False)
    studio = forms.ChoiceField(label='Studio', choices=STUDIOS, required = False)
    rating = forms.ChoiceField(label='MPAA Rating', choices=RATINGS, required = False)
    runtime = forms.IntegerField(label='Runtime', required = False)
    show_args = forms.BooleanField(label='Show args_to_ui',
                                   required=False)

def home(request):
    context = {}
    res = None
    
    #creating a form and populating it with data after the request is filled
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

            if form.cleaned_data['genre']:
                args['genre'] = form.cleaned_data['genre']

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

            if form.cleaned_data['show_args']:
                context['args'] = 'args_to_ui = ' + json.dumps(args, indent=2)

            try:
                res = classify(args)

            except Exception as e:
                if bool(args):
                    res = 'All fields are required'
                print('Exception caught')

   
    if res is None:
        context['result'] = None
    else:
        context['result'] = res

    
    context['form'] = form
    return render(request, 'model/index.html', context)
   

