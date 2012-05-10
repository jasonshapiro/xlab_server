import base64
import datetime
import gzip
import hashlib
import logging
import os
import pytz
import time
import traceback

from pytz import UnknownTimeZoneError

from tastypie.api import Api

from django.db import connection, IntegrityError
from django.contrib.auth.models import User

from tastypie.authentication import Authentication

from env_settings import *
from experiments.api.exceptions import *
from mcuser.models import *

API_VERSION = 2 #so client won't have to change

#In honor of (and largely written by) Thejo Kote. May he live long and prosper.
class ThejoAuthentication(Authentication):
    def is_authenticated(self, request, **kwargs):
        attrs = request.POST
        r_id = request_id()

        try:
            mandatory = ['key', 'username', 'password', 'identifier', 'platform',
                'api_version', 'location_services', 'timezone' ]
            if len([x for x in attrs if x in mandatory]) != len(mandatory):
                raise Exception("A mandatory parameter is missing")

            username = attrs.get('username')
            identifier = attrs.get('identifier')
            platform = int(attrs.get('platform'))
            api_version = int(attrs.get('api_version'))
            timezone = attrs.get('timezone')
            location_services = attrs.get('location_services')

            if(api_version != API_VERSION):
                raise Exception("Invalid API version for this endpoint.")

            #Check if the timezone is valid
            try:
                tz = pytz.timezone(timezone)
            except UnknownTimeZoneError:
                timezone = UserMetaData.DEFAULT_TIMEZONE
                logging.warn("%s Invalid timezone received from phone [username: %s] [identifier: %s] [platform: %s] [timezone: %s]" %
                    (r_id, username, identifier, platform, timezone))
                #TODO: Send an SMS / e-mail alert about this.

            #TODO: Check if we need an index on the username column
            u = User.objects.get(username__exact=username)
            if u.is_active == False:
                raise User.DoesNotExist("The account is inactive")

            md5_key = hashlib.md5(API_SECRET_KEY + u.username).hexdigest()
            if attrs.get('key') != md5_key:
                raise Exception("Key is invalid")

            if not u.check_password(attrs.get('password')):
                raise Exception("Password is incorrect")

            #Check if this phone is active for the account
            try:
                user_meta_data = UserMetaData.objects.get(user=u)

                logging.debug("%s [username: %s] [active UDID: %s] [current UDID: %s]" %
                    (r_id, u.username, user_meta_data.phone_identifier, identifier))

                logging.debug("%s Routine login by [username: %s] [identifier: %s]" % (r_id, u.username, identifier))
                user_meta_data.api_version = api_version
                user_meta_data.last_login = datetime.datetime.now()
                user_meta_data.save()
            except UserMetaData.DoesNotExist:
                #The user is logging in for the first time.
                logging.debug("%s First login by [username: %s] [identifier: %s]" % (r_id, u.username, identifier))
                #TODO: Handle the case where the generated keys already exist
                secret_key = base64.urlsafe_b64encode(os.urandom(32))
                invite_code = base64.urlsafe_b64encode(os.urandom(6))
                user_meta_data = UserMetaData(user=u, secret_key=secret_key,
                    phone_identifier=identifier, phone_platform=platform,
                    api_version=api_version, invite_code=invite_code,
                    timezone=timezone, last_login=datetime.datetime.now())
                try:
                    user_meta_data.save()
                except IntegrityError:
                    raise Exception("An error occurred. Please try again.")

                #TODO: Shove the location services data in a table for now
                if location_services != "":
                    ls = UserAnalytics(user=u, data_type=UserAnalytics.LOCATION_SERVICES,
                            value=location_services)
                    ls.save()
                else:
                    raise Exception("Location services data is missing.")

            logging.info("%s User logged in [username: %s] [user id: %d]" %
                (r_id, u.username, u.id))

            return true

        except User.DoesNotExist as e:
            logging.info("%s [username: %s] [error: %s]" % (r_id, username, str(e)))
            return false
        except Exception as ex:
            logging.exception( str(ex) )
            logging.info("%s [error: %s]" % (r_id, str(ex)))
            return false

    # Optional but recommended
    def get_identifier(self, request):
        return request.user.username