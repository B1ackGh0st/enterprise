# -*- coding: utf-8 -*-
class Configuration(object):
    DEBUG = True
    STATIC_FOLDER = '/static'
    SECRET_KEY = 'SECRET_KEY'

    # БД
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://username1:password1@localhost/enterprise'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ### FLASK SECURITY ###
    SECURITY_PASSWORD_SALT = 'salt'
    SECURITY_PASSWORD_HASH = 'sha512_crypt'