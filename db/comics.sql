DROP TABLE IF EXISTS titles;
CREATE TABLE titles (
    title_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    title TEXT,
    year INTEGER,
    link_title TEXT,
    pages INTEGER,
    price INTEGER,
    link_publisher TEXT,
    publisher_id INTEGER,
    FOREIGN KEY(publisher_id) REFERENCES publishers(publisher_id)
);

DROP TABLE IF EXISTS publishers;
CREATE TABLE publishers (
  publisher_id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  number_of_titles INTEGER,
  link TEXT
);