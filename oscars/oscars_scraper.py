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


BEST_ACTOR_URL = 'https://en.wikipedia.org/wiki/Academy_Award_for_Best_Actor'
BEST_SUPPORTING_ACTOR_URL = 'https://en.wikipedia.org/wiki/Academy_Award_for_Best_Supporting_Actor'
BEST_ACTRESS_URL = 'https://en.wikipedia.org/wiki/Academy_Award_for_Best_Actress'
BEST_SUPPORTING_ACTRESS_URL = 'https://en.wikipedia.org/wiki/Academy_Award_for_Best_Supporting_Actress'

def get_winners(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html5lib")
    table = soup.find('table', class_='wikitable sortable')
    rows = table.find_all('tr')[1:]  
    nominees = []
    award = ' '.join(url.split('_')[3:])

    for index, row in enumerate(rows):

        if not row.find_all('td', style= "background-color:#CACCD0; font-weight:bold; padding-left:20%"):
            nomination_info = [award]

            if row.th:
                year = row.th.find_all('a')[0].text  
            nomination_info.append(year)
            row_info = row.find_all('td')
            if row_info:
                actor = row_info[0].text.strip('\n')
                nomination_info.append(actor.strip('§^†*[]1234567890()'))
                if len(row_info) > 2:
                    movie = row_info[2].text.strip('\n')
                nomination_info.append(movie)

                winner = False
                win_test = row_info[0].find_all('img')
                if len(win_test) > 0:
                    winner = True
                elif '§'in actor:
                    winner = True
                elif '^' in actor:
                    winner = True
                elif '†' in actor:
                    winner = True
                nomination_info.append(winner)
                nominees.append(nomination_info)

    return nominees

''' 

def get_winners():


    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
    
    data = {'__RequestVerificationToken': 'utBox4gcI4FksC98fTDpUNkdf_exGrnnRS4idAnCT5xFb2svLAaHYqn_q5CjrWkL9HR8I0qJlyGP308MnMz3ETCgOxQ1',
            'BasicSearchView_FilmTitle' : '', 
            'BasicSearchView_Nominee' : '', 
            'BasicSearchView_IsWinnersOnly' : 'false',
            'BasicSearchView_AwardShowNumberFrom' : '1',
            'BasicSearchView_AwardShowNumberTo' : '90',
            'BasicSearchView_Sort' : '3-Award Category-Chron',
            'search' : 'Basic',
            'AdvancedSearchView_SearchFieldFilters[0]_Index' : '1',
            'AdvancedSearchView_SearchFieldFilters[0]_Field.Id' : '0',
            'AdvancedSearchView_SearchFieldFilters[0]_FieldValues' : '', 
            'AdvancedSearchView_SearchFieldFilters[0]_FieldValues' : '',
            'AdvancedSearchView_SearchFieldFilters[0]_Condition' : '0',
            'AdvancedSearchView_SearchFieldFilters[0]_SearchType' : '0',
            'AdvancedSearchView_SearchFieldFilters[0]_IsExcluded' : 'false',
            'AdvancedSearchView_SearchFieldFilters[1]_Index' : '2',
            'AdvancedSearchView_SearchFieldFilters[1]_Field.Id' : '0',
            'AdvancedSearchView_SearchFieldFilters[1]_FieldValues' : '',
            'AdvancedSearchView_SearchFieldFilters[1]_FieldValues' : '', 
            'AdvancedSearchView_SearchFieldFilters[1]_Condition' : '0',
            'AdvancedSearchView_SearchFieldFilters[1]_SearchType' : '0',
            'AdvancedSearchView_SearchFieldFilters[1]_IsExcluded' : 'false',
            'AdvancedSearchView_SearchFieldFilters[2]_Index' : '3',
            'AdvancedSearchView_SearchFieldFilters[2]_Field.Id' : '0',
            'AdvancedSearchView_SearchFieldFilters[2]_FieldValues' : '',
            'AdvancedSearchView_SearchFieldFilters[2]_FieldValues' : '',
            'AdvancedSearchView_SearchFieldFilters[2]_SearchType' : '0',
            'AdvancedSearchView_SearchFieldFilters[2]_IsExcluded' : 'false',
            'AdvancedSearchView_IsWinnersOnly' : 'false',
            'AdvancedSearchView_AwardShowNumberFrom' : '0',
            'AdvancedSearchView_AwardShowNumberTo' : '0', 
            'AdvancedSearchView_IsWomenOnly' : 'false',
            'AdvancedSearchView_IsMenOnly' : 'false',
            'AdvancedSearchView_IsDebut' : 'false',
            'AdvancedSearchView_IsPosthumous' : 'false',
            'AdvancedSearchView_IsShort' : 'false',
            'AdvancedSearchView_IsFeature' : 'false',
            'AdvancedSearchView_IsForeignLanguage' : 'false',
            'AdvancedSearchView_Sort' : '3-Award Category-Chron'}

    starting_url = 'http://awardsdatabase.oscars.org/search/results'
    r = requests.post(url = starting_url, json = data, headers = headers)
    #c = r.content
    #soup = BeautifulSoup(c)
    #year_list = soup.find_all('div', class_="result-group-header")

    session = HTMLSession()
    request = urllib.request.urlopen(starting_url)
    html = request.read()
    soup = bs4.BeautifulSoup(html, "html5lib")
    year_list = soup.find_all('div', class_="result-group-header")

    year_list = soup.find_all('div', class_="award_result-chron result-group group-awardcategory-chron")
    for year_tag in year_list:
        year = year_tag.find_all('a', class_="nominations_link")
'''
