#!/usr/bin/env python2

from flask import Flask, g
from os import path
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from model import Base, Entries

dbname = 'flaskr.db'
dbpath = path.join('/tmp',dbname)
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + dbpath

app = Flask(__name__)
app.config.from_object(__name__)
mydb = SQLAlchemy(app)

def connect_db():
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    return engine.connect()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.before_first_request
def setup():
    Base.metadata.drop_all(bind=mydb.engine)
    Base.metadata.create_all(bind=mydb.engine)
    mydb.session.add(Entries('First entry', 'Lorem ipsum'))
    mydb.session.commit()

import view
'''
if __name__ == '__main__':
    app.run()
'''
