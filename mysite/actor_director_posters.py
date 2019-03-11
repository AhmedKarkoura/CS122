# Assume have movie_id for rotten tomatoes:
# - Go to actor posters table:
#     - If actor poster there, return url
#     - Else: Find photo of first person in the actors, and return that poster url, as well as saving it in the db


import sqlite3
import urllib.request
import bs4
import csv

def get_person_posters(movie_url):
    connection = sqlite3.connect('final_database.db')
    c = connection.cursor()

    s = 'SELECT actor_pic_url, director_pic_url, director1 FROM ratings WHERE url == "' + movie_url + '"'
    r = c.execute(s)

    actor_url, director_url, director = r.fetchall()[0]

    if not director_url:
        director_s = '''SELECT a.director_pic_url 
            FROM ratings AS a join ratings AS b
            WHERE b.director1 == "''' + director + '''" 
            AND a.director1 == b.director1
            AND a.url != b.url
            ORDER BY b.director_pic_url DESC
            LIMIT 1'''

        result = c.execute(director_s).fetchall()
        if result:
            director_url = result[0][0]

        else:
            director_url = ''

    if not actor_url or not director_url:
        if not director_url:
            actor_url, director_url = scrape(movie_url, True)

        else:
            actor_url, _ = scrape(movie_url)

        update_pics_query = "UPDATE ratings SET actor_pic_url = " + "'" + actor_url + "'" \
                           ", director_pic_url = " + "'" + director_url + "'" + \
                           ' WHERE ratings.url = ' + "'" + movie_url + "'"

        c.execute(update_pics_query)
        connection.commit()

    connection.close()

    return actor_url, director_url

def scrape(movie_url, director = False):
    r = urllib.request.urlopen('https://www.rottentomatoes.com' + movie_url)
    html = r.read()
    soup = bs4.BeautifulSoup(html, features = 'html5lib')
    try: 
        tag = soup.find('div', class_ = 'cast-item media inlineBlock')
        actor_url = tag.find('img')['data-src']

        if actor_url[0] == '/':
            actor_url = 'https://www.rottentomatoes.com' + actor_url
    except:
        actor_url = ''

    if director:
        for li in soup.find_all('li', 'meta-row clearfix'):
            label, actual = li.find_all('div')

            if label.text.strip() == 'Directed By:':
                break

        url = 'https://www.rottentomatoes.com/' + actual.find('a')['href']

        try:
            r = urllib.request.urlopen(url)
            html = r.read()
            soup = bs4.BeautifulSoup(html, features = 'html5lib')


            if soup.find('div', class_ = 'celebHeroImage'):
                director_url = soup.find('div', class_ = 'celebHeroImage')['style'][22:]
                director_url = director_url[:len(director_url) - 2]

            else:
                director_url = soup.find('img', class_ = 'posterImage js-lazyLoad').attrs['data-src']

            if director_url[0] == '/':
                director_url = 'https://www.rottentomatoes.com' + director_url

        except Exception as e:
            director_url = 'https://www.rottentomatoes.com/assets/pizza-pie/images/user_none.710c9ebd183.jpg'

    else:
        director_url = ''

    return actor_url, director_url


### IGNORE EVERYTHING BELOW THIS LINE ###
def get_picture_url(movie_url):
    actor_query = 'SELECT ratings.actor_pic_url FROM ratings WHERE ratings.url = ' + "'" + movie_url + "'"
    director_query = 'SELECT ratings.director_pic_url FROM ratings WHERE ratings.url = ' + "'" + movie_url + "'"

    connection = sqlite3.connect('final_complete.db')
    c = connection.cursor() 
    actor_r = c.execute(actor_query)
    director_r = c.execute(director_query)
    
    actor_pic_url = actor_r.fetchall()
    director_pic_url = director_r.fetchall()

    if not actor_pic_url or not director_pic_url:
        director_pic_url, actor_pic_url = scrape(movie_url)
        update_pics_query = "UPDATE ratings SET actor_pic_url = " + "'" + actor_pic_url + "'" \
                           ", director_pic_url = " + "'" + director_pic_url + "'" + \
                           ' WHERE ratings.url = ' + "'" + movie_url + "'"

        c.execute(update_pics_query)
        connection.commit()

    connection.close()

    return actor_pic_url, director_pic_url

def update_table():
    connection = sqlite3.connect('final_complete.db')
    c = connection.cursor()

    s = 'SELECT url FROM ratings'

    r = c.execute(s)
    urls = [tup[0] for tup in r.fetchall()][1:]

    with open('actor_director_urls.csv', 'w') as f:
        csvwriter = csv.writer(f, delimiter='|')
        
        for i, url in enumerate(urls):
            if url != '/m/the_amityville_murders':
                actor, director = scrape(url, True)
                csvwriter.writerow([url, director, actor])
                print(i, url[3:])
            

def run(director_name, top3actors, movie_url):
    # THIS WOULD BE EASIER WITH NAME_ID
    movie_url = 'https://www.rottentomatoes.com' + movie_url
    actor_name = top3actors.split('/')[0]
    connection = sqlite3.connect('final_complete.db')

    c = connection.cursor()
    actor_name = "'" + actor_name + "'"
    director_name = "'" + director_name + "'"

    s = 'SELECT names.picture_url FROM names WHERE name = '
    
    #actor_s = s + actor_name + ''' AND profession LIKE '%actor%' '''
    actor_s = s + actor_name
    director_s = s + director_name
    #director_s = s + director_name + ''' AND profession LIKE '%director%' '''


    actor_r = c.execute(actor_s)
    director_r = c.execute(director_s)

    actor_url = actor_r.fetchall()
    director_url = director_r.fetchall()

    if not actor_url and not director_url:
        director_url, actor_url = scrape(movie_url)

        s = 'UPDATE names SET names.picture_url = ' + actor_url
        #s += ' WHERE name = ' + actor_name + ''' AND profession LIKE '%actor%' '''
        s += ' WHERE names.name = ' + actor_name

        c.execute(s)

        s = 'UPDATE names SET names.picture_url = ' + director_url
        #s += ' WHERE name = ' + director_name + ''' AND profession LIKE '%director%' '''
        s += ' WHERE names.name = ' + director_name    
        c.execute(s)

    connection.close()

    return director_url, actor_url