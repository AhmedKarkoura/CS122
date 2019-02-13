CREATE TABLE movie_level (
    movie_id int PRIMARY KEY,
    directors VARCHAR(1024),
    genres VARCHAR(255),
    theater_date VARCHAR(255),
    disc_date VARCHAR(255),
    mpaa_rating VARCHAR(512),
    m_runtime VARCHAR(50),
    studios VARCHAR(128),
    writers VARCHAR(1024),
    full_syn VARCHAR(2048)
    );

.import movie_level_data.csv movie_level