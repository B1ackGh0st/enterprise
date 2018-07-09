# -*- coding: utf-8 -*-
from flask import Flask, request, make_response, redirect, url_for
from config import Configuration
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_login import LoginManager, current_user, login_required, UserMixin
from flask_admin import Admin, BaseView
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView
import re

def load_user_id(id):
    return User.query.get(int(id))

def load_user_role(user_roles):
    return User.role.get(int(user_roles))

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
class AdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated \
               and current_user.has_role('Administrator')
        if not current_user.is_authenticated():
            return False
        return current_user.has_role('Administrator')
        #return current_user.is_authenticated

class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated \
               and current_user.has_role('Administrator')
        if not current_user.is_authenticated():
            return False
        return current_user.has_role('Administrator')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))

class BaseModelView(ModelView):
    def on_model_change(self, form, model, is_created):
        #model.generated_slug()
        return super(BaseModelView, self).on_model_change(form, model, is_created)

class DefectAdminView(BaseModelView):
    column_labels = dict(equipment='Оборудование',description='Описание')
    form_columns = ['equipment', 'description']

# Класс пользователей для админки
class UserAdminView(BaseModelView):
    column_labels = dict(username='Логин', surname='Фамилия', name='Имя', middle_name='Отчество')
    form_columns = ['username', 'surname', 'name', 'middle_name']

# Класс ролей для админки
class RoleAdminView(BaseModelView):
    column_labels = dict(name='Пользователь', description='Описание')
    form_columns = ['user', 'role']
    pass

# Класс оборудования для админки
class EquipmentAdminView(BaseModelView):
    column_labels = dict(name='Наименование')
    form_columns = ['name']
    pass

# Создаем админку
admin = Admin(app, template_mode='bootstrap3', index_view=AdminIndexView())

# Страница редактирования дефектов
admin.add_view(AdminModelView(Defect, db.session))
# Страница редактирования пользователей
admin.add_view(AdminModelView(User, db.session))
# Страница редактирования ролей пользователей
admin.add_view(AdminModelView(Role, db.session))
# Страница редактирования оборудования
admin.add_view(AdminModelView(Equipment, db.session))

# Setup Flask-Security
#user_datastore = SQLAlchemyUserDatastore(db, User, Role)
#security = Security(app, user_datastore)