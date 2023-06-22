from flask import Blueprint, render_template, request, flash, redirect, url_for

from page_analyzer.db import get_db
from page_analyzer.services import URLParse, add_or_get_url

bp = Blueprint('page_analyzer', __name__)

INSERT_URL_QUERY = 'INSERT INTO urls (name, created_at) ' \
                   'VALUES (%s,%s) ON CONFLICT DO NOTHING RETURNING id'
SELECT_URL_QUERY = 'SELECT * FROM urls WHERE id = (%s)'
SELECT_URLS_QUERY = 'SELECT * FROM urls ORDER BY id DESC'


@bp.get('/')
def index():
    """Главная страница."""

    return render_template('index.html')


@bp.get('/urls')
def get_urls():
    """Страница со всеми url."""

    db = get_db()
    rows = db.execute(SELECT_URLS_QUERY).fetchall()
    return render_template('urls.html', urls=rows)


@bp.post('/urls')
def post_url():
    """ Проверяет есть ли url в базе,
    добавляет в базу или берет из базы существующий,
    редиректит на страницу с url."""

    db = get_db()
    parsed_url = URLParse(request.form['url'])
    if parsed_url.validate:
        url_id = add_or_get_url(parsed_url.normalize, db)
        return redirect(url_for('page_analyzer.get_url', url_id=url_id))

    flash('Некорректный URL', 'danger')
    return redirect(url_for('index'))


@bp.get('/urls/<int:url_id>')
def get_url(url_id):
    """Страница c url с выдачей по id."""

    db = get_db()
    row = db.execute(SELECT_URL_QUERY, (url_id,)).fetchone()
    return render_template('url.html', url=row)
