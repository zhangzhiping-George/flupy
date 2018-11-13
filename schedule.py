import warnings
import osconfeed

from argparse import Namespace

'''
class Record:
    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)
'''

DB_NAME = 'data/schedule1_db'
CONFERENCE = 'conference.115'

def load_db(db):    
    raw_feed = osconfeed.load()
    warnings.warn('loading ' + DB_NAME)
    for collection, rec_list in raw_feed['Schedule'].items():
        record_type = collection[:-1]
        for record in rec_list:
            key = '{}.{}'.format(record_type, record['serial'])
            record['serial'] = key
            #db[key] = Record(**record)
            db[key] = Namespace(**record)

import shelve

db = shelve.open(DB_NAME)

if CONFERENCE not in db:
    load_db(db)

speaker = db['speaker.3471']

print(type(speaker))
print(speaker.name, speaker.twitter)

