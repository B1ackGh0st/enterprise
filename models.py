from app import db, login
from datetime import datetime
import re
from flask_login import UserMixin
from hashlib import md5
#from flask_security import UserMixin, RoleMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql.functions import func

### FLASK_SECURiTY ###

roles_users = db.Table('roles_users',
                     db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                     db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
                     )
### Пользователи ###


### Преобразование для ЧПУ ###
def slugify(s):
    pattern = r'[^\w+]'
    return re.sub(pattern, '-', s)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Role(UserMixin, db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(255))

def role_query(columns=None):
    return Role.query.all()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    surname = db.Column(db.String(64), index=True)
    name = db.Column(db.String(64), index=True)
    middle_name = db.Column(db.String(64), index=True)
    password_hash = db.Column(db.String(128))
    role = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy=True), lazy=True)
    defect = db.relationship('Defect', backref=db.backref('author', lazy=True), lazy=True,
                                   foreign_keys="Defect.author_id")
    defect_taken = db.relationship('Defect', backref=db.backref('defect_taken', lazy=True), lazy=True,
                                   foreign_keys="Defect.taken_user_id")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def has_roles(self, *args):
        return set(args).issubset({role.name for role in self.roles})


class Equipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    defect = db.relationship('Defect', backref=db.backref('equipments'))


class Defect(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equipment = db.Column(db.Integer, db.ForeignKey('equipment.id'))
    description = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    taken_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, default=1)
    created = db.Column(db.DateTime, default=datetime.now())  # Дата создания
    eliminated = db.Column(db.Integer, nullable=False, default=0)
    eliminated_description = db.Column(db.Text)

    def __init__(self, *args, **kwargs):
        super(Defect, self).__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        if self.id:
            self.slug = slugify(self.id)

    def __repr__(self):
        return '<Post id: {}, title: {}>'.format(self.id, self.title)

def equipment_query(columns=None):
    return Equipment.query

def load_query(id):
    return Equipment.query.get(int(id))