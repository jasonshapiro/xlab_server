from mcuser.models import *
from django.contrib import admin

class UserMetaDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone_platform', 'api_version', 'last_login',
        'push_notification_failures', 'timezone', 'created_date',)
    list_filter = ('phone_platform', 'api_version', 'user__groups__name')

class UserInactivePhoneAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone_identifier', 'phone_platform',
        'created_date',)
    list_filter = ('phone_platform',)

class UserSummaryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'trips', 'miles', 'accidents_passed',
        'left_turns', 'created_date',)
    list_filter = ('user__groups__name',)

class HotspotAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'lat', 'lon', 'description',
        'created_date',)
    list_filter = ('user__groups__name',)

class InviteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'invite_email', 'is_accepted', 'sent_date',)

class InboundUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'is_insurance_company', 'created_date')
    list_filter = ('is_insurance_company',)

class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'type', 'url', 'created_date')

admin.site.register(UserMetaData, UserMetaDataAdmin)
admin.site.register(UserInactivePhone, UserInactivePhoneAdmin)
admin.site.register(UserSummary, UserSummaryAdmin)
admin.site.register(Hotspot, HotspotAdmin)
admin.site.register(Invite, InviteAdmin)
admin.site.register(InboundUser, InboundUserAdmin)
admin.site.register(Image, ImageAdmin)