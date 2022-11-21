from flask import Blueprint, url_for, render_template
from werkzeug.utils import redirect

bp = Blueprint('menu', __name__, url_prefix='/menu')


@bp.route('/mainpage/')
def mainpage():
    return render_template('mainpage.html')

''' 네비게이션의 로그인 이후 나오는 로그아웃 기능을 구현한 authority_views.py에 마이페이지도 추가하기
@bp.route('/mypage/')
def mypage():
    return render_template('mypage.profile')
    '''

@bp.route('/online/')
def online():
    return redirect('online.board')

@bp.route('/offline/')
def offline():
    return redirect('offline.board')

@bp.route('/intro/')
def intro():
    return redirect('intro._page')