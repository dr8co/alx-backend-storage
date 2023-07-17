#!/usr/bin/env python3
"""
Module that returns the list of school having a specific topic
"""


def schools_by_topic(mongo_collection, topic):
    """Return the list of school having a specific topic"""
    documents = mongo_collection.find({"topics": topic})
    return list(documents)
