#!/usr/bin/env python2
from sqlalchemy.sql import select
from flask import g
from model import Users

def authenticate(username, password):
    '''
    Returns:
    0: Unsuccessful authentication
    1: Succesful authentication
    Other: Error
    '''
    s = select([Users]).where(Users.username==username and Users.password==password)
    result = [r[0] for r in g.db.execute(s)]
    return len(result)
