from django.conf.urls.defaults import *

from xlab_server import env_settings

from django.contrib import admin
admin.autodiscover()

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

    #XLAB
    (r'^experiments/', include('xlab_server.experiments.urls')), #better be okay
        
)

if env_settings.ENV_DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': env_settings.STATIC_DOC_ROOT}),
    )
