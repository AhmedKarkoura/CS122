import sqlite3

def find_movies(ui_dict):

	if not ui_dict:
        return ([], [])

    else:
        connection = sqlite3.connect(DATABASE_FILENAME)
        c = connection.cursor()
        params = get_where_params(args_from_ui)[1]
        query = generate_query(args_from_ui)
        r = c.execute(query, params)
        header = get_header(c)
        movies = r.fetchall() 
        connection.close()
        return header, movies

def get_query(ui_dict):
	return QUERY

def get_select(ui_dict):
	return SELECT

def get_from(ui_dict):
	return FROM

def get_where_params(ui_dict):
	return WHERE, PARAMS



