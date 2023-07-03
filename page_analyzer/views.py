from flask import Blueprint, render_template, request, flash, redirect, url_for, g


from page_analyzer.services.url import URLService

bp = Blueprint('page_analyzer', __name__)


@bp.get('/')
def index():
    """Главная страница."""

    return render_template('index.html')


@bp.get('/urls')
def get_urls():
    """Страница со всеми url."""

    db = g.get('my_db')
    url_service = URLService(db=db)
    items = url_service.get_all_items()

    return render_template('urls.html', urls=items)


@bp.post('/urls')
def post_url():
    """ Проверяет есть ли url в базе,
    добавляет в базу или берет из базы существующий,
    редиректит на страницу с url."""

    db = g.get('my_db')

    url = request.form['url']

    url_service = URLService(db=db)

    result = url_service.insert_item(url)
    flash(*result['message'])

    if result['item']:
        return redirect(
            url_for(
                'page_analyzer.get_url',
                url_id=result['item']['id']),
        )

    return redirect(url_for('index'))


@bp.get('/urls/<int:url_id>')
def get_url(url_id):
    """Страница c url с выдачей по id."""

    db = g.get('my_db')
    url_service = URLService(db=db)
    item = url_service.get_item_by_id(url_id)
    print(item)
    return render_template('url.html', item=item)


@bp.post('/urls/<int:url_id>/checks')
def check_url(url_id):
    db = g.get('my_db')
    url_service = URLService(db=db)
    message = url_service.insert_item_in_url_checks(url_id)
    flash(*message)
