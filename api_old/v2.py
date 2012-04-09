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

from boto.s3.connection import S3Connection
from boto.s3.key import Key

from django.db import transaction, connection, IntegrityError
from django.contrib.auth.models import User

from piston.handler import AnonymousBaseHandler

from api.exceptions import *
from mcuser.models import *
from xlab_server.env_settings import *

API_VERSION = 2

class AnonymousAuthHandler(AnonymousBaseHandler):
    """
    Accept username and password and check if they are valid.
    """
    allowed_methods = ('POST',)

    @transaction.commit_manually
    def create(self, request):
        attrs = self.flatten_dict(request.POST)
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
#                if user_meta_data.phone_identifier != identifier:
#                    #The user is logging in on a different phone
#                    if 'change_phone' in attrs:
#                        inactive_phone = UserInactivePhone(user=u.id,
#                                            phone_identifier=user_meta_data.phone_identifier,
#                                            phone_platform=user_meta_data.phone_platform,
#                                            api_version=api_version)
#                        inactive_phone.save()
#
#                        user_meta_data.phone_identifier = identifier
#                        user_meta_data.phone_platform = platform
#                        user_meta_data.api_version = api_version
#                        user_meta_data.save()
#                    else:
#                        raise NewPhoneException("Your account is associated with a different phone." +
#                            " Would you like to associate it with this phone instead?")
#                else:
                #This is just a routine login. The user had probably killed / upgraded the application.
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

            # Save details of this API access
            api_access = ApiAccessEvent(user=u, access_type=ApiAccessEvent.AUTH_EVENT)
            api_access.save()

            resp = {'code' : 1, 'userid' : u.id, 'secret_key': user_meta_data.secret_key,
                    'email' : u.email, 'first_name' : u.first_name,
                    'last_name' : u.last_name}
        except User.DoesNotExist as e:
            transaction.rollback()
            logging.info("%s [username: %s] [error: %s]" % (r_id, username, str(e)))
            resp = {'code' : 0, 'message' : "The username is not valid."}
        except NewPhoneException as np:
            transaction.rollback()
            logging.info("%s [username: %s] [error: %s]" % (r_id, username, str(np)))
            resp = {'code' : 2, 'message' : str(np)}
        except Exception as ex:
            transaction.rollback()
            logging.exception( str(ex) )
            logging.info("%s [error: %s]" % (r_id, str(ex)))
            resp = {'code' : 0, 'message' : str(ex)}
        else:
            transaction.commit()

        return resp

