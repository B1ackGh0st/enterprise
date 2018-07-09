from app import *
from models import *
from forms import *
from flask import render_template, flash, request, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
db.session.commit()


# http://localhost/
@app.route('/')
@app.route('/index')
#@login_required
def index():
    defect_count = Defect.query.count()
    defect_accept = Defect.query.filter(Defect.taken_user_id != 0).count()
    defect_not_accept = Defect.query.filter(Defect.taken_user_id == None).count()
    defect_writing = Defect.query.filter(Defect.eliminated != 0).count()

    January = Defect.query.filter(func.extract('month', Defect.created) == 1).count()
    February = Defect.query.filter(func.extract('month', Defect.created) == 2).count()
    March = Defect.query.filter(func.extract('month', Defect.created) == 3).count()
    April = Defect.query.filter(func.extract('month', Defect.created) == 4).count()
    May = Defect.query.filter(func.extract('month', Defect.created) == 5).count()
    June = Defect.query.filter(func.extract('month', Defect.created) == 6).count()
    July = Defect.query.filter(func.extract('month', Defect.created) == 7).count()
    August = Defect.query.filter(func.extract('month', Defect.created) == 8).count()
    September = Defect.query.filter(func.extract('month', Defect.created) == 9).count()
    October = Defect.query.filter(func.extract('month', Defect.created) == 10).count()
    November = Defect.query.filter(func.extract('month', Defect.created) == 11).count()
    December = Defect.query.filter(func.extract('month', Defect.created) == 12).count()

    return render_template('index.html',
                           title='Home Page',
                           defect_count=defect_count,
                           defect_accept=defect_accept,
                           defect_not_accept=defect_not_accept,
                           defect_writing=defect_writing,
                           January=January,
                           February=February,
                           March=March,
                           April=April,
                           May=May,
                           June=June,
                           July=July,
                           August=August,
                           September=September,
                           October=October,
                           November=November,
                           December=December
                           )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неверное имя пользователя или пароль')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Войти', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))



@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    surname=form.surname.data,
                    name=form.name.data,
                    middle_name=form.middle_name.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        #flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    defects = Defect.query.filter(Defect.taken_user_id == current_user.id).order_by(Defect.created.desc())

    return render_template('user.html', defects=defects)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)