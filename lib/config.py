from ConfigParser import RawConfigParser
import sys
from os import path


confdir = path.dirname(__file__)
confdir = path.join(confdir, '..')

default_values = {
'database':{
    'server':   'localhost',
    'username': '',
    'password': '',
    'database': '',
    'port': 5432,
    }
}

config = RawConfigParser(allow_no_value=False)
config.readfp(open(path.join(confdir, 'config.cfg'), 'r'))
