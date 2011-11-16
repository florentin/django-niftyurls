import os
from django.conf import settings

temp_settings = {'example.com': {'rows': '3', 'title': 'Welcome', 'h1': 'Hello'}}
temp_settings.update(getattr(settings, 'NIFTYURLS_SETTINGS', {}))

NIFTYURLS_MEDIA  = getattr(settings, 'NIFTYURLS_MEDIA', 
                           os.path.join(settings.MEDIA_URL, 'niftyurls')+"/")
NIFTYURLS_SETTINGS = temp_settings
NIFTYURLS_LIMIT_POSTS  = getattr(settings, 'NIFTYURLS_LIMIT_POSTS', 40) # keep maximum 40 articles in db

default_js = ['http://ajax.googleapis.com/ajax/libs/jquery/1.5/jquery.min.js',
              'http://cufon.shoqolate.com/js/cufon-yui.js',
              NIFTYURLS_MEDIA+'niftyurls/fonts/Museo.font.js',
              NIFTYURLS_MEDIA+'niftyurls/facebox/facebox.js',
              NIFTYURLS_MEDIA+'niftyurls/js/niftyurls.js',
]
default_css = ['http://yui.yahooapis.com/combo?3.3.0/build/cssreset/reset-min.css&3.3.0/build/cssfonts/fonts-min.css&3.3.0/build/cssgrids/grids-min.css&3.3.0/build/cssbase/base-min.css',
               NIFTYURLS_MEDIA+'niftyurls/css/style.css',
               NIFTYURLS_MEDIA+'niftyurls/facebox/facebox.css',
]

NIFTYURLS_JS  = getattr(settings, 'NIFTYURLS_JS', default_js)
NIFTYURLS_CSS  = getattr(settings, 'NIFTYURLS_CSS', default_css)
