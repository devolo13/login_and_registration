from flask_app import app
from flask import render_template, redirect, request
from flask_app.models.user_model import User

# default page for users who aren't logged in
@app.route('/')
def login_page():
    # if user already logged in, reroute to their page
    # else render index.html
    return render_template('login.html')


# route for verifying user inputs, adding them to the db, then redirecting to ...?
@app.route('/register_user')
def register_new_user():
    # format user inputs into the standard format
    data = {
        **request.form
    }
    # what does our data look like? we should only get the registration data, not the login data
    print(data)
    # test if the users inputs were valid
    if User.validate_registration():
        # if user input was valid, add them to the db and redirect to their page
        user = User.add_new_user()
        redirect('single_user.html', user=user)
    else:
        # if user input was not validate, show errors and redirect back to registration/login page
        redirect('/')

# route for logging in existing users and redirecting to their page
@app.route('/login_user')
def login_user():
    # format user inputs into the standard format
    data = {
        **request.form
    }
    # see what data we got back. we only want the login data, not the registration data
    print(data)
    # see if our user exists in our database
    if data.email in User.get_all_emails:
        print(f"the email address {data.email} is in our database")
        # see if the password matches the existing users password
            # store the user's information in session
            # redirect them to their individual page
    else:
        print(F"the email address {data.email} is not in our database")
        # show the error and redirect to ('/')

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