from flask import (Flask, session, request, render_template,
                   send_from_directory, redirect, flash)
import os
from dbcm import UseDatabase, ConnectionError, CredentialError, SQLError
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['dbconfig'] = {'host': '127.0.0.1',
                          'user': 'avilio',
                          'password': 'Avilio@9711',
                          'database': 'linux'}
app.permanent_session_lifetime = timedelta(days=21)


@app.route('/favicon.ico')
def favicon() -> 'icon':
    return send_from_directory(os.path.join(app.root_path, 'static/img'),
                               'favicon.ico', mimetype='image')


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login() -> 'html':
    if 'user' in session:
        return redirect('/home')
    if request.method == 'POST':
        try:
            with UseDatabase(app.config['dbconfig']) as cursor:
                QUERY = """select password from user
                        where email = %s"""
                cursor.execute(QUERY, (request.form['email'],))
                data = cursor.fetchone()

            if data and check_password_hash(data[0], request.form['password']):
                session['user'] = request.form['email']
                if request.form.getlist('remember'):
                    session.permanent = True
                else:
                    session.permanent = False

                flash('Login Successfully')
                return redirect('/home')
            else:
                flash('Wrong email or password')
                return redirect('/login')

        except ConnectionError as err:
            print('Is your Database on? Error:', err)
        except CredentialError as err:
            print('User-id/Password issue. Error:', err)
        except SQLError as err:
            print('Check your query. Error:', err)
        except Exception as err:
            print('Something went wrong. Error:', err)

    return render_template('login.html')


@app.route('/home')
def home() -> None:
    if 'user' in session:
        return render_template('home.html')
    return redirect('/')


@app.route('/signup', methods=['GET', 'POST'])
def signup() -> None:
    if 'user' in session:
        return redirect('/home')
    if request.method == 'POST':
        try:
            with UseDatabase(app.config['dbconfig']) as cursor:
                QUERY = """select email from user where email=%s"""
                cursor.execute(QUERY, (request.form['email'],))
                email = cursor.fetchone()
                if email:
                    flash('Email already registered')
                    return redirect('/signup')
                QUERY = """insert into user
                            (email, password, fname, lname)
                            values (%s, %s, %s, %s)"""
                password = generate_password_hash(request.form['password'],
                                                  method='sha256')
                cursor.execute(QUERY, (request.form['email'],
                                       password,
                                       request.form['fname'],
                                       request.form['lname']))
                flash('Sign up Successfully')
                session['user'] = request.form['email']
                return redirect('/home')
        except ConnectionError as err:
            print('Is your Database on? Error:', err)
        except CredentialError as err:
            print('User-id/Password issue. Error:', err)
        except SQLError as err:
            print('Check your query. Error:', err)
        except Exception as err:
            print('Something went wrong. Error:', err)
        flash('Server failed, Try again.')
        return redirect('/signup')
    return render_template('signup.html')


@app.route('/logout')
def logout() -> None:
    if 'user' in session:
        session.pop('user')
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
