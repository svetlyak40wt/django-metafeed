from itertools import chain
from pdb import set_trace

from django.utils.feedgenerator import Atom1Feed
from django.contrib.syndication.feeds import Feed

class MetaForMeta(type):
    def __new__(cls, name, bases, dct):
        item_attrs = [
            'item_author_email',
            'item_author_link',
            'item_author_name',
            'item_categories',
            'item_copyright',
            'item_enclosure_length',
            'item_enclosure_mime_type',
            'item_enclosure_url',
            'item_guid',
            'item_link',
            'item_pubdate',
        ]

        new_class = type.__new__(cls, name, bases, dct)

        def gen_method(name):
            def met(self, item):
                func = getattr(item._feed, name)
                if func is None:
                    raise AttributeError( 'Attribute %s not found' % name)
                return func(item)
            return met

        import copy

        for attrname in item_attrs:
            _func = gen_method(attrname)
            new_class.add_to_class(attrname, _func)
            print '%r %r %r' % (attrname, _func, getattr(new_class, attrname))
#            set_trace()
#            setattr(
#                new_class,
#                attrname,
#                copy.deepcopy(_func)
#            )

        assert(not getattr(new_class, 'item_link') is getattr(new_class, 'item_pubdate'))
        return new_class

    def add_to_class(cls, name, value):
        setattr(cls, name, value)



class MetaFeed(Feed):
    __metaclass__ = MetaForMeta
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
        def patch_item(item, feed):
            setattr(item, '_feed', feed)
            return item

        items = list(chain(
            *((patch_item(item, feed) for item in feed.items())
                for feed in self.feeds)
        ))
        set_trace()
        return items


    def item_link(self, item):
        return item._feed.item_link(item)


assert(not getattr(MetaFeed, 'item_link') is getattr(MetaFeed, 'item_pubdate'))
