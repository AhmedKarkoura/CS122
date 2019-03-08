# import json
# from django.shortcuts import HttpResponse
 
# def myView(request):

#     my_dict = {}
#     my_dict['Movie Recommendation'] = 'http://127.0.0.1:8000/movie_recommendation'
#     my_dict['Executive Modeling'] = 'http://127.0.0.1:8000/model'
#     return HttpResponse(json.dumps([my_dict]),content_type="application/json")

from django.shortcuts import render
 
def myView(request):
    
    context = {}
    context['Movie Recommendation'] = 'http://127.0.0.1:8000/movie_recommendation'
    context['Executive Modeling'] = 'http://127.0.0.1:8000/model'
    return render(request, 'homepage/index.html', context)
