Introduction
============

I've created this simple application to join RSS feeds from my blog and from my
photo gallery.

It can be used to merge two or more feeds together. Resulting feed will have all
items from the underlying feeds, but you can customize some fields like feed's
title, author, link, categories, etc.

Install It!
-----------

django-metafeed depends on...

...well it depends on the Django. Surprize!

Just install it using easy_install, pip, buildot or any other tool.

Next, add ``django_metafeed`` to your ``INSTALLED_APPS``.

Use It!
-------

To use django-metafeed, you need to create Feed and to add it to the urls.py.

First, create the feed. The most simple example::

    from blog.feeds import LatestArticlesFeed
    from gallery.feeds import LatestPhotosFeed

    class AllPosts(MetaFeed):
        feeds = (LatestArticlesFeed, LatestPhotosFeed)
        title = 'My posts and photos'
        link = '/'

Second, add this feed to the urls.py::

    from myproject.feeds import AllPosts

    all_posts = {'atom': AllPosts}

    (r'^feeds/all/$',
     'django.contrib.syndication.views.feed',
     {'feed_dict': all_posts, 'url': 'atom'}),

Well done! Now point your browser to the http://127.0.0.1:8000/feeds/all/ to see result.

.. _django: http://djangoproject.org
