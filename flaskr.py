#!/usr/bin/env python2

from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
from os import path
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from model import Base, Entries

DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/flaskr.db'

app = Flask(__name__)
app.config.from_object(__name__)
mydb = SQLAlchemy(app)

def connect_db():
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    return engine.connect()

@app.before_first_request
def setup():
    Base.metadata.drop_all(bind=mydb.engine)
    Base.metadata.create_all(bind=mydb.engine)
    mydb.session.add(Entries('First entry', 'Lorem ipsum'))
    mydb.session.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def show_entries():
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)
    
@app.route('/add', methods=['POST'])
def add_entry():
	if not session.get('logged_in'):
		abort(401)
	trans = g.db.begin()
	try:
		g.db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
		trans.commit()
		flash('New entry was successfully posted')
		return redirect(url_for('show_entries'))
	except:
		trans.rollback()
		raise

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)



@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))



if __name__ == '__main__':
    #setup()
    app.run()
