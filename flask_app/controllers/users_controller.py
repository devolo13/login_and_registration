from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.user_model import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


# default page for users who aren't logged in
@app.route('/')
def login_page():
    return render_template('login.html')


# route for verifying user inputs, adding them to the db, then redirecting to their page
@app.route('/register_user', methods=['POST'])
def register_new_user():
    # format user inputs into the standard format
    # we get first_name, last_name, email, password, confirm_password fields
    data = {
        **request.form
    }
    # test if the users inputs were valid
    if User.validate_registration_inputs(data):
        # if user input was valid, add them to the db and redirect to their page
        data['password'] = bcrypt.generate_password_hash(data['password'])
        user_id = User.save(data)
        session['user_id'] = user_id
        return redirect(f'/users/{user_id}')
    else:
        # if user input was not valid, show errors and redirect back to registration/login page
        return redirect('/')


# route for logging in existing users and redirecting to their page
@app.route('/login_user', methods=['POST'])
def login_user():
    # format user inputs into the standard format
    # we will only get back 'email' and 'password' forms
    data = {
        'email': request.form['login_email'],
        'password': request.form['login_password']
    }
    # get a list of all user emails & passwords
    # this could be more efficient by looking for the email directly on the sql db
    logins = User.get_all_logins()
    # search for user's email in list of emails
    for user in range(len(logins)):
        # if the given email was found in our db
        if data['email'] == logins[user]['email']:
            # check if the password is correct for that user
            if bcrypt.check_password_hash(logins[user]['password'], data['password']):
                # password is correct. store the user's id in session and redirect them to their page
                user_id = logins[user]['id']
                session['user_id'] = user_id
                return redirect(f'/users/{user_id}')
            else:
                # password is incorrect. show them an error and ask them to log in again
                flash('Incorrect password', 'login_password')
                return redirect('/')
    # that email was not found in db. show an error and send them back to the login page
    flash('Email not found', 'login_email')
    return redirect('/')


# page for an individual user
@app.route('/users/<int:id>')
def logged_in_user_page(id):
    if session['user_id'] == id:
        # we have the correct user. get the user object and render their page
        user = User.get_by_id(id)
        return render_template('single_user.html', user=user)
    else:
        # this user doesn't have access to this page. send them to the login page
        return redirect('/')


# route for logging out a user and redirecting to login page
@app.route('/logout')
def log_out_a_user():
    session.clear()
    return redirect('/')
