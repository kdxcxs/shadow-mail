import os

class Config(object):
    DATABASE_PATH = os.getenv('DATABASE_PATH') or 'sqlite:///./shadowmail.db'
    MAILDIR = os.getenv('MAILDIR')
