#!/usr/bin/env python3
"""
Module that inserts a new document in a collection based on kwargs
"""


def insert_school(mongo_collection, **kwargs):
    """ Insert a document in Python"""
    return mongo_collection.insert(kwargs)
