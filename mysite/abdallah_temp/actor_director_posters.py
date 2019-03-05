# Assume have movie_id for rotten tomatoes:
# - Go to actor posters table:
#     - If actor poster there, return url
#     - Else: Find photo of first person in the actors, and return that poster url, as well as saving it in the db


'''
DID THIS TO DATABASE

ALTER TABLE names
ADD poster_url VARCHAR(1000);
'''
import sqlite3
import urllib.request
import bs4

def run(director_name, actor_name, movie_url):
    connection = sqlite3.connect('../../sql_filter/updated_complete.db')

    c = connection.cursor()

    s = 'SELECT poster_url FROM names WHERE person == '
    
    actor_s = s + actor_name + ''' AND profession LIKE '%actor%' '''
    director_s = s + director_name + ''' AND profession LIKE '%director%' '''


    actor_r = c.execute(actor_s)
    director_r = c.execute(actor_s)

    actor_url = actor_r.fetchall()
    director_url = director_r.fetchall()

    if not actor_url and not director_url:
        director_url, actor_url = scrape(movie_url)

        s = 'UPDATE table_name SET poster_url = ' + actor_url
        s += ' WHERE person == ' + actor_name ''' AND profession LIKE '%actor%' '''

        c.execute(s)

        s = 'UPDATE table_name SET poster_url = ' + director_url
        s += ' WHERE person == ' + director_name ''' AND profession LIKE '%director%' '''

        c.execute(s)

    connection.close()

    return director_url, actor_url


def scrape(movie_url):
    r = urllib.request.urlopen(url)
    html = r.read()
    soup = bs4.BeautifulSoup(html, features = 'html5lib')




    return director_url, actor_url

















