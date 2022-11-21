from datetime import datetime

from flask import Blueprint, render_template, request, url_for, g, flash
from werkzeug.utils import redirect
from crossme import db
from crossme.forms import FreeboardForm, CommentForm
from crossme.models import Freeboard, Comment, User
from crossme.views.authority_views import login_required


bp = Blueprint('freeboard', __name__, url_prefix='/freeboard')


@bp.route('/list/')
def _list():
    page = request.args.get('page', type=int, default=1) # 페이지
    kw = request.args.get('kw', type=str, default='')
    freeboard_list = Freeboard.query.order_by(Freeboard.create_date.desc())
    if kw:
        search = '%%{}%%'.format(kw)
        sub_query = db.session.query(Comment.freeboard_id, Comment.content, User.username) \
            .join(User, Comment.user_id == User.id).subquery()
        freeboard_list = freeboard_list \
            .join(User) \
            .outerjoin(sub_query, sub_query.c.freeboard_id == Freeboard.id) \
            .filter(Freeboard.subject.ilike(search) |  # 자유게시판 게시물 제목
                    Freeboard.content.ilike(search) |  # 자유게시판 게시물 내용
                    User.username.ilike(search) |       # 자유게시판 게시물 작성자
                    sub_query.c.content.ilike(search) |  # 댓글내용
                    sub_query.c.username.ilike(search)  # 댓글작성자
                    ) \
            .distinct()
    freeboard_list = freeboard_list.paginate(page=page, per_page=10)
    return render_template('freeboard/freeboard_list.html', freeboard_list=freeboard_list, page=page, kw=kw)
    


@bp.route('/detail/<int:freeboard_id>/')
def detail(freeboard_id):
    form = CommentForm()
    freeboard = Freeboard.query.get_or_404(freeboard_id)
    return render_template('freeboard/freeboard_detail.html', freeboard=freeboard, form=form)

@bp.route('/create/', methods=('GET','POST')) #freeboard_form 데이터 전송방식:post
@login_required
def create():
    form = FreeboardForm()   # 로컬 속성 form에 FreeboardForm
    if request.method == 'POST' and form.validate_on_submit():
        freeboard = Freeboard(subject=form.subject.data, content=form.content.data, create_date=datetime.now(), user=g.user)
        db.session.add(freeboard)
        db.session.commit()
        return redirect(url_for('board.intro'))
    return render_template('freeboard/freeboard_form.html', form=form) # freeboard_form.html 템플릿에 전달 FreeboardForm의 객체(form)은 템플릿에서 라벨 or 입력폼 등 만들 때 사용

# 자유게시판 게시글 수정
@bp.route('/modify/<int:freeboard_id>', methods=('GET', 'POST'))
@login_required
def modify(freeboard_id):
    freeboard = Freeboard.query.get_or_404(freeboard_id)
    if g.user != freeboard.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('freeboard.detail', freeboard_id=freeboard_id))
    if request.method == 'POST':  # POST 요청
        form = FreeboardForm()
        if form.validate_on_submit():
            form.populate_obj(freeboard)
            freeboard.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect(url_for('freeboard.detail', freeboard_id=freeboard_id))
    else:  # GET 요청
        form = FreeboardForm(obj=freeboard)
    return render_template('freeboard/freeboard_form.html', form=form)

@bp.route('/delete/<int:freeboard_id>')
@login_required
def delete(freeboard_id):
    freeboard = Freeboard.query.get_or_404(freeboard_id)
    if g.user != freeboard.user:
        flash('삭제권한이 없습니다')
        return redirect(url_for('freeboard.detail', freeboard_id=freeboard_id))
    db.session.delete(freeboard)
    db.session.commit()
    return redirect(url_for('freeboard._list'))

