# -*- coding: utf-8 -*-
from app import app, db
from models import User
from defects.blueprint import defects
import view


app.register_blueprint(defects, url_prefix='/defects')


if __name__ == '__main__':
    app.run()