#Hello and welcome

Niftyurls is a popurls-style script built entirely with Django.

#View some examples

* [JavascriptNews][www.JavascriptNews.com]
* [PythonDaddy][www.PythonDaddy.com]

#Excerpt from the popurls site:

> "... is the dashboard for the latest web-buzz, a single page that encapsulates up-to-the-minute headlines from the most popular sites on the internet."

#Unique features

* Powered by Django
* No tooltips by default, there are better ways of reading the text
* Read the news in a Facebook-style lightbox ("pop" layout)
* Read the news in a clean page ("page" layout)
* Easy editable feed settings, titles, urls, positions in the page
* Javascript assisted by jQuery
* Grid templates provided by Yui3 Grids
* Fast text replacement with Cufon

#Wish list

* remember visitor's last viewed links, mark new/old links
* show new links only
* videos support
* admin interface for feed configuration, more config options
* multiple domain support
* site search with database support
* usability improvements
* user accounts, openid support
* code comments, svn support

#Installation (linux, localhost)

1. Make sure you have the following Python packages available: Django - http://pypi.python.org/pypi/Django/ Pil - http://pypi.python.org/pypi/PIL/ Feedparser - http://pypi.python.org/pypi/feedparser/ You may install these with the "pip" tool (http://pypi.python.org/pypi/pip/) $ pip install "django>=1.3" $ pip install pil $ pip install feedparser
2. Add "niftyurls" to the INSTALLED_APPS tuple. The Niftyurls application depends on the following Django packages: 'django.contrib.staticfiles' 'django.contrib.admin' To make sure every app is enabled, add the following line to your project's "settings.py" file: INSTALLED_APPS += ('django.contrib.staticfiles', 'django.contrib.admin', 'niftyurls', )
3. Synchronize the database $ python manage.py syncdb
4. To add the "niftyurls" in your templates, use the following:
{% load niftyurls_tags %} {% niftyurls_media "js,css" %} {% niftyurls_content %}

5. Please check the available Niftyurls settings in niftyurls/settings.py You may add custom values to NIFTYURLS_SETTINGS (please see niftyurls/settings.py) and retrive them inside your templates with: {% niftyurls_settings title %} {% niftyurls_settings h1 %}
6. Add some feeds in the admin interface http://127.0.0.1:8000/admin/niftyurls/feed/add/ Here are some feed urls examples: - http://feeds.delicious.com/v2/rss/popular/python?count=15 - http://www.reddit.com/.rss
7. Run the following command so that fresh entries are added to the database. $ python manage.py niftyurls_feeds
8. Niftyurls templatetags depend on the existing of the "request" inside the templates, in case of errors verify that you have passed the "RequestContext" to the templates. http://docs.djangoproject.com/en/dev/ref/templates/api/#subclassing-context-requestcontext Make sure the TEMPLATE_CONTEXT_PROCESSORS contains the following: ('django.core.context_processors.request', 'django.contrib.auth.context_processors.auth',)
