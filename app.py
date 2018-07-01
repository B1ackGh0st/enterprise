# -*- coding: utf-8 -*-
from flask import Flask, request, make_response
from config import Configuration
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView
from flask_security import SQLAlchemyUserDatastore
from flask_security import Security, RoleMixin
from flask import redirect, request, url_for
from flask_login import login_user, logout_user, current_user, login_required


def load_user_id(id):
    return User.query.get(int(id))

# обрезка строки
def shorten_line(text):
    str = text[:75]
    return str

app = Flask(__name__)
app.jinja_env.globals.update(load_user_id=load_user_id, shorten_line=shorten_line)
app.config.from_object(Configuration)

db = SQLAlchemy(app)

### Migrate ###
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

login = LoginManager(app)
login.login_view = 'login'

from models import *


# Разграничение доступа к админки и ее функциям
class AdminMixin:
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        # next='' <- Сыылка куда будет перенапровлятся пользователь
        return redirect( url_for('security.login', next=request.url))


class BaseModelView(ModelView):
    def on_model_change(self, form, model, is_created):
        #model.generated_slug()
        return super(BaseModelView, self).on_model_change(form, model, is_created)

class AdminView(AdminMixin, ModelView):
    pass

class HomeAdminView(AdminMixin, AdminIndexView):
    pass

class DefectAdminView(BaseModelView):
    column_labels = dict(equipment='Оборудование',description='Описание')
    form_columns = ['equipment', 'description']
    pass


class UserAdminView(BaseModelView):
    column_labels = dict(username='Логин', surname='Фамилия', name='Имя', middle_name='Отчество')
    form_columns = ['username', 'surname', 'name', 'middle_name']
    pass


class RoleAdminView(BaseModelView):
    column_labels = dict(name='Наименование', description='Описание')
    form_columns = ['name', 'description']
    pass


class equipmentAdminView(BaseModelView):
    column_labels = dict(name='Наименование')
    form_columns = ['name']
    pass


admin = Admin(app, 'FlaskApp', url='/', index_view=HomeAdminView(name='Home'))
admin.add_view(DefectAdminView(Defect, db.session))
admin.add_view(UserAdminView(User, db.session))
admin.add_view(RoleAdminView(Role, db.session))
admin.add_view(equipmentAdminView(Equipment, db.session))
