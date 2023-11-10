from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, ValidationError
from models import User

# ログイン用入力クラス
class LoginForm(FlaskForm):
    username = StringField('ユーザー名：',
                           validators=[DataRequired('ユーザー名は必須入力です')])
    password = PasswordField('パスワード: ',
                             validators=[Length(1, 10,
                                    'パスワードの長さは4文字以上10文字以内です')])
    submit = SubmitField('ログイン')

class SignUpForm(LoginForm):
    submit = SubmitField('サインアップ')
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('そのユーザー名は既に使用されています')
