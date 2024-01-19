from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, logout_user, current_user, login_required

from data import db_session
from data.user import User
from data.test import Test

from forms.reg_form import RegisterForm
from forms.login_form import LoginForm
from forms.change_pwd_form import ChangePasswordForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    """Менеджер авторизации."""
    session = db_session.create_session()

    user = session.get(User, user_id)

    session.close()
    return user


def main():
    db_session.global_init("sqlite.db")
    app.run(debug=True)


@app.route('/')
def index():
    return redirect('/my_tests')


# ERROR HANDLING
# ==================================================


@app.errorhandler(404)
def not_found(error):
    """Отлавливает ошибку 404 Not Found. Возвращает страницу с сообщением об ошибке."""
    return render_template('error.html', error=str(error).split(': ')), 404


@app.errorhandler(500)
def bad_request(error):
    """Отлавливает ошибку 500 Bad Request. Возвращает страницу с сообщением об ошибке."""
    return render_template('error.html', error=str(error).split(': ')), 500


@app.errorhandler(401)
def unauthorized(error):
    """Отлавливает ошибку 401 Unauthorized. Перенаправляет пользователя на страницу для входа."""
    return redirect('/login')


# ==================================================

# TESTS
# ==================================================

@app.route('/my_tests', methods=['GET'])
@login_required
def my_tests():
    session = db_session.create_session()
    user = session.get(User, current_user.id)

    if current_user.is_teacher:
        tests = user.tests_created
    else:
        tests = user.tests_available

    return render_template('my_tests.html', tests=tests)


@app.route('/create_test', methods=['GET', 'POST'])
def create_test():
    pass


# ==================================================


@app.route('/my_idioms', methods=['GET'])
@login_required
def my_idioms():
    if not current_user.is_teacher:
        return redirect('/login')


@app.route('/pupils_results', methods=['GET'])
@login_required
def pupils_results():
    if not current_user.is_teacher:
        return redirect('/login')


# AUTHENTICATION
# ==================================================


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        session = db_session.create_session()

        if session.query(User).filter(User.login == form.login.data.strip()).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пользователь с таким логином уже существует :(")

        new_user = User(
            login=form.login.data.strip(),
            surname=form.surname.data.strip(),
            name=form.name.data.strip(),
            is_teacher=form.is_teacher.data
        )
        new_user.set_password(form.password.data)

        session.add(new_user)
        session.commit()
        session.close()

        return redirect('/login')
    return render_template('register.html', form=form, title='Регистрация')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/logout')

    form = LoginForm()

    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(
            User.login == form.login.data.strip()).first()

        if user and user.check_password(password=form.password.data):
            login_user(user, remember=form.remember_me.data)

            next_url = request.args.get('next', '/')
            return redirect(next_url)

        return render_template('login.html', title='Авторизация',
                               message='Неправильный логин или пароль',
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    """Страница для выхода пользователя."""
    logout_user()
    return redirect('/login')


# ==================================================

# PROFILE
# ==================================================


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    """Страница настроек пользователя."""
    form = ChangePasswordForm()

    if form.validate_on_submit():

        if current_user.check_password(form.old_password.data):

            if form.old_password.data != form.new_password.data:
                session = db_session.create_session()

                user = session.get(User, current_user.id)
                user.set_password(form.new_password.data)

                session.commit()
                session.close()

                return render_template('settings.html', title='Настройки', form=form,
                                       message='Пароль успешно изменён')
            return render_template('settings.html', title='Настройки', form=form,
                                   error='Старый и новый пароли совпадают!')
        return render_template('settings.html', title='Настройки', form=form,
                               error='Неверный пароль')
    return render_template('settings.html', title='Настройки', form=form)


@app.route('/delete_profile/<int:user_id>')
@login_required
def delete_profile(user_id):
    """Функция для удаления профиля пользователя."""
    logout_user()

    session = db_session.create_session()

    user = session.get(User, user_id)
    session.delete(user)

    session.commit()
    session.close()

    return redirect('/register')


# ==================================================

if __name__ == '__main__':
    main()
