from wtforms import EmailField, PasswordField, \
    BooleanField, SubmitField, StringField, IntegerRangeField, SelectField, SelectMultipleField
from data import db_session
from data.users import User
from data.jobs import Jobs
from flask import Flask, url_for, render_template, redirect
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from flask_login import LoginManager, login_user, login_required, logout_user
from datetime import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login = LoginManager()
login.init_app(app)
db_session.global_init('db/blogs.db')


@login.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


class LoginForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    age = SelectField('Возраст', validators=[DataRequired()], choices=range(100))
    position = StringField('Должность', validators=[DataRequired()])
    spec = SelectField('Профессии', validators=[DataRequired()],
                       choices=['Никто', 'инженер', 'врач', 'пилот',
                                'геолог', 'физик', 'свистун'])
    address = StringField('Расположение', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class EntryForm(FlaskForm):
    em = EmailField('Почта', validators=[DataRequired()])
    pas = PasswordField('Пароль', validators=[DataRequired()])
    forgot = BooleanField('Запомнить меня')
    sub = SubmitField('Войти')


@app.route('/entry', methods=['GET', 'POST'])
def entry():
    form = EntryForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.em).first()
        if user and user.check_password(form.pas.data):
            login_user(user, remember=form.forgot.data)
            return redirect('/')
        return render_template('entry.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('entry.html', title='Вход', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        sess = db_session.create_session()
        if sess.query(User).filter(User.email == str(form.email.data)).first():
            return render_template('/login', form=form, message='Такой пользователь уже есть')

        user = User()
        user.name = form.name.data
        user.surname = form.surname.data
        user.age = form.age.data
        user.email = form.email.data
        user.position = form.position.data
        user.speciality = form.spec.data
        user.address = form.address.data
        user.set_password(form.password.data)

        sess.add(user)
        sess.commit()
        return redirect('/', code=302)
    return render_template('login.html', form=form, title='Регистрация')


class AddJobs(FlaskForm):
    sess = db_session.create_session()
    job = StringField('Название задачи', validators=[DataRequired()])
    work_size = SelectField('Необходимое для выполнения время',
                            choices=range(100), validators=[DataRequired()])
    captain = SelectField('Руководитель', choices=[f'{x.id}: {x.name} {x.surname}' for x in sess.query(User).all()],
                          validators=[DataRequired()])
    members = StringField('Участники', validators=[DataRequired()])
    is_finished = BooleanField('Выполнена ли задача')
    btn = SubmitField('Добавить!')


@app.route('/add', methods=['GET', 'POST'])
def adding():
    form = AddJobs()
    if form.validate_on_submit():
        sess = db_session.create_session()
        job = Jobs()
        job.job = form.job.data
        job.team_leader = form.captain.data
        job.work_size = form.work_size.data
        job.collaborators = form.members.data
        job.is_finished = form.is_finished.data
        job.start_date = datetime.now()

        sess.add(job)
        sess.commit()
        return redirect('/', code=302)
    return render_template('adding.html', form=form, title='Добавление записи')


class MainForm(FlaskForm):
    pass


@app.route('/', methods=['GET', 'POST'])
@app.route('/main', methods=['GET', 'POST'])
def main():
    form = MainForm()
    sess = db_session.create_session()
    data = []
    print(sess.query(Jobs).filter())
    for x in sess.query(Jobs).all():
        data.append([x.id, x.job, x.team_leader, x.work_size, x.collaborators, x.is_finished])
    return render_template('main_page.html', form=form, data=data, lengh=len(data))


@app.route('/delete/<int:id>')
def deleting(id_n):
    print(id_n  )
    return redirect('/')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
