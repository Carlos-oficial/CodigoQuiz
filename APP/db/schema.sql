DROP TABLE IF EXISTS answer_log;

CREATE TABLE IF NOT EXISTS user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS record (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  score INTEGER NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);
CREATE TABLE answer_log (
  question_id INTEGER NOT NULL,
  status TEXT CHECK(status IN ('Wrong', 'Right', 'Unanswered')) NOT NULL DEFAULT 'Unanswered',
  author_id INTEGER NOT NULL,
  record_id INTEGER NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id),
  FOREIGN KEY (record_id) REFERENCES record (id)
);