# coding: utf-8

"""
Test case for MongoEngine

Adapted from https://github.com/MongoEngine/mongoengine/blob/master/mongoengine/django/tests.py
MongoEngine's license: https://github.com/MongoEngine/mongoengine/blob/master/LICENSE
"""

from __future__ import unicode_literals

from django.test import TestCase
from django.conf import settings
from mongoengine.connection import connect, disconnect


class MongoTestCase(TestCase):
    """
    TestCase class that clears the collection between the tests
    """

    db_name = 'test_%s' % settings.MONGOENGINE['db']

    def __init__(self, method_name='runtest'):
        disconnect()
        self.database = connect(self.db_name)[self.db_name]

        super(MongoTestCase, self).__init__(method_name)

    def _post_teardown(self):
        super(MongoTestCase, self)._post_teardown()

        for collection in self.database.collection_names():
            if collection == 'system.indexes':
                continue

            self.database.drop_collection(collection)

        disconnect()
