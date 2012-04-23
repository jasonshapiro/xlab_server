from django.db import models
from django.contrib.auth.models import User, Group

class UserMetaData(models.Model):
    DEFAULT_TIMEZONE = "America/Los_Angeles"
    
    PLATFORM_IOS = 1
    PLATFORM_ANDROID = 11
    PLATFORMS = ( (0, "Unknown"), (PLATFORM_IOS, "iOS"), (PLATFORM_ANDROID, "Android"),
        (21, "Windows") )

    user = models.ForeignKey(User)
    secret_key = models.CharField(max_length=100, unique=True)
    phone_identifier = models.CharField(max_length=100)
    phone_platform = models.IntegerField(default=0, choices=PLATFORMS)
    last_login = models.DateTimeField(db_index=True, null=True, blank=True,)
    sleep_time = models.TextField(null=True, blank=True,
        help_text="Minute of day in parentheses: (start sleep)-(end sleep),(start sleep)-(end sleep)")
    invite_code = models.CharField(max_length=50, unique=True)
    push_notification_token = models.CharField(max_length=255, null=True, blank=True)
    push_notification_failures = models.IntegerField(default=0)
    api_version = models.IntegerField(default=1)
    hardware_device_id = models.CharField(max_length=255, null=True, blank=True,
        help_text="Unique identifier of the hardware device associated with this account")
    timezone= models.CharField(max_length=100, default=DEFAULT_TIMEZONE)
    last_updated_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "user meta data"

class UserInactivePhone(models.Model):
    #This column is not a foreign key because we can have more than one row per user
    user = models.IntegerField()
    phone_identifier = models.CharField(max_length=100)
    phone_platform = models.IntegerField(default=0, choices=UserMetaData.PLATFORMS)
    api_version = models.IntegerField(default=1)
    last_updated_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)
        
class UserSummary(models.Model):
    user = models.ForeignKey(User)
    trips = models.DecimalField(max_digits=12, decimal_places=6)
    miles = models.DecimalField(max_digits=12, decimal_places=6)
    accidents_passed = models.DecimalField(max_digits=12, decimal_places=6)
    left_turns = models.DecimalField(max_digits=12, decimal_places=6)
    highway_miles = models.DecimalField(max_digits=12, decimal_places=6)
    confidence = models.DecimalField(max_digits=12, decimal_places=6, null=True, blank=True,)
    hour_of_day_histogram = models.CommaSeparatedIntegerField(max_length=255, null=True, blank=True,)
    zipcode_parked_at_night = models.TextField(null=True, blank=True,)
    zipcode_driven_through = models.TextField(null=True, blank=True,)
    last_updated_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def get_total_miles(self):
        return '%.2f' % (self.miles / 1609.344)

    def get_highway_distance_percent(self):
        if self.miles == 0:
            return "Unknown"
        else:
            h_dist = '%.2f' % ((self.highway_miles / float(self.miles)) * 100)
            return "%s%s" % (h_dist, "%")

    class Meta:
        verbose_name_plural = "user summaries"

class UserAnalytics(models.Model):
    LOCATION_SERVICES = 1
    DATA_TYPE = ( (0, "Unknown"), (LOCATION_SERVICES, "Location services on login"),  )

    user = models.ForeignKey(User)
    data_type = models.IntegerField(default=0, choices=DATA_TYPE)
    value = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

class Hotspot(models.Model):
    user = models.ForeignKey(User)
    lat = models.DecimalField(max_digits=12, decimal_places=6)
    lon = models.DecimalField(max_digits=12, decimal_places=6)
    average_duration = models.DecimalField(max_digits=12, decimal_places=6,
        null=True, blank=True,)
    last_visited = models.BigIntegerField(null=True, blank=True,)
    hours_histogram = models.TextField(null=True, blank=True,)
    description = models.CharField(max_length=100, null=True, blank=True,)
    last_updated_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)

class Invite(models.Model):
    #This column is not a foreign key because we can have more than one row per user
    user = models.IntegerField(db_index=True)
    name = models.CharField(max_length=100, null=True, blank=True,)
    invite_email = models.EmailField()
    invite_code = models.CharField(max_length=100, unique=True, db_index=True)
    group = models.ForeignKey(Group)
    is_accepted = models.BooleanField(default=False)
    last_updated_date = models.DateTimeField(auto_now=True)
    sent_date = models.DateTimeField(auto_now_add=True)

class InboundUser(models.Model):
    email = models.EmailField(max_length=255, db_index=True)
    is_insurance_company = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)


class Image(models.Model):
    TYPE_ODOMETER = 1
    IMAGE_TYPE = ( (0, "Unknown"), (TYPE_ODOMETER, "Odometer"),  )

    user = models.ForeignKey(User)
    type = models.IntegerField(default=0, choices=IMAGE_TYPE)
    url = models.URLField()
    created_date = models.DateTimeField(auto_now_add=True)
