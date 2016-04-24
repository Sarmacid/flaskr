#!/usr/bin/env python2

#from flaskr import mydb
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Text

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

'''
from flaskr import mydb
import model
p = model.Entries(title='test', text='test message')
session.add(p)
session.commit()
'''
