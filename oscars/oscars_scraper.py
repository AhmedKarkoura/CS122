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
import urllib.request
import requests

CURR_CAT_URL = 'https://en.wikipedia.org/wiki/Academy_Awards#Current_categories'

def get_acting_nominees(current_category_url):
    '''
    Get nominees for all acting awards and write to csv (year, category, actor/
    actress, winner(bool), movie associated with nomination)

    Inputs:
        current_category_url: url for current categories
    '''
    nominees = []
    for url in get_category_urls(current_category_url)[2:6]:
        nominees += get_nominees(url) 
    write_csv(nominees)
    return nominees

def get_category_urls(current_category_url):
    '''
    From URL with current categories, get url for each category
    Input: 
        current_category_url: url for current categories 

    Return:
        list of urls with each url containing awards information for one 
        category
    '''
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html5lib")
    links = soup.find('div', 
                      class_= "div-col columns column-width").find_all('a')
    urls = []
    for link in links:
        category_relative_url = link['href']
        category_url = util.convert_if_relative_url(url, 
                                                    category_relative_url)
        urls.append(category_url)

    return urls

def get_nominees(acting_award_url):
    '''
    Given url for an acting category, get nomination information for each 
    nominee

    Inputs:
        acting_award_url: url for acting award category

    Return: 
        list of lists: list of nominees, each nominee being a list of year, 
        category, actor/actress, winner(bool), movie
    '''

    nominees = []
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html5lib")
    table = soup.find('table', class_='wikitable sortable')
    rows = table.find_all('tr')[1:]  
    award = ' '.join(url.split('_')[3:])

    for index, row in enumerate(rows):

        if not row.find_all('td', style= 
            "background-color:#CACCD0; font-weight:bold; padding-left:20%"):
            nomination_info = []

            if row.th:
                year = row.th.find_all('a')[0].text  
            nomination_info.append(year)
            nomination_info.append(award.upper())
            row_info = row.find_all('td')
            if row_info:
                actor = row_info[0].text.strip('\n')
                nomination_info.append(actor.strip('§^†*[]1234567890()'))

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
                
                if len(row_info) > 2:
                    movie = row_info[2].text.strip('\n')
                nomination_info.append(movie)

                nominees.append(nomination_info)

    return nominees

def write_csv(nominees):
    '''
    Write csv for nominees 

    Input:
        nominees: list of nominees, each nominee being a list of year, 
        category, actor/actress, winner(bool), movie
    '''
    with open('acting_awards.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['year', 'category', 'actor/actress','winner', 
                         'movie'])
        writer.writerows(nominees)