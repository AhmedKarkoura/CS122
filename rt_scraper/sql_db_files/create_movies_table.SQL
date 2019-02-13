CREATE TABLE all_movies_page (
    movie_id int PRIMARY KEY,
    top_actors VARCHAR(1024),
    h_runtime VARCHAR(32),
    short_syn VARCHAR(1024),
    title VARCHAR(255),
    url VARCHAR(512)
    );

.import all_movies_page.csv all_movies_page