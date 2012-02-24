import os
import sys
import logging
import itertools

#Boolean value denoting debug status. Used for Django debug status too
ENV_DEBUG = True

#Database settings
DB_NAME = 'milesense'
DB_USER = 'postgres'
DB_PASSWORD = ''
DB_HOST = ''
DB_PORT = '6543'

AUTHENTICATION_BACKENDS = (
    'modechoice.backends.CaseInsensitiveModelBackend',
)

#For django-debug-toolbar
#INTERNAL_IPS = ('127.0.0.1',)
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

MODECHOICE_BASE = os.path.abspath(os.path.dirname(__file__))

# Find the install directory and add it to PYTHONPATH
lib_path = MODECHOICE_BASE + '/lib'
if lib_path not in sys.path:
    sys.path.append(lib_path)

# Location of static media files
MC_MEDIA_FILES = MODECHOICE_BASE + '/static'

API_SECRET_KEY = 'fswehw7et912ur2rf7#Y@^nfhfbqwme34f&HB&T24gvdkk'

#LOG_FILE = '/var/log/apps/modechoice/modechoice.log'
LOG_FILE = '/home/milesense/logs/web-env/modechoice.log'
logging.basicConfig(
    level = logging.DEBUG,
    format = '%(asctime)s %(levelname)s %(message)s',
    filename = LOG_FILE,
)

# Doc root for static files
STATIC_DOC_ROOT = MODECHOICE_BASE + '/static'

# Default sender e-mail ID
SENDER_EMAIL_ID = '"MileSense" <support@milesense.com>'
TEAM_MAIL_IDS = 'thejo@milesense.com,david@milesense.com,jerry@milesense.com,ram@milesense.com'

# Company name
COMPANY_NAME = "MileSense"
# Domain
DOMAIN = 'milesense.com'

#Amazon Web Services
AWS_ACCESS_KEY = 'AKIAIA5RYAWC22XG4SMA'
AWS_SECRET_KEY = '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'
AWS_IMAGE_URL_BASE = 'http://s3.amazonaws.com/com.milesense.images'

# Mailgun API Key
MAILGUN_API_KEY = "key-3b2hdhv60rtzq-d3-1"

# Browsers that we don't support
UNSUPPORTED_BROWSERS = ["MSIE 5", "MSIE 6", "MSIE 7", "MSIE 8"]

STAFF_GROUP_ID = 2
CUSTOMER_GROUP_ID = 3
TRIPOGRAPHY_GROUP_ID = 4
APPROVER_GROUP_NAME = 'Approvers'

# Java server endpoint
JAVA_SERVER_ENDPOINT = 'http://127.0.0.1:9000'

ATOMIC_COUNTER = itertools.count()

#Generate a unique request ID which can be pre-prended to log messages
def request_id():
    return "<%s-%s>" % (os.getpid(), ATOMIC_COUNTER.next())
