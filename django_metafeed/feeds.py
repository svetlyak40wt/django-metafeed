from itertools import chain
from pdb import set_trace

from django.utils.feedgenerator import Atom1Feed
from django.contrib.syndication.feeds import Feed



class MetaFeed(Feed):
    feeds = []
    feed_type = None

    def __init__(self, slug, request):
        super(MetaFeed, self).__init__(slug, request)
        self.feeds = [feed(slug, request) for feed in self.feeds]

        if len(self.feeds) < 2:
            raise ValueError('Please, specify two or more basic feeds')

        if self.feed_type is None:
            feed_types = set(feed.feed_type for feed in self.feeds)
            if len(feed_types) > 1:
                raise ValueError('Please, specify feeds '\
                    'with similar feed types or feed_type class attribute.')
            self.feed_type = feed_types.pop()

    def items(self):
        return []

    def get_feed(self, url = None):
        my = super(MetaFeed, self).get_feed(url)
        feeds = [feed.get_feed(url) for feed in self.feeds]

        for feed in feeds:
            for item in feed.items:
                my.items.append(item)

        my.items.sort(key = lambda x: x['pubdate'], reverse = True)

        return my

