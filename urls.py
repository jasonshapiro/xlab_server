from django.conf.urls.defaults import *
from tastypie.api import Api
from xlab_server import env_settings
from xlab_server.myapi import UserResource
from xlab_server.myapi import BlineResource
from django.contrib import admin

admin.autodiscover()

user_resource = UserResource()

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(BlineResource())

urlpatterns = patterns('',
    # Example:
    # (r'^modechoice/', include('modechoice.foo.urls')),

    (r'^$', 'mcuser.views.index'), #updated for xlab (see TODO)
    (r'^home/$', 'mcuser.views.index'),  #updated for xlab (see TODO in mcuser.views.index)
    (r'^mcadmin/$', 'mcuser.views.mcadmin'), #updated for xlab

    (r'^accounts/login/$', 'django.contrib.auth.views.login'), #okay (Where is HTML defined?)
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout'), #okay (Where is HTML defined?)
    (r'^accounts/createnewaccount/$', 'mcuser.views.register'), #okay
    (r'^accounts/profile/$', 'mcuser.views.profile'), #updated for xlab (see TODO in mcuser.views.index)

    (r'^user/', include('xlab_server.mcuser.urls')), #okay

    # TODO: Add admin documentation?
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)), #okay

    #TODO: Should future API be handled through this for user-specific data?

    (r'^api/', include('xlab_server.api.urls')), #contains relics
    (r'^api/', include(v1_api.urls)), #authentication using tasetypie 

    #(r'^api/', include('xlab_server.api.urls')), #contains relics
#authentication using tasetypie 

    #XLAB
    (r'^experiments/', include('xlab_server.experiments.urls')), #better be okay
   
)

if env_settings.ENV_DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': env_settings.STATIC_DOC_ROOT}),
    )
