from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    current_app,
    flash,
)
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from functools import wraps
from app.models.models import User
from werkzeug.utils import secure_filename
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from urllib.parse import urlsplit
import uuid
import os

bp = Blueprint("routes", __name__)

def with_db(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        db = current_app.extensions['sqlalchemy']
        return func(db, *args, **kwargs)
    return wrapper

@bp.route("/")
@bp.route("/home")
def home():
    return render_template("index.html")


@bp.route("/login", methods=["GET", "POST"])
@with_db
def login(db):
    if current_user.is_authenticated:
        return redirect(url_for("routes.home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data)
        )
        if user is None or not user.check_password(form.password.data):
            # error_message = 'Неправильный логин или пароль'
            flash("Неправильный логин или пароль")
            return redirect(url_for("routes.login"))
        login_user(user, remember=form.remember_me.data)
        flash(
            "Добро пожаловать, {}! Запомнить меня={}".format(
                form.username.data, form.remember_me.data
            )
        )
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('routes.home')
        return redirect(next_page)

    return render_template("login.html", title="Sing In", form=form)


@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("routes.home"))

@bp.route("/registration", methods=["GET", "POST"])
@with_db
def registration(db):
    form = RegistrationForm()
    if form.validate_on_submit():
        user_exist = db.session.scalar(sa.select(User).where(
            User.username == form.username.data))
        if user_exist is not None:
            form.username.errors.append('Этот логин уже занят')
            return render_template('registration.html', form=form)
        
        email_exist = db.session.scalar(sa.select(User).where(
            User.email == form.email.data))
        if email_exist is not None:
            form.email.errors.append('Эта почта уже используется')
            return render_template('registration.html', form=form)
        
        user = User(username = form.username.data, email = form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash("Вы зарегистрированы!")
        return redirect(url_for('routes.login'))
    return render_template('registration.html', form=form)

@bp.route('/user/<username>')
@login_required
@with_db
def user(db, username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    looks = [
        {'author': user, 'name': 'Test look #1'},
        {'author': user, 'name': 'Test look #2'}
    ]
    return render_template('user.html', user=user, looks=looks)

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
@with_db
def edit_profile(db):
    form = EditProfileForm()
    if form.cancel.data:
        flash('Редактирование отменено')
        return redirect(url_for('routes.user', username=current_user.username))
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        # current_user.password = form.password.data
        db.session.commit()
        flash('Изменения сохранены')
        return redirect(url_for('routes.user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('edit_profile.html', title='Редактирование профиля',
                           form=form)

@bp.route("/about")
def about():
    return render_template("about.html")


@bp.route("/gen")
@login_required
def gen():
    return render_template("gen.html")


@bp.route("/upload", methods=["POST"])
def upload():
    if "photo" not in request.files:
        return redirect("/")

    file = request.files["photo"]
    if file.filename == "":
        return redirect("/")

    if not file.filename.lower().endswith((".jpg", ".png", ".jpeg")):
        return "Только изображения (JPG/PNG)!"

    os.makedirs(current_app.config["UPLOAD_FOLDER"], exist_ok=True)

    filename = f"{uuid.uuid4()}_{secure_filename(file.filename)}"
    file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))
    return render_template("gen.html", uploaded_image=filename)


def register_routes(app):
    app.register_blueprint(bp)