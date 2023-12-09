DROP TABLE IF EXISTS titles;
CREATE TABLE titles (
    title_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    title TEXT,
    year INTEGER,
    link_title TEXT,
    pages INTEGER,
    price INTEGER,
    link_publisher TEXT,
    FOREIGN KEY(link_publisher) REFERENCES publishers(publisher_id)
);

DROP TABLE IF EXISTS publishers;
CREATE TABLE publishers (
  publisher_id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  number_of_titles INTEGER,
  link TEXT
);