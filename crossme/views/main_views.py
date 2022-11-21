from flask import Blueprint, url_for
from werkzeug.utils import redirect


bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/hello')
def hello_crossme():
    return 'Hello, Crossme!'

@bp.route('/')
def index():
    #return redirect(url_for('freeboard._list'))
    return redirect(url_for('menu.mainpage'))