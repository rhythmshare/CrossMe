from datetime import datetime

from flask import Blueprint, url_for, request, render_template, g, flash
from werkzeug.utils import redirect

from crossme import db
from crossme.forms import CommentForm
from crossme.models import Freeboard, Comment
from .authority_views import login_required

bp = Blueprint('comment', __name__, url_prefix='/comment')


@bp.route('/create/<int:freeboard_id>', methods=('POST',))
@login_required
def create(freeboard_id):
    form = CommentForm()
    freeboard = Freeboard.query.get_or_404(freeboard_id)
    if form.validate_on_submit():
        content = request.form['content']
        comment = Comment(content=content, create_date=datetime.now(), user=g.user)
        freeboard.comment_set.append(comment)
        db.session.commit()
        return redirect('{}#comment_{}'.format(url_for('freeboard.detail', freeboard_id=freeboard_id), comment.id)) # 앵커 엘리먼트
    return render_template('freeboard/freeboard_detail.html', freeboard=freeboard, form=form)

@bp.route('/delete/<int:comment_id>')
@login_required
def delete(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    freeboard_id = comment.freeboard.id
    if g.user != comment.user:
        flash('삭제권한이 없습니다')
    else:
        db.session.delete(comment)
        db.session.commit()
    return redirect('{}#comment_{}'.format(url_for('freeboard.detail', freeboard_id=freeboard_id), comment.id)) # 앵커 엘리먼트