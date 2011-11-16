import re, sys

from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site
from django import template

from niftyurls.models import Feed
from niftyurls.settings import NIFTYURLS_SETTINGS, NIFTYURLS_JS, \
                                NIFTYURLS_CSS, NIFTYURLS_MEDIA

register = template.Library()

def replace( string, args ): 
    search  = args.split(args[0])[1]
    replace = args.split(args[0])[2]
    return re.sub( search, replace, string )

register.filter('replace', replace)

def get_site(context):
    domain = RequestSite(context['request']).domain.replace('www.', '')
    try:
        current_site = Site.objects.get(domain=domain)
    except Site.DoesNotExist:
        current_site = Site.objects.get(domain='example.com')
    return current_site

def get_settings(context):
    domain = RequestSite(context['request']).domain.replace('www.', '')
    if not context.render_context.get(domain):
        settings = dict(NIFTYURLS_SETTINGS).get('example.com', {})
        settings.update(dict(NIFTYURLS_SETTINGS).get(domain, {}))
        context.render_context[domain] = settings

    return context.render_context.get(domain)

def niftyurls_content(context):
    settings = get_settings(context)
    current_site = get_site(context)
    
    feeds = Feed.objects.filter(sites=current_site)
    """ filter feeds with less than N entries """
    feeds = filter(lambda feed: feed.entry_set.count()>4, feeds)
    
    rows_settings = settings.get('rows', 3)
    
    feeds_per_row = []
    start = 0
    """
    3,2 means 3 rows, 3 columns on the first row, 2 columns on the second row 
    """
    columns = rows_settings.split(',')
    while len(columns) < len(feeds):
        columns.append(columns[-1]) # repeat the last number of columns

    for col in columns:
        end = start+int(col)
        feeds_per_row.append(feeds[start:end])
        start = end
    
    extra_context = {
                     'rows':feeds_per_row,
                     'current_site': current_site,
                     'NIFTYURLS_MEDIA': NIFTYURLS_MEDIA,
                    } 
    context.update(extra_context)
    return context

def niftyurls_media(args):
    context = {}
    
    if 'js' in args:
        context.update(dict(js_files=list(NIFTYURLS_JS)))
    if 'css' in args:
        context.update(dict(css_files=list(NIFTYURLS_CSS)))
    
    return context

def niftyurls_settings(parser, token):
    try:
       tag_name, arg = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires a single argument" % token.contents.split()[0]

    return NiftySettings(arg)

class NiftySettings(template.Node):
    def __init__(self, arg):
        self.arg = arg

    def render(self, context):
        settings = get_settings(context)
        return settings.get(self.arg, None)
    
    
register.inclusion_tag('niftyurls/content.html', takes_context = True)(niftyurls_content)
register.inclusion_tag('niftyurls/media.html')(niftyurls_media)
register.tag('niftyurls_settings', niftyurls_settings)
