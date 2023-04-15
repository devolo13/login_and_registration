from flask_app import app
from flask import render_template, redirect, request, flash
from flask_app.models.user_model import User

# default page for users who aren't logged in
@app.route('/')
def login_page():
    # if user already logged in, reroute to their page
    # else render index.html
    return render_template('login.html')


# route for verifying user inputs, adding them to the db, then redirecting to ...?
# error messages work. doesn't currently add anything to db or redirect correctly
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
        user = User.save(data)
        print(user)
        return redirect('single_user.html', user=user)
    else:
        # if user input was not validate, show errors and redirect back to registration/login page
        return redirect('/')

# route for logging in existing users and redirecting to their page
# needs session storage. works otherwise
# THESE ERROR MESSAGES GET TRIGGERED WHEN PRESSING REGISTER BUTTON AS WELL BUT DOESN'T LOG USER IN???
@app.route('/login_user', methods=['POST'])
def login_user():
    # format user inputs into the standard format
    # we will only get back 'email' and 'password' forms
    data = {
        'email': request.form['login_email'],
        'password': request.form['login_password']
    }
    # get a list of all user emails & passwords
    logins = User.get_all_logins()
    # search for user's email in list of emails
    for user in range(len(logins)):
        # if the given email was found in our db
        if data['email'] == logins[user]['email']:
            print('found a match for the email')
            # check if the password is correct for that user
            if data['password'] == logins[user]['password']:
                # password is correct. store stuff in session and redirect them to their page
                user_id = logins[user]['id']
                return redirect(f'/user/{user_id}')
            else:
                # password is incorrect. show them an error and ask them to log in again
                flash('Incorrect password', 'login_password')
                return redirect('/')
    # assume that email was not found in db
    flash('Email not found', 'login_email')
    return redirect ('/')

# page for an individual user
@app.route('/users/<int:id>')
def logged_in_user_page():
    # get the user object to pass through
    user = User.get_by_id(id)
    return render_template('single_user.html', user=user)

# route for logging out a user and redirecting to login page
@app.route('/logout')
def log_out_a_user():
    # clear out the session
    return redirect('/')