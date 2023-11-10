from flask_wtf import FlaskForm
from flask import session
from wtforms import StringField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, ValidationError
from models import URLList
from urllib.parse import urlparse
import urllib.request, urllib.error

class InputForm(FlaskForm):
    def url_validator(self, url):
        try:
            response = urllib.request.urlopen(url.data)
        except urllib.error.HTTPError as e:
            raise ValidationError('HTTPError')
        except urllib.error.URLError as e:
            raise ValidationError('URLError')
        except :
            pass
    def url_parse(self, url):
        result = urlparse(url.data)
        check = len(result.scheme)
        if check < 1:
            raise ValidationError('URLが有効ではありません')

    url = StringField('URL名：',
                           validators=[DataRequired('必須入力です')\
                           , url_validator, url_parse])
    submit = SubmitField('発行')
