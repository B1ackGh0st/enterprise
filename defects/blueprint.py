# -*- coding: utf-8 -*-
from flask import Blueprint
from flask import render_template
from flask import request, redirect
from app import *
from flask import url_for
from flask_security import login_required
from flask import redirect, url_for, request
from models import *
from forms import *
from flask_user import roles_required, UserMixin
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy import update

defects = Blueprint('defects', __name__, template_folder='templates')

''' Создание поста '''
# http://localhost/defect/create
@defects.route('/create', methods=['POST', 'GET'])
def create_defect():
    if request.method == 'POST':
        equipment = request.form['equipment']
        body = request.form['body']
        user = request.form['user']
        try:
            defect = Defect(equipment=equipment,
                            description=body,
                            author_id=user)
            db.session.add(defect)
            db.session.commit()
        except:
            print ('Something wrong')
        return redirect(url_for('defects.index'))
    form = DefectForm()
    #form.equipment.query = Equipment.query
    return render_template('defects/create_defect.html', form=form)


''' Редактирование поста '''
# http://localhost/defects/edit
@defects.route('/<slug>/edit/', methods = ['POST', 'GET'])
@login_required
def edit_defect(id):
    defect = Defect.query.filter(Defect.slug == slug).first_or_404()

    if request.method == 'POST':
        form = DefectForm(fordefectsmdata=request.form, obj=defect)
        form.populate_obj(defect)
        db.session.commit()

        return redirect(url_for('defect.defect_detail', slug=defect.slug))

    form = DefectForm(obj=defect)
    return render_template('defects/edit_defect.html', defect=defect, form=form)

# http://localhost/defects/
@defects.route('/')
def index():
    page = request.args.get('page')
    if page and page.isdigit(): # Если переменная имеет значение и переменная является цифрой
        page = int(page) # Преобразуем переменную в цифру
    else: # Иначе ...
        page = 1 # Даем значение переменной 1

    # пагинация

    defects = Defect.query.order_by(Defect.created.desc())

    # Колличество выводимых записей
    page_num = 10
    pages = defects.paginate(page=page, per_page=page_num)

    defect_count = Defect.query.count()
    defect_accept = Defect.query.filter(Defect.taken_user_id != 1).count()
    defect_not_accept = Defect.query.filter(Defect.taken_user_id == 1).count()
    defect_writing = Defect.query.filter(Defect.eliminated != 0).count()


    # Выводим шаблон
    return render_template('defects/index.html',
                           defects=defects,
                           pages=pages,
                           defect_count=defect_count,
                           defect_accept=defect_accept,
                           defect_writing=defect_writing
                           )

# http://localhost/defects/<slug>
@defects.route('/<id>')
def defect_detail(id):
    defect = Defect.query.filter(Defect.id == id).first_or_404()
    return render_template('defects/defect_detail.html', defect=defect)


# AJAX

""" Принять дефект """
@app.route('/accept_a_defect', methods=['GET', 'POST'])
def accept_a_defect():
    defect_id = request.form['defect_id'];

    rows = Defect.query.filter_by(id=defect_id).update({'taken_user_id': current_user.id})
    db.session.commit()

    page = request.args.get('page')
    if page and page.isdigit(): # Если переменная имеет значение и переменная является цифрой
        page = int(page) # Преобразуем переменную в цифру
    else: # Иначе ...
        page = 1 # Даем значение переменной 1

    defects = Defect.query.order_by(Defect.created.desc())

    # пагинация

    # Колличество выводимых записей
    page_num = 10
    pages = defects.paginate(page=page, per_page=page_num)
    # Выводим шаблон
    return render_template('defects/defects-ajax.html', defects=defects, pages=pages)


""" Отпись дефекта """
@app.route('/defect_writing', methods=['GET', 'POST'])
def defect_writing():

    if request.method == 'POST':
        defect_id = request.form['defect_id'];
        eliminated_description = request.form['eliminated_description'];

        rows = Defect.query.filter_by(id=defect_id).update({'eliminated_description':eliminated_description, 'eliminated':1})
        db.session.commit()
    pass


# http://localhost/defects/
@defects.route('/defect_type', methods=['GET', 'POST'])
def defect_type():
    defect_type = request.form['defect_type'];

    page = request.args.get('page')
    if page and page.isdigit(): # Если переменная имеет значение и переменная является цифрой
        page = int(page) # Преобразуем переменную в цифру
    else: # Иначе ...
        page = 1 # Даем значение переменной

    # пагинация
    #defect_type = request.args.get('defect_type')

    if defect_type == 'all':
        defects = Defect.query.order_by(Defect.created.desc())

    elif defect_type == 'adopted':
        defects = Defect.query.filter(Defect.taken_user_id != 1).order_by(Defect.created.desc())

    elif defect_type == 'not_adopted':
        defects = Defect.query.filter(Defect.taken_user_id == 1).order_by(Defect.created.desc())

    elif defect_type == 'eliminated':
        defects = Defect.query.filter(Defect.eliminated == 1).order_by(Defect.created.desc())

    # Колличество выводимых записей

    page_num = 10
    pages = defects.paginate(page=page, per_page=page_num)

    # Выводим шаблон
    return render_template('defects/defects-ajax.html', defects=defects, pages=pages)


def defect_chart():
    Defect.query.filter_by(condition).count()
    pass
