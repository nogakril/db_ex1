create table Producer(
  producers VARCHAR(100) PRIMARY KEY
);

create table Award(
  award_type VARCHAR(100) PRIMARY KEY CHECK(award_type='Winner' or award_type='Nominee')
);

create table Film(
  film_id VARCHAR(100) PRIMARY KEY,
  film_name VARCHAR(100) NOT NULL,
  imdb_rating NUMERIC(2,1) CHECK(imdb_rating>=1 and imdb_rating<=10),
  imdb_votes INTEGER CHECK(imdb_votes>=0),
  movie_time INTEGER CHECK(movie_time>0),
  year_of_release INTEGER CHECK(oscar_year>=1927 and oscar_year<=2022),
  oscar_year INTEGER CHECK(oscar_year>=1927 and oscar_year<=2022),
  award_type VARCHAR(100),
  produers VARCHAR(100),
  FOREIGN KEY (award_type) REFERENCES Award(award_type),
  FOREIGN KEY (produers) REFERENCES Producer(producers)
);

create table Person(
  name VARCHAR(100) PRIMARY KEY
);

create table Actor(
  name VARCHAR(100) UNIQUE,
  FOREIGN KEY (name) REFERENCES Person(name) ON DELETE CASCADE
);

create table ActedIn(
  film_id VARCHAR(100),
  name VARCHAR(100),
  FOREIGN KEY (name) REFERENCES Actor(name) ON DELETE CASCADE,
  FOREIGN KEY (film_id) REFERENCES Film(film_id) ON DELETE CASCADE,
  UNIQUE(name, film_id)
);

create table Author(
  name VARCHAR(100) UNIQUE,
  FOREIGN KEY (name) REFERENCES Person(name) ON DELETE CASCADE
);

create table Wrote(
  film_id VARCHAR(100),
  name VARCHAR(100),
  FOREIGN KEY (name) REFERENCES Author(name) ON DELETE CASCADE,
  FOREIGN KEY (film_id) REFERENCES Film(film_id) ON DELETE CASCADE,
  UNIQUE(name, film_id)
);

create table Director(
  name VARCHAR(100) UNIQUE,
  FOREIGN KEY (name) REFERENCES Person(name) ON DELETE CASCADE
);

create table Directed(
  film_id VARCHAR(100),
  name VARCHAR(100),
  FOREIGN KEY (name) REFERENCES Director(name) ON DELETE CASCADE,
  FOREIGN KEY (film_id) REFERENCES Film(film_id) ON DELETE CASCADE,
  UNIQUE(name, film_id)
);

create table ContentRating(
  content_rating VARCHAR(100) PRIMARY KEY
);

create table Rated(
  film_id VARCHAR(100) UNIQUE,
  content_rating VARCHAR(100),
  FOREIGN KEY (content_rating) REFERENCES ContentRating(content_rating) ON DELETE CASCADE,
  FOREIGN KEY (film_id) REFERENCES Film(film_id) ON DELETE CASCADE
);

create table MovieGenre(
  genre VARCHAR(100) PRIMARY KEY
);

create table GenreOf(
  film_id VARCHAR(100),
  genre VARCHAR(100),
  FOREIGN KEY (genre) REFERENCES MovieGenre(genre) ON DELETE CASCADE,
  FOREIGN KEY (film_id) REFERENCES Film(film_id) ON DELETE CASCADE,
  UNIQUE(genre, film_id)
);


