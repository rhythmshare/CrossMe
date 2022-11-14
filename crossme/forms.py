from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo

class FreeboardForm(FlaskForm):
    subject = StringField('제목', validators=[DataRequired('제목을 입력하세요.')])  #라벨: 제목, 필수항목 체크
    content = TextAreaField('내용', validators=[DataRequired('내용을 입력하세요.')])   #라벨: 내용
    
class CommentForm(FlaskForm):
    content = TextAreaField('댓글', validators=[DataRequired('댓글 내용을 입력하세요.')])
    
class UserCreateForm(FlaskForm):
    username = StringField('사용자ID', validators=[DataRequired(), Length(min=5, max=25)])
    password1 = PasswordField('비밀번호', validators=[DataRequired(), EqualTo('password2', '비밀번호가 일치하지 않습니다')])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired()])

class UserLoginForm(FlaskForm):
    username = StringField('사용자ID', validators=[DataRequired(), Length(min=5, max=25)])
    password = PasswordField('비밀번호', validators=[DataRequired()])