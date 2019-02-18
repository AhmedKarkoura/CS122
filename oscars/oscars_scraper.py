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

def get_category_urls(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html5lib")
    links = soup.find('div', class_= "div-col columns column-width").find_all('a')
    urls = []
    for link in links:
        category_relative_url = link['href']
        category_url = util.convert_if_relative_url(url, category_relative_url)
        urls.append(category_url)

    return urls

def get_acting_nominees(url):
    nominees = []
    for url in get_category_urls(url)[2:6]:
        nominees += get_nominees(url) 
    write_csv(nominees)
    return nominees

def get_nominees(url):
    nominees = []
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html5lib")
    table = soup.find('table', class_='wikitable sortable')
    rows = table.find_all('tr')[1:]  
    award = ' '.join(url.split('_')[3:])

    for index, row in enumerate(rows):

        if not row.find_all('td', style= "background-color:#CACCD0; font-weight:bold; padding-left:20%"):
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
    with open('acting_nominees.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['year', 'category', 'actor/actress','winner', 'movie'])
        writer.writerows(nominees)

def get_best_pic(url):
    nominees = []
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html5lib")
    tables = soup.find_all('table', class_='wikitable')
    for table in tables:
        rows = table.find_all('tr')[1:]
        for index, row in enumerate(rows):
            row_info = row.find_all('td')
    
    return tables