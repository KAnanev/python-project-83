import os

import psycopg


DATABASE_URL = os.environ['DATABASE_URL']


class Psycopg:
    def __enter__(self):
        self.conn = psycopg.connect(DATABASE_URL)
        return self.conn.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()


def create_db():
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(open('../database.sql').read())
            conn.commit()


def insert_url(url, created_time):
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                'INSERT INTO urls (name, created_at) VALUES (%s, %s)',
                (url, created_time)
            )
            conn.commit()
