from datetime import datetime
from hashlib import sha1
from mongoengine import *

import int_to_alnum

class User(Document):
    login   = StringField(required=True, unique=True)
    api_key = StringField(required=True)
    email   = StringField(required=True)

class ShortPathConflict(Exception):
    def __init__(self, link):
        self.link = link

    def __str__(self):
        return 'Hash "%s" has already been bound.' % link.hash

class Link(Document):
    # FIXME: Add unit tests - WFU-1527

    hash       = StringField(required=True, unique=True)
    prefix     = StringField(required=True)
    short_path = StringField(required=True)
    long_url   = StringField(required=True)
    creator    = StringField(required=True)
    created_at = DateTimeField(required=True)

    meta = {
        'indexes': [('prefix', 'long_url')]
    }

    @classmethod
    def shorten(cls, long_url, short_path=None, prefix='', creator=None):
        if short_path is None:
            link = cls.objects(long_url=long_url, prefix=prefix).first()

            if link is None:
                link = cls.__create_with_random_short_path(long_url, prefix, creator)
        else:
            link, created = cls.__get_or_create(prefix, short_path, long_url, creator)

            if not created and link.long_url != long_url:
                raise ShortPathConflict(link)

        link.save()

        return link

    @classmethod
    def __create_with_random_short_path(cls, long_url, prefix, creator):
        while True:
            # Generate a seed from the long url and the current date (with milliseconds)
            seed   = long_url + str(datetime.utcnow())
            hashed = int(sha1(seed).hexdigest(), 16)
            mod    = 1

            while hashed > mod:
                mod *= 10
                short_path = int_to_alnum.encode(hashed % mod)

                link, created = cls.__get_or_create(prefix, short_path, long_url, creator)

                if created:
                    # Short path didn't exist, we're done
                    return link

    @classmethod
    def __get_or_create(cls, prefix, short_path, long_url, creator):
        return cls.objects.get_or_create(
            hash=Link.hash_for_prefix_and_short_path(prefix, short_path),
            defaults={
                'short_path': short_path,
                'prefix': prefix,
                'long_url': long_url,
                'creator': creator,
                'created_at': datetime.utcnow()})

    @classmethod
    def hash_for_prefix_and_short_path(prefix, short_path):
        return ('%s%s' % ('%s/' % prefix if prefix != '' else '', short_path)).lower()

    @classmethod
    def find_by_hash(cls, short_path):
        return cls.objects(hash=hash.lower()).first()

    def __str__(self):
        return "%s -> %s\n" % (self.hash, self.long_url)

class Click(Document):
    server     = StringField(required=True)
    full_path  = StringField(required=True)
    link       = ReferenceField('Link')
    created_at = DateTimeField(required=True)
    ip         = StringField(required=True)
    browser    = StringField()
    referer    = StringField()
    lang       = StringField()

    meta = {
        'cascade': False
    }
