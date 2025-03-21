from flask_pymongo import PyMongo

def initialize_db(app):
    mongo = PyMongo(app)
    return mongo
