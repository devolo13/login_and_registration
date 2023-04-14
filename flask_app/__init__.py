from flask import Flask

app = Flask(__name__)
app.secret_key = 'Harry Potter was mid'

# NEED TO CHANGE DATABASE
DATABASE = 'users_schema'