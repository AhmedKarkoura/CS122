from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('movie_recommendation/', include('polls.urls')),
    path('model/', include('model.urls')),
    path('', include('homepage.urls'))
]