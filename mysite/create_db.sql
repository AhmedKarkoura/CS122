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
    movie_id VARCHAR(50),
    imdb_score int,
    title VARCHAR(255),
    box_office VARCHAR(50),
    mpaa VARCHAR(1024),
    runtime int,
    studio VARCHAR(1024),
    full_synop VARCHAR(2048),
    critics_score VARCHAR(32),
    audience_score int,
    year int,
    genre1 VARCHAR(255),
    genre2 VARCHAR(255),
    genre3 VARCHAR(255),
    director1 VARCHAR(255),
    director2 VARCHAR(255),
    writer1 VARCHAR(255),
    writer2 VARCHAR(255),
    writer3 VARCHAR(255)
    );
.separator ,
.import cleaned_matches.csv ratings

CREATE TABLE principal (
	movie_id VARCHAR(50),
	name_id VARCHAR(50),
	category VARCHAR(255));
.separator ,
.import updated_principals.csv principal

CREATE TABLE names (
	name_id VARCHAR(50),
	name VARCHAR(255),
	profession VARCHAR(255),
	known_for VARCHAR(1024));
.separator ,
.import updated_names.csv names