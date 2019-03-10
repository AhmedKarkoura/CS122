'''
Find Movies SQL Filter for Project Big Screen
'''
import sqlite3
from fuzzywuzzy import fuzz
import actor_director_posters as adp

HEADERS = ['title', 'genre1', 'director1','top3actors',
           'critics_score', 'audience_score', 'box_office', 
           'runtime', 'mpaa', 'oscar_nomination_count', 
           'poster_url', 'actor_pic_url', 'director_pic_url']

SELECT = ["ratings.title", "ratings.genre1", 
          "ratings.director1", 
          "format_top3actors(ratings.top3actors)", 
          "ratings.critics_score", "ratings.audience_score", 
          "format_box_office(ratings.box_office)", 
          "ratings.runtime||' minutes'", "ratings.mpaa", 
          "ratings.oscar_nomination_count||' nominations'", 
          "ratings.poster_url", "ratings.url"]

FROM = ['ratings', 'principal', 'names']

ON = ['ratings.movie_id = principal.movie_id', 
      'principal.name_id = names.name_id']

WHERE_DICT = {
    "genre": "(ratings.genre1 == ? OR ratings.genre2 == ?" + \
             " OR ratings.genre3 == ?)",
    "actor": "(fuzz(names.name, ?) >= 80 and" + \
             " (principal.category == 'actor'" + \
             " OR principal.category == 'actress'))",
    "director": "(fuzz(ratings.director1, ?) >= 80" + \
                " OR fuzz(ratings.director2, ?) >= 80)",
    "studio": "ratings.studio = ?",
    "rating": "ratings.mpaa = ?",
    "runtime": "ratings.runtime <= ?"}

ORDERBY_DICT = {"oscars_nominations": "ratings.oscar_nomination_count DESC",
                "critics_score": "ratings.critics_score DESC",
                "audience_score": "ratings.audience_score DESC",
                "box_office": "ratings.box_office DESC"}

### USER DEFINED FUNCTIONS FOR SQL 

def format_genre(genre):
    '''
    Format genre selected 

    Input:
        genre: str selected from sql query

    Return: genre or "N/A" if no second or third genre
    '''
    if not genre:
        return "N/A"
    else: 
        return genre

def format_box_office(box_office):
    '''
    Format box office

    Input:
        box_office = int selected from sql query

    Return: string formatted as $ amount or Not Available
    '''
    if box_office == -1:
        return "Not Available"
    else: 
        return "$" + "{:,}".format(box_office)

def format_synop(short_synop):
    '''
    Format short synopsis (remove html tags)

    Input:
        short_synop: str selected from sql query
    Return: string with html tags removed
    '''
    for replace in ['<em>', '</em>', '<i>', '</i>']:
        short_synop = short_synop.replace(replace, '')

    return short_synop

def format_top3actors(top3actors):
    '''
    Format_top 3 actors

    Input: 
        top3actors: str selected from sql query
    Return: string with comma replacing forward slash
    '''
    top3actors = top3actors.split('/') 
    return ', '.join(top3actors)


def find_movies(ui_dict):
    '''
    Finds movies that satisfy given criteria from ui_dict
    Inputs: 
        Key, value pairs in ui_dict:
            genre = string
            actor/actress = string
            director = string
            studio = string
            rating = string
            runtime <= int
            order by = ['oscar_winners', 'critics_score', 'audience_score', 
            'box_office']

    Return: 
        list of headers and list containing query results
    '''

    if not ui_dict:
        return ([], [])

    else:
        connection = sqlite3.connect('final_database.db')
        c = connection.cursor()
        connection.create_function("fuzz", 2, fuzz.ratio)
        connection.create_function("format_box_office", 1, format_box_office)
        connection.create_function("format_top3actors", 1, format_top3actors)
        connection.create_function("format_genre", 1, format_genre)
        connection.create_function("format_synop", 1, format_synop)
        params = get_where_params(ui_dict)[1]
        query = get_query(ui_dict)
        r = c.execute(query, params)
        movies = r.fetchall() 
        connection.close()
        if len(movies) == 0:
            return ([],[])
        else:
            final = []
            for movie in movies:
                url = movie[-1]
                movie = tuple(movie[:len(movie)-1])
                movie += adp.get_person_posters(url)
                final.append(movie)
            return (HEADERS, final)

