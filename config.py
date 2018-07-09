# -*- coding: utf-8 -*-
class Configuration(object):
    DEBUG = True
    STATIC_FOLDER = '/static'
    SECRET_KEY = 'SECRET_KEY'

    # БД
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://username1:password1@localhost/enterprise'

    '''отключаем функцию Flask-SQLAlchemy, которая которая сигнализирует приложению каждый раз, когда
    в базе данных должно быть внесено изменение.'''
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ### FLASK SECURITY ###
    SECURITY_PASSWORD_SALT = 'salt'
    SECURITY_PASSWORD_HASH = 'sha512_crypt'

    USER_ENABLE_CONFIRM_EMAIL = False
    MAIL_DEFAULT_SENDER = False
    SECURITY_CONFIRM_URL = False
    SECURITY_CONFIRMABLE = False
    SECURITY_REGISTERABLE = False
    SECURITY_USER_IDENTITY_ATTRIBUTES = 'username'

