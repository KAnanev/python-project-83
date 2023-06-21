import psycopg
import click

from flask import current_app, g
from psycopg.rows import dict_row


def get_db():
    """Функция проверяет наличие объекта соединения
    с базой данных в контексте приложения Flask"""
    if 'db' not in g:
        g.db = psycopg.connect(
            current_app.config['DATABASE_URL'], row_factory=dict_row
        )
    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('database.sql') as f:
        db.execute(f.read().decode('utf8'))
        db.commit()


@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('База данных инициализирована')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
