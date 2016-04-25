#!/usr/bin/env python2

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Text, String

Base = declarative_base()

class Entries(Base):
	__tablename__ = 'entries'
	id = Column(Integer, primary_key=True)
	title = Column(Text)
	text = Column(Text)

	def __init__(self, title=None, text=None):
		self.title = title
		self.text = text

	def __repr__(self):
		return '<Entry %r>' % (self.title)

class Users(Base):
	__tablename__ = 'users'
	id = Column(Integer, primary_key=True)
	username = Column(String(30), nullable=False, unique=True)
	password = Column(String(64), nullable=False)
	salt = Column(String(12), nullable=False)

	def __init__(self, username=None, password=None, salt='None'):
		self.username = username
		self.password = password
		self.salt = salt

	def __repr__(self):
		return '<Entry %r>' % (self.username)
