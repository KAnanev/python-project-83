from flask import Blueprint, render_template, request, flash

from page_analyzer.db import get_db
from page_analyzer.services import URLParse, get_date_now

bp = Blueprint('page_analyzer', __name__)

INSERT_URL_QUERY = 'INSERT INTO urls (name, created_at) VALUES (%s,%s)'
SELECT_URL_QUERY = 'SELECT * FROM urls WHERE id = (%s)'
SELECT_URLS_QUERY = 'SELECT * FROM urls'


@bp.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        _url = request.form['url']
        _url = URLParse(_url)
        if _url.validate:
            db = get_db()
            db.execute(INSERT_URL_QUERY, (_url.normalize, get_date_now(),))
            db.commit()
        else:
            flash('Некорректный URL', 'danger')
    return render_template('index.html')


@bp.route('/urls')
def urls():
    db = get_db()
    rows = db.execute(SELECT_URLS_QUERY).fetchall()
    return render_template('urls.html', urls=rows)


@bp.route('/urls/<int:url_id>')
def url(url_id):
    db = get_db()
    row = db.execute(SELECT_URL_QUERY, url_id).fetchone()
    return render_template('url.html', url=row)
