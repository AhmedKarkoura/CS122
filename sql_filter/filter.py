import sqlite3

def find_movies(ui_dict):
    '''
    Inputs: 
        Key, value pairs in ui_dict:
            genre = string
            actor/actress = string
            director = string
            studio = string
            rating = string
            runtime <= int
            order by = ['oscar_winners', 'critics_score', 'audience_score', 'box_office']
    '''

    if not ui_dict:
        return ([], [])

    else:
        connection = sqlite3.connect(DATABASE_FILENAME)
        c = connection.cursor()
        params = get_where_params(ui_dict)[1]
        query = generate_query(ui_dict)
        r = c.execute(query, params)
        header = get_header(c)
        movies = r.fetchall() 
        connection.close()
        return header, movies

def get_query(ui_dict):
    QUERY = get_select(ui_dict) + get_from(ui_dict) + \
            get_where_params(ui_dict)[0] + get_orderby(ui_dict)

    return QUERY

def get_select(ui_dict):
    query_SELECT = "SELECT ratings.top_actors, ratings.all_reviewers_average, " +
                    "ratings.user_rating, ratings.box_office, " +  
                    "ratings.poster_url, ratings.short_syn, " + 
                    "ratings.runtime, oscars.category, " + 
                    "acting_nominees.category"
    return query_SELECT


def get_from(ui_dict):
    query_FROM = "FROM ratings JOIN principal JOIN names JOIN awards JOIN acting_nominees" +
           "ON ratings.tconst = principal.tconst AND principal.nconst = names.nconst " +
           "AND ratings.tconst = oscars.tconst AND principal.nconst = acting_nominees.nconst " +
           "AND principal.tconst = acting_nominees.tconst"

    return query_FROM

def get_where_params(ui_dict):
    WHERE_DICT = {"genre": "ratings.genre == ?",
                  "actor": "(names.primaryName == ? and (principal.category = actor or principal.category = actress))",
                  "director": "(names.primaryName == ? and principal.category = director)",
                  "studio": "studio = ?",
                  "rating": "rating = ?",
                  "runtime": "runtime <= ?"}
    WHERE = []
    params = []

    for arg in ui_dict:
        if arg in WHERE_DICT:
            WHERE.append(WHERE_DICT[arg])
            params.append(ui_dict[arg])

    query_WHERE = " WHERE " + " AND ".join(WHERE)

    return query_WHERE, PARAMS

def get_orderby(ui_dict):
    ORDERBY_DICT = {"oscar_winners": "",
                    "critics_score": "ratings.all_reviewers_average DESC",
                    "audience_score": "ratings.user_rating DESC",
                    "box_office": "ratings.box_office DESC"}
    
    query_ORDERBY = "ORDER BY " + ui_dict['order_by']

    return query_ORDERBY



