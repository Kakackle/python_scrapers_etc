DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS history;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE history (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  term TEXT NOT NULL,
  action_type TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);