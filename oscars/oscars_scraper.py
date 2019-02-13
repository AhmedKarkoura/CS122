'''
Oscars Scraper for Project Big Screen
'''

import re
import util
from bs4 import BeautifulSoup
import queue
import json
import sys
import csv
import sqlite3
import urllib.request
import requests


def get_winners():

    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
    
    data = {'__RequestVerificationToken': 'utBox4gcI4FksC98fTDpUNkdf_exGrnnRS4idAnCT5xFb2svLAaHYqn_q5CjrWkL9HR8I0qJlyGP308MnMz3ETCgOxQ1',
            'BasicSearchView.FilmTitle' : '', 
            'BasicSearchView.Nominee' : '', 
            'BasicSearchView.IsWinnersOnly' : 'false',
            'BasicSearchView.AwardShowNumberFrom' : '1',
            'BasicSearchView.AwardShowNumberTo' : '90',
            'BasicSearchView.Sort' : '3-Award Category-Chron',
            'search' : 'Basic',
            'AdvancedSearchView.SearchFieldFilters[0].Index' : '1',
            'AdvancedSearchView.SearchFieldFilters[0].Field.Id' : '0',
            'AdvancedSearchView.SearchFieldFilters[0].FieldValues' : '', 
            'AdvancedSearchView.SearchFieldFilters[0].FieldValues' : '',
            'AdvancedSearchView.SearchFieldFilters[0].Condition' : '0',
            'AdvancedSearchView.SearchFieldFilters[0].SearchType' : '0',
            'AdvancedSearchView.SearchFieldFilters[0].IsExcluded' : 'false',
            'AdvancedSearchView.SearchFieldFilters[1].Index' : '2',
            'AdvancedSearchView.SearchFieldFilters[1].Field.Id' : '0',
            'AdvancedSearchView.SearchFieldFilters[1].FieldValues' : '',
            'AdvancedSearchView.SearchFieldFilters[1].FieldValues' : '', 
            'AdvancedSearchView.SearchFieldFilters[1].Condition' : '0',
            'AdvancedSearchView.SearchFieldFilters[1].SearchType' : '0',
            'AdvancedSearchView.SearchFieldFilters[1].IsExcluded' : 'false',
            'AdvancedSearchView.SearchFieldFilters[2].Index' : '3',
            'AdvancedSearchView.SearchFieldFilters[2].Field.Id' : '0',
            'AdvancedSearchView.SearchFieldFilters[2].FieldValues' : '',
            'AdvancedSearchView.SearchFieldFilters[2].FieldValues' : '',
            'AdvancedSearchView.SearchFieldFilters[2].SearchType' : '0',
            'AdvancedSearchView.SearchFieldFilters[2].IsExcluded' : 'false',
            'AdvancedSearchView.IsWinnersOnly' : 'false',
            'AdvancedSearchView.AwardShowNumberFrom' : '0',
            'AdvancedSearchView.AwardShowNumberTo' : '0', 
            'AdvancedSearchView.IsWomenOnly' : 'false',
            'AdvancedSearchView.IsMenOnly' : 'false',
            'AdvancedSearchView.IsDebut' : 'false',
            'AdvancedSearchView.IsPosthumous' : 'false',
            'AdvancedSearchView.IsShort' : 'false',
            'AdvancedSearchView.IsFeature' : 'false',
            'AdvancedSearchView.IsForeignLanguage' : 'false',
            'AdvancedSearchView.Sort' : '3-Award Category-Chron'}

    starting_url = 'http://awardsdatabase.oscars.org/search/results'
    r = requests.post(url = starting_url, data = data, headers = headers)
    #c = r.content
    #soup = BeautifulSoup(c)
    #year_list = soup.find_all('div', class_="result-group-header")
    '''
    session = HTMLSession()
    request = urllib.request.urlopen(starting_url)
    html = request.read()
    soup = bs4.BeautifulSoup(html, "html5lib")
    year_list = soup.find_all('div', class_="result-group-header")

    year_list = soup.find_all('div', class_="award_result-chron result-group group-awardcategory-chron")
    for year_tag in year_list:
        year = year_tag.find_all('a', class_="nominations_link")

    '''

    print(r.text)



