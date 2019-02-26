CREATE TABLE awards (
	year integer,
	category VARCHAR(100),
	winner boolean,
	entity VARCHAR(200));

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