#!/usr/bin/env python2

from flask import request, session, g, redirect, url_for, \
	 abort, render_template, flash
from flaskr import app
from users import authenticate

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
		g.db.execute('insert into entries (title, text) values (?, ?)', \
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
		if authenticate(request.form['username'], request.form['password']) == 0:
			error = 'Invalid username or password'
		elif authenticate(request.form['username'], request.form['password']) == 1:
			session['logged_in'] = True
			flash('You were logged in')
			return redirect(url_for('show_entries'))
	return render_template('login.html', error=error)

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You were logged out')
	return redirect(url_for('show_entries'))