def get_query(ui_dict):
    '''
    Takes a dictionary containing search criteria and returns an SQL query

    Input:
        ui_dict: dictionary containing search criteria

    Returns:
        query: string SQL query 
    '''

    QUERY = get_select(ui_dict) + get_from(ui_dict) + \
            get_where_params(ui_dict)[0] + get_orderby(ui_dict) + " LIMIT 10"

    return QUERY

def get_select(ui_dict):
    '''
    Takes a dictionary containing search criteria and returns select portion of 
    SQL query

    Input:
        ui_dict: dictionary containing search criteria

    Returns:
        query_SELECT: string for select portion of SQL query 
    '''

    query_SELECT = 'SELECT DISTINCT ' + ', '.join(SELECT)
    
    return query_SELECT


def get_from(ui_dict):
    '''
    Takes a dictionary containing search criteria and returns
    FROM and ON portion of SQL query, which indicates which tables 
    to JOIN and on what columns to join them. 

    Input:
        ui_dict: dictionary containing search criteria

    Returns:
        FROM and ON query: string containing FROM, JOIN and ON 
            portion of SQL query 
    '''

    query_FROM = " FROM " + ' JOIN '.join(FROM) + " ON " + ' AND '.join(ON)
    return query_FROM
    

def get_where_params(ui_dict):
    '''
    Takes a dictionary containing search criteria and returns
    WHERE portion of SQL query, as well as tuple of parameters 
    on which to execute the SQL query. 

    Input:
        ui_dict: dictionary containing search criteria

    Returns:
        WHERE query, params: string containing WHERE portion of SQL query,
          tuple containing parameters on which to execute query
    '''
    
    WHERE = []
    params = []

    for arg in ui_dict:
        if arg in WHERE_DICT:
            if arg in ['actor', 'director']:
                searches_where = []
                searches = ui_dict[arg].split(',')
                searches = [search.strip(' ') for search in searches]
                for search in searches:
                    searches_where.append(WHERE_DICT[arg])
                    if arg == 'director':
                        params += 2 * [search.title()]
                    else:
                        params.append(search.title())
                WHERE.append('(' + ' OR '.join(searches_where) + ')')
            else:
                if arg == 'genre':    
                    params += 3 * [ui_dict[arg][:]]
                else:
                    params.append(ui_dict[arg])
                WHERE.append(WHERE_DICT[arg])
    if WHERE:
        query_WHERE = " WHERE " + " AND ".join(WHERE)
    else:
        query_WHERE = ""

    return query_WHERE, params

def get_orderby(ui_dict):
    '''
    Takes a dictionary containing search criteria and returns order by portion 
    of SQL query

    Input:
        ui_dict: dictionary containing search criteria

    Returns:
        query_ORDERBY: string for orderby portion of SQL query 
    '''
    
    query_ORDERBY = " ORDER BY " + ORDERBY_DICT[ui_dict['order_by']]

    return query_ORDERBY

### TESTING DICTIONARIES

TEST_0 = {'actor': "emma stone",
          'order_by': 'oscars_nominations'}

TEST_1 = {'genre': 'Drama',
          'actor': 'Matt Damon',
          'studio': 'Universal',
          'runtime': 150,
          'rating': "PG-13",
          'order_by': 'audience_score'}

TEST_2 = {'actor': 'emma stone , matt damon',  
          'director': 'woody allen, damien chazelle',
          'order_by': 'box_office',
          'genre': 'Drama'}

TEST_3 = {'rating': "PG-13",
          'order_by': 'audience_score'}

