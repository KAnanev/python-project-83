import click

from flask import current_app, g

from page_analyzer.services.db import PostgresDB


def get_db():
    """Функция проверяет наличие объекта соединения
    с базой данных в контексте приложения Flask"""
    if 'db' not in g:
        g.db = PostgresDB(current_app.config['DATABASE_URL'])
    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('database.sql') as f:
        db.execute_query(f.read().decode('utf8'))


@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('База данных инициализирована')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
