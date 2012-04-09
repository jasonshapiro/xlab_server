from django.conf.urls.defaults import *
from piston.resource import Resource
from xlab_server.api import v2

class CsrfExemptResource( Resource ):
    def __init__( self, handler, authentication = None ):
        super( CsrfExemptResource, self ).__init__( handler, authentication )
        self.csrf_exempt = getattr( self.handler, 'csrf_exempt', True )

#API v2
v2_data_handler = CsrfExemptResource(v2.AnonymousDataHandler)
v2_auth_handler = CsrfExemptResource(v2.AnonymousAuthHandler)
v2_image_handler = CsrfExemptResource(v2.AnonymousImageHandler)

urlpatterns = patterns('',
    #API v1 - deprecated

    #API v2
    url(r'^v2/data/', v2_data_handler),
    url(r'^v2/auth/', v2_auth_handler),
    url(r'^v2/image/', v2_image_handler)
)