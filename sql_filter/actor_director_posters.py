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
    # THIS WOULD BE EASIER WITH NAME_ID
    connection = sqlite3.connect('../../sql_filter/final_complete.db')

    c = connection.cursor()
    actor_name = "'" + actor_name + "'"
    director_name = "'" + director_name + "'"

    s = 'SELECT poster_url FROM names WHERE name = '
    
    actor_s = s + actor_name + ''' AND profession LIKE '%actor%' '''
    director_s = s + director_name + ''' AND profession LIKE '%director%' '''


    actor_r = c.execute(actor_s)
    director_r = c.execute(actor_s)

    actor_url = actor_r.fetchall()
    director_url = director_r.fetchall()

    if not actor_url and not director_url:
        director_url, actor_url = scrape(movie_url)

        s = 'UPDATE names SET poster_url = ' + actor_url
        s += ' WHERE name = ' + actor_name + ''' AND profession LIKE '%actor%' '''

        c.execute(s)

        s = 'UPDATE names SET poster_url = ' + director_url
        s += ' WHERE name = ' + director_name + ''' AND profession LIKE '%director%' '''

        c.execute(s)

    connection.close()

    return director_url, actor_url


def scrape(movie_url):
    r = urllib.request.urlopen(movie_url)
    html = r.read()
    soup = bs4.BeautifulSoup(html, features = 'html5lib')

    actor_url = soup.find_all('div', 
        class_ = 'cast-item media inlineBlock')[0].find('img')['data-src']

    for li in soup.find_all('li', 'meta-row clearfix'):
        label, actual = li.find_all('div')

        if label.text.strip() == 'Directed By:':
            break

    url = 'https://www.rottentomatoes.com/'
    url += actual.find('a')['href']

    r = urllib.request.urlopen(url)
    html = r.read()
    soup = bs4.BeautifulSoup(html, features = 'html5lib')

    director_url = soup.find('div', class_ = 'celebHeroImage')['style'][22:]
    director_url = director_url[:len(director_url) - 2]

    return director_url, actor_url