class AnonymousDataHandler(AnonymousBaseHandler):
    """
    Accept data in bulk and add to the database.
    """
    allowed_methods = ('POST',)

    def _get_column_names(self, columns):
        l = list()

        for c in columns:
            l.append("%%(%s)s" % c)

        return ",".join(l)

    @transaction.commit_manually
    def create(self, request):
        user = username = identifier = None
        resp = {}
        cursor = connection.cursor()
        r_start = int(time.time() * 1000)
        r_id = request_id()

        try:
            sid = transaction.savepoint()
            
            #Log the size of the uploaded file
            upload_data_size = 0
            try:
                upload_data_size = len(request.FILES['data'])
                logging.debug("%s Size of compressed file - %s" % (r_id,
                    upload_data_size))
            except AttributeError:
                logging.debug("%s Could not fetch file size." % r_id)
                
            #Uncompress the data
            gzipper = gzip.GzipFile(fileobj=request.FILES['data'].file)
            data_str = gzipper.read()
            data_params = data_str.split('&')
            
            attrs = {}
            for p in data_params:
                kv = p.split('=', 1)
                attrs[kv[0]] = kv[1]

            if not (attrs.has_key('secret_key') and attrs.has_key('username')
                and attrs.has_key('identifier')):
                raise Exception("Key, username or identifier is missing")

            #log received data
            logging.debug("%s Client request [username: %s] [identifier: %s]" %
                            (r_id, attrs.get('username'), attrs.get('identifier')))

            #We have the key, username and identifier
            username = attrs.get('username')
            identifier = attrs.get('identifier')

            user = User.objects.get(username=username)
            if user.is_active == False:
                raise InactivePhoneException("This account is no longer active.")

            #Check if this phone is active for the account
            try:
                user_meta_data = UserMetaData.objects.get(user=user,
                    phone_identifier=identifier)
            except UserMetaData.DoesNotExist:
                #Check if the phone is inactive (can appear more than once in the table)
                inactive_phones = UserInactivePhone.objects.filter(user=user.id,
                    phone_identifier=identifier)
                    
                if len(inactive_phones) == 0:
                    #We should never be here. A phone should never
                    #upload data before the user has logged in at least once.
                    logging.critical("%s Received data from phone, but meta data is not available [username: %s] [identifier: %s]" %
                            (r_id, username, identifier))

                #TODO: The phone making the request is no longer active, but
                #it may still have data that we should save. Look for the
                #last login time of the phone that is now active and add all
                #the data collected earlier than that time from this request.
                raise InactivePhoneException("This phone is no longer " +
                    "associated with the username %s" % (username))

            md5_key = hashlib.md5(user_meta_data.secret_key + user.username).hexdigest()
            if attrs.get('secret_key') != md5_key:
                raise Exception("Key is invalid")

            # ----------------- Save all the data ------------------ #

            # Save location data
            if 'location_data' in attrs and attrs.get('location_data').strip() != "":
                data_list = list()
                loc_columns = ['lat', 'lon', 'gps_time', 'sample_time', 'velocity',
                    'haccuracy', 'altitude', 'course', 'service_provider',
                    'travel_mode', 'gps_sample_period', 'battery_level',]
                decimal_values = ['lat', 'lon', 'velocity', 'haccuracy', 'altitude',
                    'course',]
                loc_data_lines = attrs.get('location_data').split("\n")

                for key, sample in enumerate(loc_data_lines):
                    fields = {'user_id' : user.id}
                    parts = sample.split(",")

                    if len(parts) < len(loc_columns):
                            raise InvalidDataException("Mandatory values are "
                                "missing in location_data")

                    for index, part in enumerate(parts):
                        if part.strip() == "":
                                raise InvalidDataException("Mandatory value "
                                    "cannot be an empty string in location_data")

                        fields[loc_columns[index]] = part

                    #Validate the numbers in this trace
                    valid_data = True
                    for key, part in fields.items():
                        if type(part) is float:
                            fields[key] = '%.6f' % part

                        #Check if any float value is out of bounds
                        if key in decimal_values and (float(part) > 999999 or float(part) < -999999):
                            valid_data = False
                            logging.warn(("%s Out of bounds location data "
                                "received [username: %s] [data: %s]") %
                                (r_id, user.username, sample))
                            break

                    #Save this object
                    if valid_data is True:
                        data_list.append(fields)
                        
                cursor.executemany(("INSERT INTO traces_data \
                    (user_id, seed_data, created_date, " +
                    ",".join(loc_columns) + ") \
                    VALUES (%(user_id)s, false, NOW(), " +
                    self._get_column_names(loc_columns) + ")"), data_list)

                logging.info("%s Wrote location data to the database [username: %s] [rows: %d]" %
                    (r_id, username, len(loc_data_lines)))

            # Save android state machine data
            if 'sm_data' in attrs and attrs.get('sm_data').strip() != "":
                data_list = list()
                sm_columns = ['sample_time', 'lat', 'lon', 'data',]
                sm_data_lines = attrs.get('sm_data').split("\n")

                for key, sample in enumerate(sm_data_lines):
                    fields = {'user_id' : user.id}
                    parts = sample.split(",")

                    if len(parts) < len(sm_columns):
                            raise InvalidDataException("Mandatory values are missing in sm_data")

                    for index, part in enumerate(parts):
                        if part.strip() == "":
                                raise InvalidDataException("Mandatory value cannot be an empty string in sm_data")

                        fields[sm_columns[index]] = part

                    #Validate the numbers
                    valid_data = True
                    for key, part in fields.items():
                        if type(part) is float:
                            fields[key] = '%.6f' % part

                        #Check if any float value is out of bounds
                        if key in ['lat', 'lon'] and (float(part) > 999999 or float(part) < -999999):
                            valid_data = False
                            logging.warn("%s Out of bounds state machine data received [username: %s] [data: %s]" %
                                (r_id, user.username, sample))
                            break

                    #Save this object
                    if valid_data is True:
                        data_list.append(fields)

                cursor.executemany("INSERT INTO traces_androiddata \
                    (user_id, sample_time, lat, lon, data, created_date) \
                    VALUES (%(user_id)s, %(sample_time)s, %(lat)s, %(lon)s, %(data)s, NOW())",
                    data_list)

                logging.info("%s Wrote android state machine data to the database [username: %s] [rows: %d]" %
                    (r_id, username, len(sm_data_lines)))

            # Save lifecycle event data
            if 'lifecycle_events' in attrs and attrs.get('lifecycle_events').strip() != "":
                data_list = list()
                le_columns = ['event_type', 'event_time', 'lat', 'lon', 'accuracy',
                    'last_fix_time', 'event_reason']
                event_data_lines = attrs.get('lifecycle_events').split("\n")

                for key, sample in enumerate(event_data_lines):
                    fields = {'user_id' : user.id, 'data': None}
                    parts = sample.split(",")

                    if len(parts) < len(le_columns):
                        raise InvalidDataException("Mandatory values are missing in lifecycle_events")

                    for index, part in enumerate(parts):
                        if part.strip() == "":
                                raise InvalidDataException("Mandatory value cannot be an empty string in lifecycle_events")

                        #Handle the raw data if it is present
                        if index == 0:
                            #event_type
                            part = part.lower()
                            fields[le_columns[index]] = LifecycleEvent.EVENT_TYPE_MAP[part]
                        elif index == len(le_columns):
                            fields['data'] = part
                        elif index == len(le_columns) - 1:
                            #reason
                            part = part.lower()
                            fields[le_columns[index]] = 0 if not LifecycleEvent.REASON_MAP.has_key(part) \
                                else LifecycleEvent.REASON_MAP[part]
                        else:
                            fields[le_columns[index]] = part

                    #Validate the numbers
                    valid_data = True
                    for key, part in fields.items():
                        if type(part) is float:
                            fields[key] = '%.6f' % part

                        #Check if any float value is out of bounds
                        if key in ['lat', 'lon'] and (float(part) > 999999 or float(part) < -999999):
                            valid_data = False
                            logging.warn("%s Out of bounds lifecycle event data received [username: %s] [data: %s]" %
                                (r_id, user.username, sample))
                            break

                    #Save this object
                    if valid_data is True:
                        data_list.append(fields)

                cursor.executemany(("INSERT INTO traces_lifecycleevent \
                    (user_id, data, created_date, " + ",".join(le_columns) + ") \
                    VALUES (%(user_id)s, %(data)s, NOW(), " + self._get_column_names(le_columns) + ")"),
                    data_list)

                logging.info("%s Wrote lifecycle event data to the database [username: %s] [rows: %d]" %
                    (r_id, username, len(event_data_lines)))

            # Save sensor state machine data
            if 'sensor_data' in attrs and attrs.get('sensor_data').strip() != "":
                data_list = list()
                sm_columns = ['type', 'sample_time', 'data',]
                sm_data_lines = attrs.get('sensor_data').split("\n")

                for key, sample in enumerate(sm_data_lines):
                    fields = {'user_id' : user.id}
                    parts = sample.split(",")

                    if len(parts) < len(sm_columns):
                            raise InvalidDataException("Mandatory values are missing in sensor_data")

                    for index, part in enumerate(parts):
                        if part.strip() == "":
                                raise InvalidDataException("Mandatory value cannot be an empty string in sensor_data")

                        fields[sm_columns[index]] = part
                        
                    data_list.append(fields)

                cursor.executemany("INSERT INTO  traces_sensorstatemachinedata \
                    (user_id, sample_time, type, data, created_date) \
                    VALUES (%(user_id)s, %(sample_time)s, %(type)s, %(data)s, NOW())",
                    data_list)

                logging.info("%s Wrote sensor state machine data to the database [username: %s] [rows: %d]" %
                    (r_id, username, len(sm_data_lines)))


            #Save the push notification token if it is available
            if 'push_notification_token' in attrs and attrs.get('push_notification_token').strip() != "":
                user_meta_data.push_notification_token = attrs.get('push_notification_token')
                user_meta_data.save()
            
            #Fetch and add the hotspot data if it is available
            h_list = ["%s,%s" % (h.lat,h.lon) for h in Hotspot.objects.filter(user=user)]
            if len(h_list) > 0:
                resp.update({'hot_spots': ";".join(h_list)})

            # Add cached trips if they are available
            if 'cached_trips' in attrs:
                ct_list = [{"ep": ct.encoded_path,
                    "dt": ct.distance_traveled}
                    for ct in CachedTrip.objects.filter(user=user)
                    if ct.encoded_path is not None]
                if len(ct_list) > 0:
                    resp.update({'cached_trips': ct_list})

            # Add list of groups this user is a member of
            # TODO: This information needs to cached
            if user.groups.count() > 0:
                resp.update({'groups' : ",".join([ str(g['id']) for g in user.groups.values() ])})

            resp.update({'code' : 1, 'message' : 'Success',
                        'sleep_time': user_meta_data.sleep_time})

            # Save details of this API access
            api_access = ApiAccessEvent(user=user,
                access_type=ApiAccessEvent.DATA_UPLOAD, data=upload_data_size)
            api_access.save()

            transaction.savepoint_commit(sid)

        except (InvalidDataException, KeyError, IndexError) as id:
            transaction.savepoint_rollback(sid)
            logging.exception( "%s %s [username: %s] [identifier: %s]" %
                (r_id, str(id), username, identifier) )
            # Code 0 tells the client to delete the data
            resp.update({'code' : 0, 'message' : str(id)})
            if user is not None:
                uploaded_data = "%s \n*******************\n%s" % \
                    (traceback.format_exc(), data_str)
                api_access = ApiAccessEvent(user=user,
                    access_type=ApiAccessEvent.DATA_UPLOAD_FAIL,
                    data=uploaded_data)
                api_access.save()
        except (InactivePhoneException, User.DoesNotExist) as ip:
            transaction.savepoint_rollback(sid)
            logging.info("%s %s [username: %s] [identifier: %s]" %
                (r_id, str(ip), username, identifier))
            resp.update({'code' : 2, 'message' : str(ip)})
            if user is not None:
                uploaded_data = "%s \n*******************\n%s" % \
                    (traceback.format_exc(), data_str)
                api_access = ApiAccessEvent(user=user,
                    access_type=ApiAccessEvent.DATA_UPLOAD_FAIL,
                    data=uploaded_data)
                api_access.save()
        except Exception as ex:
            transaction.savepoint_rollback(sid)
            logging.exception( "%s %s" % (r_id, str(ex)) )
            # Code 3 tells the client to try again later
            resp.update({'code' : 3, 'message' : str(ex)})
            if user is not None:
                uploaded_data = "%s \n*******************\n%s" % \
                    (traceback.format_exc(), data_str)
                api_access = ApiAccessEvent(user=user,
                    access_type=ApiAccessEvent.DATA_UPLOAD_FAIL,
                    data=uploaded_data)
                api_access.save()

        transaction.commit()
        logging.info("%s Data upload API process time - %s" % (r_id,
            int(time.time() * 1000) - r_start))
        
        return resp

