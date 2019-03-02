from django.shortcuts import render
from django.http import HttpResponse
import json
import traceback
import sys
import csv
import os

from functools import reduce
from operator import and_

from django.shortcuts import render
from django import forms
from filter import find_movies

# def index(request):
# 	return HttpResponse("Hello, world! You are at the polls index.")

#  Inputs: 
#         Key, value pairs in ui_dict:
#             genre = string
#             actor/actress = string
#             director = string
#             studio = string
#             rating = string
#             runtime <= int
#             order by = ['oscar_winners', 'critics_score', 'audience_score', 'box_office']

NOPREF_STR = 'No preference'
RES_DIR = os.path.join(os.path.dirname(__file__), '..', 'res')
COLUMN_NAMES = dict(
    genre='Genre',
    actor='Actor/Actress',
    director='Director',
    studio='Studio',
    rating='Rating',
    runtime='Runtime',
)

NOPREF_STR = 'No preference'

def _build_dropdown(options):
    """Convert a list to (value, caption) tuples."""
    return [(x, x) if x is not None else ('', NOPREF_STR) for x in options]

genres_lst = ['No preference', 'Action & Adventure', 'Classics', 'Art House & International', 'Drama',
'Musical & Performing Arts', 'Animation', 'Comedy', 'Western',
'Documentary', 'Horror', 'Mystery & Suspense', 'Cult Movies', 'Kids & Family',
'Science Fiction & Fantasy', 'Romance', 'Sports & Fitness', 'Special Interest',
'Gay & Lesbian', 'Television', 'Faith & Spirituality', 'Anime & Manga']
ratings_lst = ['No preference', 'NR', 'PG-13', 'PG', 'G', 'R', 'NC17']
studios_lst = ['No preference','IFC Films','Warner Bros. Pictures','Universal Pictures',
'20th Century Fox','Magnolia Pictures','Sony Pictures Classics',
'Paramount Pictures','Sony Pictures','Netflix','Focus Features',
'Warner Home Video','Walt Disney Pictures','MGM' ,'MGM Home Entertainment'
,'Lionsgate Films','Lionsgate','Roadside Attractions','Samuel Goldwyn Films'
,'WARNER BROTHERS PICTURES','First Run Features','The Weinstein Company'
,'Freestyle Releasing','Gravitas Ventures','Anchor Bay Entertainment'
,'Fox Searchlight Pictures','New Line Cinema','Strand Releasing'
,'Warner Bros.']

GENRES = _build_dropdown(genres_lst)
RATINGS = _build_dropdown(ratings_lst)
STUDIOS = _build_dropdown(studios_lst)
ORDER = _build_dropdown(['oscar_winners', 'critics_score', 'audience_score',
 'box_office'])

class SearchForm(forms.Form):


    genre = forms.ChoiceField(label='Genre', choices=GENRES, required=False)
    actor = forms.CharField(
        label='Actor/Actress',
        help_text='e.g. Johnny Depp or  e.g. Johnny Depp,Ben Affleck',
        required=False)
    director = forms.CharField(
        label='Director',
        help_text='e.g. Christopher Nolan or e.g. Christopher Nolan, Ron Howard',
        required=False)
    studio = forms.ChoiceField(label='Studio', choices=STUDIOS, required=False)
    rating = forms.ChoiceField(label='Rating', choices=RATINGS, required=False)

    runtime = forms.IntegerField(label='Runtime', 
        help_text='Maximum duration of movie in minutes',
        required=False)
    order_by = forms.ChoiceField(label='Order By', choices=ORDER, required=True)

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

            # Convert form data to an args dictionary for find_courses

            args = {}
            if form.cleaned_data['query']:
                args['terms'] = form.cleaned_data['query']
           

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
                args['rating'] = rating

            if runtime:
                args['runtime'] = runtime

            if order_by:
                args['order_by'] = order_by

            if form.cleaned_data['show_args']:
                context['args'] = 'args_to_ui = ' + json.dumps(args, indent=2)

            try:
                res = find_movies(args)
            except Exception as e:
                print('Exception caught')
                bt = traceback.format_exception(*sys.exc_info()[:3])
                context['err'] = """
                An exception was thrown in find_courses:
                <pre>{}
{}</pre>
                """.format(e, '\n'.join(bt))

                res = None
    else:
        form = SearchForm()

    # Handle different responses of res
    if res is None:
        context['result'] = None
    elif isinstance(res, str):
        context['result'] = None
        context['err'] = res
        result = None
    # elif not _valid_result(res):
    #     context['result'] = None
    #     context['err'] = ('Return of find_courses has the wrong data type. '
    #                       'Should be a tuple of length 4 with one string and '
    #                       'three lists.')
    else:
        columns, result = res

        # Wrap in tuple if result is not already
        if result and isinstance(result[0], str):
            result = [(r,) for r in result]

        context['result'] = result
        context['num_results'] = len(result)
        context['columns'] = [COLUMN_NAMES.get(col, col) for col in columns]

    context['form'] = form
    return render(request, 'polls/index.html', context)
