from datetime import datetime as dt
from pdb import set_trace

from unittest import TestCase

from django.utils.feedgenerator import Atom1Feed
from django.contrib.syndication.feeds import Feed
from django.test import Client
from django.core.handlers.wsgi import WSGIRequest

from django_metafeed.feeds import MetaFeed


def request():
    environ = {
        'HTTP_COOKIE':       {},
        'PATH_INFO':         '/',
        'QUERY_STRING':      '',
        'REMOTE_ADDR':       '127.0.0.1',
        'REQUEST_METHOD':    'GET',
        'SCRIPT_NAME':       '',
        'SERVER_NAME':       'testserver',
        'SERVER_PORT':       '80',
        'SERVER_PROTOCOL':   'HTTP/1.1',
        'wsgi.version':      (1,0),
        'wsgi.url_scheme':   'http',
        'wsgi.errors':       [],
        'wsgi.multiprocess': True,
        'wsgi.multithread':  False,
        'wsgi.run_once':     False,
    }
    return WSGIRequest(environ)


class Item(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class BlogFeed(Feed):
    feed_type = Atom1Feed
    title = 'Blog feed'
    link = 'http://example.com/blog/'
    title_template = 'blog_title.html'
    description_template = 'blog_description.html'

    def items(self):
        return [
            Item(title = 'Second post', date = dt(2009, 10, 10)),
            Item(title = 'First post', date = dt(2009, 10, 5)),
        ]

    def item_pubdate(self, item):
        return item.date

    def item_link(self, item):
        return 'http://example.com/%s/' % item.title



class GalleryFeed(Feed):
    feed_type = Atom1Feed
    title = 'Gallery feed'
    link = 'http://example.com/gallery/'
    title_template = 'gallery_title.html'
    description_template = 'gallery_description.html'

    def items(self):
        return [
            Item(title = 'Second image', date = dt(2009, 10, 11)),
            Item(title = 'First image', date = dt(2009, 10, 6)),
        ]

    def item_pubdate(self, item):
        return item.date

    def item_link(self, item):
        return 'http://example.com/%s/' % item.title



class FullFeed(MetaFeed):
    feeds = (BlogFeed, GalleryFeed)
    title = 'Full feed'
    link = 'http://example.com/all/'



class FeedTests(TestCase):
    def testBlogFeedHasItems(self):
        client = Client()
        r = request()

        feed = BlogFeed('blog', r).get_feed('')
        self.assertEqual(2, len(feed.items))
        i = feed.items
        self.assertEqual('Blog: Second post\n', i[0]['title'])
        self.assertEqual('Blog: First post\n', i[1]['title'])

    def testMetaFeed(self):
        client = Client()
        r = request()

        feed = FullFeed('all', r).get_feed('')
        self.assertEqual(Atom1Feed, type(feed))

        f = feed.feed
        self.assertEqual('Full feed', f['title'])
        self.assertEqual('http://example.com/all/', f['link'])

        i = feed.items
        self.assertEqual(4, len(i))
        self.assertEqual('Gallery: Second image\n', i[0]['title'])
        self.assertEqual('Blog: Second post\n',     i[1]['title'])
        self.assertEqual('Gallery: First image\n',  i[2]['title'])
        self.assertEqual('Blog: First post\n',      i[3]['title'])

