from flask_wtf import FlaskForm
from flask import current_app
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
import sqlalchemy as sa
from app.models.models import User


class LoginForm(FlaskForm):
    username = StringField(
        "Логин", validators=[DataRequired(message="Пожалуйста, введите логин")])
    password = PasswordField(
        "Пароль", validators=[DataRequired(message="Пожалуйста, введите пароль")])
    remember_me = BooleanField("Запомнить меня")
    submit = SubmitField("Войти")


class RegistrationForm(FlaskForm):
    username = StringField(
        "Логин", validators=[DataRequired(message="Пожалуйста, введите логин")]) #добавить правила (длина, запретные слова)
    email = StringField(
        "Почта", validators=[DataRequired(message="Пожалуйста, введите почту"), Email('Некорректный адрес')])
    password = PasswordField(
        "Пароль", validators=[DataRequired(message="Пожалуйста, введите пароль")])  #добавить правила (длина, символы и чет еще)
    password2 = PasswordField(
        "Пароль повторно",
        validators=[
            DataRequired(message="Пожалуйста, введите пароль"),
            EqualTo("password", message="Пароли должны совпадать")])
    submit = SubmitField('Регистрация')

class EditProfileForm(FlaskForm):
    username = StringField(
        "Логин", validators=[DataRequired(message="введите логин")]) #добавить правила (длина, запретные слова)
    email = StringField(
        "Почта", validators=[DataRequired(message="Пожалуйста, введите почту"), Email('Некорректный адрес')])
    # password = PasswordField(
    #     "Пароль", validators=[DataRequired(message="введите пароль")])  #добавить правила (длина, символы и чет еще)
    # password2 = PasswordField(
    #     "Пароль повторно",
    #     validators=[
    #         DataRequired(message="Пожалуйста, введите пароль"),
    #         EqualTo("password", message="Пароли должны совпадать")])
    submit = SubmitField('Сохранить')
    cancel = SubmitField('Отмена')