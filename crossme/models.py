from crossme import db

class Freeboard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    # 작성자 속성
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('freeboard_set'))



class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    freeboard_id = db.Column(db.Integer, db.ForeignKey('freeboard.id', ondelete='CASCADE'))
    freeboard = db.relationship('Freeboard', backref=db.backref('comment_set'))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    # 작성자 속성
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('comment_set'))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False) # 사용자 id
    password = db.Column(db.String(200), nullable=False) # 비밀번호
    
