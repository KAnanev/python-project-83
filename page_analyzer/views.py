from flask import Blueprint, render_template, request, flash, redirect, url_for

from page_analyzer.db import get_db
from page_analyzer.services import URLParse, add_url

bp = Blueprint('page_analyzer', __name__)

INSERT_URL_QUERY = 'INSERT INTO urls (name, created_at) ' \
                   'VALUES (%s,%s) ON CONFLICT DO NOTHING RETURNING id'
SELECT_URL_QUERY = 'SELECT * FROM urls WHERE id = (%s)'
SELECT_URLS_QUERY = 'SELECT * FROM urls ORDER BY id DESC'


@bp.route('/', methods=('GET', 'POST'))
def index():
    return render_template('index.html')


@bp.route('/urls', methods=('GET', 'POST'))
def urls():
    db = get_db()
    if request.method == 'POST':
        new_url = request.form['url']
        new_parsed_url = URLParse(new_url)
        if new_parsed_url.validate:
            url_id = add_url(new_parsed_url.normalize, db)
            return redirect(url_for('page_analyzer.url', url_id=url_id))
        flash('Некорректный URL', 'danger')
        return redirect(url_for('index'))
    rows = db.execute(SELECT_URLS_QUERY).fetchall()
    return render_template('urls.html', urls=rows)


@bp.route('/urls/<int:url_id>')
def url(url_id):
    db = get_db()
    row = db.execute(SELECT_URL_QUERY, (url_id,)).fetchone()
    return render_template('url.html', url=row)
