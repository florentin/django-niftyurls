# -*- coding: UTF-8 -*-
import signal, datetime, logging, os, sys, time, json, base64 #zlib, bz2,
from optparse import make_option
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from niftyurls.fetch_feed import FetchFeed
from niftyurls.models import Feed, Entry, MetaData
from niftyurls.settings import NIFTYURLS_LIMIT_POSTS

def alarm_handler(signum, frame):
    print 'Signal handler called with signal', signum
    signal.alarm(0)
    sys.exit(0)

signal.signal(signal.SIGALRM, alarm_handler)
signal.alarm(60*30) # run for maximul 30 minutes
#connection.connection.text_factory = lambda x: unicode(x, "utf-8", "ignore")

class Command(BaseCommand):
    help = "Can be run as a cronjob or directly to download RSS feeds."
    option_list = BaseCommand.option_list + (
        make_option(
            '--verbose', action='store_true', dest='verbose', default=True,
            help='Log output to console.'
        ),
        make_option(
            '--limit', action='store', dest='limit', default=300,
            help='Feed limit'
        ),
    )
    def handle(self, **options):
        """
        Update the database with articles
        """
        # delete extra posts 
        for feed in Feed.objects.values('id'):
            excluded_entries = Entry.objects.filter(feed=feed['id']).order_by('-created', '-id')[:NIFTYURLS_LIMIT_POSTS]
            Entry.objects.filter(feed=feed['id']).exclude(pk__in=excluded_entries).delete()
        
        verbose = options.get('verbose', True)
        logging.basicConfig(
            filename='news_log.log',
            level=logging.INFO,
            format='%(asctime)s %(levelname)-8s %(message)s',
        )
        
        if verbose:
            console = logging.StreamHandler()
            console.setLevel(logging.INFO)
            formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
            console.setFormatter(formatter)
            logging.getLogger('').addHandler(console)

        logging.info('Download starting')
        #total_start = time.time()
        #new_articles = 0
        
        entry_type = ContentType.objects.get(app_label="niftyurls", model="entry")
        dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime) else None
        
        from django.db import connection
        connection.connection.text_factory = str
        
        for feed in Feed.objects.filter(is_published=True).order_by("last_downloaded")[0:options.get('limit')]: #.filter(slug='hackernews')
            logging.info("Processing feed: %s" % (feed.title))
            start = time.time()
            logging.info("Downloading: %s" % feed.link)
            try:
                fetch = FetchFeed(feed.link, feed.page_url)
                fetch.fetch_feed()
            except: #NiftyUrlsException
                logging.error("Error occurred processing %s" % feed.link)
            
            for entry in fetch.data.entries:
                try:
                    entry = fetch.sanitize_item(entry)
                except:
                    continue
                entry_obj, created = Entry.objects.get_or_create(guid=entry['guid'], feed=feed, defaults=entry)
                try:
                    #zlib.compress
                    #base64.standard_b64encode
                    metadata_value = json.dumps(entry.items(), default=dthandler)
                    #MetaData.objects.get_or_create(content_type=entry_type, object_id=entry_obj.pk, key='entry', defaults={'value':metadata_value})
                except Exception as ex:
                    #raise ex
                    pass
            feed.last_downloaded = datetime.datetime.now()
            feed.save()
            
            end = time.time()
            logging.info("This feed processing took %fs" % (end - start))
            time.sleep(2) # wait a bit, don't lock the database
            
        #total_end = time.time()
