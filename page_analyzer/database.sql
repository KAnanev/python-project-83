DROP TABLE IF EXISTS urls CASCADE;

CREATE TABLE IF NOT EXISTS urls (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS url_checks (
    id SERIAL PRIMARY KEY,
    url_id INT,
    status_code TEXT,
    h1 TEXT,
    title TEXT,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE,
    FOREIGN KEY (url_id) REFERENCES urls (id)
);