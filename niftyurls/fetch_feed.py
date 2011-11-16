import socket
socket.setdefaulttimeout(60)
import datetime, time, urllib2, urlparse #, sys, json, zlib, signal
import feedparser

class NiftyUrlsException(Exception):
    pass

class FetchFeed(object):
    def __init__(self, link, page_url=None):
        self.link = link
        self.page_url = page_url # useful for deciding on getting the real url or not
        self.page_url_parsed = urlparse.urlparse(self.page_url)

    def get_item_summary(self, item):
        summary = ''
        if hasattr(item, "summary"):
            summary = item.summary
        elif hasattr(item, "content"):
            summary = item.content[0].value
        elif hasattr(item, "description"):
            summary = item.description
        return summary
    
    def get_item_pubdate(self, item):
        pubdate = None
        attrs = ['updated_parsed', 'published_parsed', 'date_parsed', 
                 'created_parsed']
        
        for attr in attrs:
            if hasattr(item, attr):
                pubdate = getattr(item, attr)
                break
        
        if pubdate:
            try:
                ts = time.mktime(pubdate)
                return datetime.datetime.fromtimestamp(ts)
            except TypeError:
                pass
        
        return datetime.datetime.now()
    
    def get_final_url(self, entry):
        entry_link_parsed = urlparse.urlparse(entry.link)
        if entry_link_parsed.hostname!=self.page_url_parsed.hostname:
            u = urllib2.urlopen(entry.link)
            entry_link = u.geturl() # get the real url
            u.close()
        else:
            entry_link = entry.link
        return entry_link
        
    def sanitize_item(self, entry):
        #entry_link = self.get_final_url(entry)
        entry_link = entry.link
        return {
            'title':        entry.title,
            'link':         entry_link,
            'description':  self.get_item_summary(entry), 
            'guid':         entry.get("id", entry.link),
            'pubdate':      self.get_item_pubdate(entry),
        }

    def fetch_feed(self):
        self.data = feedparser.parse(self.link)
        if 'bozo' in self.data and self.data.bozo:
            raise NiftyUrlsException('Error fetching %s' % self.link)
        return True

    """
    def fetch_feed(self):
        def timeout(signum, frame):
            raise NiftyUrlsException('Timeout fetching %s' % self.link)
        signal.signal(signal.SIGALRM, timeout)
        signal.alarm(65) # timeout in X seconds, in case that socket timeout isn't working
        try:
            self.data = feedparser.parse(self.link)
            if 'bozo' in self.data and self.data.bozo:
                raise NiftyUrlsException('Error fetching %s' % self.link)
        except Exception as e:
            signal.alarm(0)
            raise(e)
        
        return True
    """