class AnonymousImageHandler(AnonymousBaseHandler):
    """
    Accept image and store it
    """
    allowed_methods = ('POST',)
    s3_conn = S3Connection(AWS_ACCESS_KEY, AWS_SECRET_KEY)

    @transaction.commit_manually
    def create(self, request):
        attrs = self.flatten_dict(request.POST)
        r_id = request_id()
        image_type = 0
        r_start = int(time.time() * 1000)

        try:
            mandatory = ['secret_key', 'username', 'type', 'extension']
            if len([x for x in attrs if x in mandatory]) != len(mandatory):
                raise Exception("A mandatory parameter is missing")

            username = attrs.get('username')
            secret_key = attrs.get('secret_key')
            type = attrs.get('type')
            extension = attrs.get('extension')
            fileobj = request.FILES['image'].file

            user = User.objects.get(username=username)
            if user.is_active == False:
                raise InactivePhoneException("This account is no longer active.")

            #Check if this phone is active for the account
            try:
                user_meta_data = UserMetaData.objects.get(user=user)
            except UserMetaData.DoesNotExist:
                raise InactivePhoneException("This phone is no longer " +
                    "associated with the username %s" % (username))

            md5_key = hashlib.md5(user_meta_data.secret_key + user.username).hexdigest()
            if secret_key != md5_key:
                raise Exception("Key is invalid")

            # Check if the right image type has been provided
            if type == "odometer":
                image_type = Image.TYPE_ODOMETER
            else:
                raise Exception("Unsupported image type - %s" % type)

            # Check if the right file type has been provided
            if extension not in ["jpg", "png"]:
                raise Exception("Unsupported image extension - %s" % extension)

            # Save the file to S3
            s3_bucket = self.s3_conn.create_bucket('com.milesense.images')
            s3_key = Key(s3_bucket)
            file_md5, digest_base64 = s3_key.compute_md5(fileobj)
            s3_key.key = "%s.%s" % (file_md5, extension)
            s3_key.set_contents_from_file(fileobj)
            s3_key.set_acl('public-read')

            file_url = "%s/%s" % (AWS_IMAGE_URL_BASE, s3_key.key)
            image = Image(user=user, type=image_type, url=file_url)
            image.save()

            # Save details of this API access
            api_access_data = "Type: %s, file size: %s" % (type,
                len(request.FILES['image']))
            api_access = ApiAccessEvent(user=user,
                access_type=ApiAccessEvent.IMAGE_UPLOAD, data=api_access_data)
            api_access.save()

            resp = {'code' : 1, 'message' : 'Success'}
        except Exception as ex:
            transaction.rollback()
            logging.exception( str(ex) )
            logging.info("%s [error: %s]" % (r_id, str(ex)))
            resp = {'code' : 0, 'message' : str(ex)}
        else:
            transaction.commit()

        logging.info("%s Image save time - %s" % (r_id,
            int(time.time() * 1000) - r_start))

        return resp