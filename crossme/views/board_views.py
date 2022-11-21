from flask import Blueprint, render_template, request, url_for
from crossme.views.authority_views import login_required


bp = Blueprint('board', __name__, url_prefix='/board')

@bp.route('/intro/')
def intro():
    return render_template('intro.html')
