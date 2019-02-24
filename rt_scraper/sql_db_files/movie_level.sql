CREATE TABLE movie_page (
    movie_id int PRIMARY KEY,
    title VARCHAR(255),
    genre VARCHAR(1024),
    theater_date VARCHAR(64),
    stream_date VARCHAR(64),
    mpaa VARCHAR(1024),
    runtime int,
    studio VARCHAR(1024),
    writer VARCHAR(1024),
    full_synop VARCHAR(2048),
    all_reviewers_average VARCHAR(32),
    num_all_reviewers int,
    num_all_fresh int,
    num_all_rotten int,
    top_reviewers_average VARCHAR(32),
    num_top_reviewers int,
    num_top_fresh int,
    num_top_rotten  int,
    user_rating int,
    num_users int
    );

.import movie_level.csv movie_page