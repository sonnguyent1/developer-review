
from flask import Flask
import sys
import ssl
import os
import logging

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context


app_search_logger = logging.getLogger('app_search')
app_search_logger.setLevel(logging.INFO)
fh = logging.FileHandler(os.path.join(os.environ.get('APP_LOG_DIR', ''), 'app_search.log'))
fh.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(message)s')
fh.setFormatter(formatter)
app_search_logger.addHandler(fh)


app = Flask(__name__)
application = app

# Setup the app with the config.py file
app.config.from_object('config')

from tw33t.views import main
