#!/usr/bin/env python3
"""
Module that changes all topics of a school document based on the name
"""


def update_topics(mongo_collection, name, topics):
    """ Update a document in Python"""
    query = {"name": name}
    new_values = {"$set": {"topics": topics}}

    mongo_collection.update_many(query, new_values)
