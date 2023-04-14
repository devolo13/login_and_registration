from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
import re

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']

    # method for getting all users. returns an array of user objects
    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM users;'
        results = connectToMySQL(DATABASE).query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users
    
    # method for getting a single user by their id. returns user object
    @classmethod
    def get_by_id(cls,data):
        # may need a lot of tweaking
        query = 'SELECT * FROM users WHERE id = %(id)s'
        results = connectToMySQL(DATABASE).query_db(query, data)
        return cls(results)
    
    # method for getting all user emails. returns an array of email addresses
    @classmethod
    def get_all_emails(cls):
        query = "SELECT email FROM users;"
        results = connectToMySQL(DATABASE).query_db(query)
        # is this emails array necessary? do we get an array of emails back from the db?
        emails = []
        for email in results:
            emails.append(email)

    # method for validating user registration inputs
    @staticmethod
    def validate_registration_inputs(cls, data):
        valid_inputs = True
        # validate first name length
        if (len(data.first_name) < 2):
            # create an error flag for first_name length
            valid_inputs = False
        # validate last name length
        if (len(data.last_name) < 2):
            # create an error flag for last_name length
            valid_inputs = False
        # validate email format
        if not re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$').match(data.email):
            # create an error flag for email
            valid_inputs = False
        # validate password length
        if (len(data.password) < 8):
            # create an error flag for password length
            valid_inputs = False
        # validate password confirmation
        if data.password != data.confirm_password:
            # create an error flag for password matching
            valid_inputs = False
        return valid_inputs
    # NEEDS MORE CLASS METHODS AND A STATIC METHOD FOR VERIFYING REGISTRATION INPUTS