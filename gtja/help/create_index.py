#! /user/bin/env python

import pymongo
from pymongo import Connection


MONGODB_SERVER = "192.168.1.9"
MONGODB_PORT= 27017
MONGODB_DB = "gtja"
MONGODB_COLLECTION_REPORT_ABSTRACT = "report_abstract"
MONGODB_COLLECTION_REPORT_FILE = "report_file"
MONGODB_COLLECTION_REPORT_VISITED = "report_visited"

def create_index():
    connection = Connection(MONGODB_SERVER, MONGODB_PORT)
    db = connection[MONGODB_DB]
    abstract_collection = db[MONGODB_COLLECTION_REPORT_ABSTRACT]
    
    abstract_collection.create_index([("date", pymongo.DESCENDING)])

if __name__ == "__main__":
    create_index()