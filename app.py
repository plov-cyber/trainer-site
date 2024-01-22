from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
import logging

from data import db_session
from data.option import Option
from data.question import Question
from data.user import User
from data.test import Test
from data.idiom import Idiom

from forms.reg_form import RegisterForm
from forms.login_form import LoginForm
from forms.change_pwd_form import ChangePasswordForm
from forms.create_test_form import CreateTestForm
from forms.add_question_form import AddQuestionForm
from forms.add_idiom_form import AddIdiomForm

from secret_key import secret_key

logging.basicConfig(filename='error.log', level=logging.DEBUG)

application = Flask(__name__)
application.config['SECRET_KEY'] = secret_key

login_manager = LoginManager()
login_manager.init_app(application)

db_session.global_init("sqlite.db")


@login_manager.user_loader
def load_user(user_id):
    """Менеджер авторизации."""
    session = db_session.create_session()

    user = session.get(User, user_id)

    session.close()
    return user


@application.route('/')
def index():
    return redirect('/my_tests')


# ERROR HANDLING
# ==================================================

@application.errorhandler(404)
def not_found(error):
    """Отлавливает ошибку 404 Not Found. Возвращает страницу с сообщением об ошибке."""
    return render_template('error.html', error=str(error).split(': ')), 404


@application.errorhandler(500)
def bad_request(error):
    """Отлавливает ошибку 500 Bad Request. Возвращает страницу с сообщением об ошибке."""
    return render_template('error.html', error=str(error).split(': ')), 500


@application.errorhandler(401)
def unauthorized(error):
    """Отлавливает ошибку 401 Unauthorized. Перенаправляет пользователя на страницу для входа."""
    return redirect('/login')


# ==================================================


# TESTS
# ==================================================

@application.route('/my_tests', methods=['GET'])
@login_required
def my_tests():
    session = db_session.create_session()
    user = session.get(User, current_user.id)

    if current_user.is_teacher:
        tests = user.tests_created
    else:
        tests = user.tests_available

    return render_template('my_tests.html', tests=tests, title='Мои тесты')


@application.route('/create_test', methods=['GET', 'POST'])
@login_required
def create_test():
    if not current_user.is_teacher:
        return redirect('/my_tests')

    test_form = CreateTestForm()

    if test_form.validate_on_submit():
        session = db_session.create_session()

        tests = session.query(Test).filter(Test.name == test_form.name.data).all()
        if len(tests) > 0:
            return render_template('create_test.html', test_form=test_form, title='Создание теста',
                                   message="Тест с таким названием уже существует :(")

        new_test = Test(
            name=test_form.name.data.strip(),
            creator_id=current_user.id
        )

        session.add(new_test)
        session.commit()

        test_id = new_test.id

        session.close()

        return redirect(f'/add_questions/{test_id}')

    return render_template('create_test.html', test_form=test_form, title='Создание теста')


@application.route('/take_test/<int:test_id>', methods=['GET', 'POST'])
@login_required
def take_test(test_id):
    pass


@application.route('/delete_test/<int:test_id>', methods=['GET'])
@login_required
def delete_test(test_id):
    if not current_user.is_teacher:
        return redirect('/login')

    session = db_session.create_session()

    test = session.get(Test, test_id)

    if test.creator_id != current_user.id:
        return redirect('/login')

    session.delete(test)
    session.commit()
    session.close()

    return redirect(request.referrer)


# ==================================================


# QUESTIONS
# ==================================================

@application.route('/add_questions/<int:test_id>', methods=['GET', 'POST'])
@login_required
def add_questions(test_id):
    if not current_user.is_teacher:
        return redirect('/login')

    form = AddQuestionForm()

    session = db_session.create_session()

    if form.validate_on_submit():
        idiom = session.get(Idiom, form.idiom.data)

        new_question = Question(
            idiom_id=idiom.id,
            answer=idiom.text,
            test_id=test_id
        )
        session.add(new_question)
        session.commit()

        correct_option = Option(
            question_id=new_question.id,
            text=idiom.meaning
        )
        session.add(correct_option)
        session.commit()

        for opt in form.options.data:
            opt = opt.strip()

            if opt:
                new_option = Option(
                    question_id=new_question.id,
                    text=opt
                )
                session.add(new_option)
                session.commit()

        session.close()

        return redirect(f'/add_questions/{test_id}')

    test = session.get(Test, test_id)
    form.idiom.choices = [
        (idiom.id, idiom.text)
        for idiom in session.query(Idiom).filter(Idiom.creator_id == current_user.id).all()
    ]

    return render_template('add_question.html',
                           form=form, questions=test.questions, title='Добавление вопроса')


@application.route('/delete_question/<int:question_id>', methods=['GET'])
@login_required
def delete_question(question_id):
    if not current_user.is_teacher:
        return redirect("/login")

    session = db_session.create_session()

    question = session.get(Question, question_id)

    if question.test.creator_id != current_user.id:
        return redirect('/login')

    session.delete(question)
    session.commit()
    session.close()

    return redirect(request.referrer)


# ==================================================


# IDIOMS
# ==================================================

@application.route('/my_idioms', methods=['GET'])
@login_required
def my_idioms():
    if not current_user.is_teacher:
        return redirect('/login')

    session = db_session.create_session()
    user = session.get(User, current_user.id)
    idioms = user.idioms

    return render_template('my_idioms.html', idioms=idioms)


@application.route('/add_idiom', methods=['GET', 'POST'])
@login_required
def add_idiom():
    if not current_user.is_teacher:
        return redirect('/my_tests')

    form = AddIdiomForm()

    if form.validate_on_submit():
        session = db_session.create_session()

        idioms = session.query(Idiom).filter(Idiom.text == form.text.data).all()
        if len(idioms) > 0:
            return render_template('add_idiom.html', form=form, title='Добавление идиомы',
                                   message="Такая идиома уже существует :(")

        new_idiom = Idiom(
            text=form.text.data,
            meaning=form.meaning.data,
            creator_id=current_user.id
        )

        session.add(new_idiom)
        session.commit()
        session.close()

        return redirect('/my_idioms')

    return render_template('add_idiom.html', form=form, title='Добавление идиомы')


@application.route('/delete_idiom/<int:idiom_id>', methods=['GET'])
@login_required
def delete_idiom(idiom_id):
    if not current_user.is_teacher:
        return redirect('/login')

    session = db_session.create_session()

    idiom = session.get(Idiom, idiom_id)

    if idiom.creator_id != current_user.id:
        return redirect('/login')

    session.delete(idiom)
    session.commit()
    session.close()

    return redirect(request.referrer)


# ==================================================


# RESULTS
# ==================================================

@application.route('/pupils_results', methods=['GET'])
@login_required
def pupils_results():
    if not current_user.is_teacher:
        return redirect('/login')

    # заглушка
    return redirect('/my_tests')


@application.route('/my_results', methods=['GET'])
@login_required
def my_results():
    # заглушка
    return redirect('/my_tests')


# ==================================================


# AUTHENTICATION
# ==================================================


@application.route('/register', methods=['GET', 'POST'])
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


@application.route('/login', methods=['GET', 'POST'])
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


@application.route('/logout')
@login_required
def logout():
    """Страница для выхода пользователя."""
    logout_user()
    return redirect('/login')


# ==================================================


# PROFILE
# ==================================================


@application.route('/settings', methods=['GET', 'POST'])
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


@application.route('/delete_profile/<int:user_id>')
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
    application.run(host='0.0.0.0')
    # application.run(port=8080, debug=True)
