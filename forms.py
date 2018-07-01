from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, BooleanField, SubmitField, Form, TextAreaField, HiddenField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from models import *
from wtforms_sqlalchemy.fields import QuerySelectField
from flask_login import login_user, logout_user, current_user, login_required

class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    middle_name = StringField('Отчество', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField('Пароль еще раз', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрировать')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Пожалуйста, используйте другое имя пользователя.')


class DefectForm(UserMixin, FlaskForm):
    equipment = QuerySelectField('Оборудование', query_factory=equipment_query, get_label='name', allow_blank=True,
    get_pk = lambda a: a.id, blank_text = "Выберите оборудование...")
    body = TextAreaField('Описание дефекта')
    submit = SubmitField('Отправить')
