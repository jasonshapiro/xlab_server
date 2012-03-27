from django.contrib.auth.models import User
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.resources import ModelResource
from tastypie.authentication import DigestAuthentication
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.models import ApiKey
from django.forms.models import model_to_dict

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        print 'in meta'
        print model_to_dict(User, fields=[field.name for field in User._meta.fields]);
        resource_name = 'auth/user'
        excludes = ['email', 'username', 'password', 'is_superuser']
        # Add it here.
        for user in User.objects.all(): 
            try:
                key = ApiKey.objects.get(user=user)
                print "created key"
                print user 
                print key
            except ApiKey.DoesNotExist:
<<<<<<< Updated upstream
                print "api key does not exits"
#                ApiKey.objects.create(user=user) 
  #      authentication= ApiKeyAuthentication()
=======
                print 'exception raised!'
                ApiKey.objects.create(user=user) 
    
>>>>>>> Stashed changes
        authentication = DigestAuthentication()
        authorization = DjangoAuthorization()
        
        
class UserAuthentication(BasicAuthentication):
    def is_authenticated(self, request, **kwargs):
        if 'patrick' in request.user.username:
          print "Hello User, you're lookin' fine!"
          return True

        return False

    # Optional but recommended
    def get_identifier(self, request):
        return request.user.username

class UserAuthorization(DjangoAuthorization):
    def is_authorized(self, request, object=None):
        if 'patrick' in request.user.username:
            return True
 
        return False

    # Optional but useful for advanced limiting, such as per user.
    def apply_limits(self, request, object_list):
        if request and hasattr(request, 'user'):
            return object_list.filter(author__username=request.user.username)

        return object_list.none()
    
    