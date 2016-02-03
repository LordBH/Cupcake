CREATE TABLE user_table (
	  id serial PRIMARY KEY,
    username text UNIQUE,
    password text
);



INSERT INTO user_table (username, password) VALUES
    ('Cheese', 123),
    ('Bread', 123),
    ('Milk', 123);
