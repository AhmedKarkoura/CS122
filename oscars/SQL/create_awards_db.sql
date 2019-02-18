CREATE TABLE awards (
	year integer,
	category VARCHAR(100),
	winner boolean,
	entity VARCHAR(200));

.separator ,
.import oscars_awards.csv awards

