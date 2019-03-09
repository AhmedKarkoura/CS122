CREATE TABLE awards (
	year integer,
	category VARCHAR(100),
	winner boolean,
	movie VARCHAR(200));

.separator ,
.import oscars_awards.csv awards

CREATE TABLE acting_nominees(
	year integer,
	category VARCHAR(100),
	actor VARCHAR(100),
	winner boolean,
	movie VARCHAR(200));
.separator ,
.import acting_nominees.csv acting_nominees

CREATE TABLE ratings (
    top3actors VARCHAR(1024),
    short_synop VARCHAR (1024),
    url VARCHAR (1024),
    poster_url VARCHAR (1024),
    movie_id VARCHAR(50),
    imdb_score real,
    title VARCHAR(255),
    box_office int,
    mpaa VARCHAR(1024),
    runtime int,
    studio VARCHAR(1024),
    full_synop VARCHAR(2048),
    critics_score real,
    audience_score real,
    year int,
    genre1 VARCHAR(255),
    genre2 VARCHAR(255),
    genre3 VARCHAR(255),
    director1 VARCHAR(255),
    director2 VARCHAR(255),
    writer1 VARCHAR(255),
    writer2 VARCHAR(255),
    writer3 VARCHAR(255),
    oscar_nomination_count int
    );
.separator ,
.import ratings.csv ratings

CREATE TABLE principal (
	movie_id VARCHAR(50),
	name_id VARCHAR(50),
	category VARCHAR(255));
.separator ,
.import final_principals.csv principal

CREATE TABLE names (
	name_id VARCHAR(50),
	name VARCHAR(255),
	profession VARCHAR(255),
	known_for VARCHAR(1024));
.separator ,
.import final_names.csv names
