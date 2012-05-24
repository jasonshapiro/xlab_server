import simplejson as json

from django.contrib.auth.models import User
from django.forms.models import model_to_dict

from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.authentication import Authentication
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import ReadOnlyAuthorization
from tastypie.serializers import Serializer

from experiments.api.authentication import ThejoAuthentication
from experiments.models import *

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post']
        resource_name = 'auth/user'
        excludes = ['email', 'password', 'is_superuser']
        authentication = BasicAuthentication()
        authorization = ReadOnlyAuthorization()
        
    def dehydrate(self, bundle):
        return bundle.data['username']

class TimerResource(ModelResource):
    
    class Meta:
        queryset = Timer.objects.all()
        include_resource_uri = False
        authentication = BasicAuthentication()
        authorization = ReadOnlyAuthorization()
        
    def dehydrate_startDate(self, bundle):
        return {'year': bundle.data['startDate'].year, 'month': bundle.data['startDate'].month, 'date': bundle.data['startDate'].day}

    def dehydrate_endDate(self, bundle):
        return {'year': bundle.data['endDate'].year, 'month': bundle.data['endDate'].month, 'date': bundle.data['endDate'].day}


class GeofenceResource(ModelResource):
    
    class Meta:
        queryset = Geofence.objects.all()
        include_resource_uri = False
        authentication = BasicAuthentication()
        authorization = ReadOnlyAuthorization()

class BudgetLineInfoResource(ModelResource):
    
    class Meta:
        queryset = BudgetLineInfo.objects.all()
        excludes = ['created_date']
        include_resource_uri = False
        authentication = BasicAuthentication()
        authorization = ReadOnlyAuthorization()

class TextQuestionInfoResource(ModelResource):
    
    class Meta:
        queryset = TextQuestionInfo.objects.all()
        excludes = ['created_date']
        include_resource_uri = False
        authentication = BasicAuthentication()
        authorization = ReadOnlyAuthorization()

#abstract
class ExperimentResource(ModelResource):
    
    timer = fields.ToOneField('experiments.api.resources.TimerResource', 'timer', full=True, null=True)
    geofence = fields.ToOneField('experiments.api.resources.GeofenceResource', 'geofence', full=True, null=True)
    users = fields.ToManyField('experiments.api.resources.UserResource', 'users', full=True, null=True)

    class Meta:
        abstract = True
  
class BudgetLineResource(ExperimentResource):
    id = models.IntegerField(primary_key=True, editable=False)
    info = fields.ToOneField('experiments.api.resources.BudgetLineInfoResource', 'budget_line_info', full=True)

    class Meta:
        queryset = BudgetLine.objects.all()
        resource_name = 'budget_line'
        include_resource_uri = False
        users = fields.ToManyField(UserResource, 'notes', full=True)
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post']
        authentication = BasicAuthentication()
        authorization = ReadOnlyAuthorization()

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(users=request.user)

class TextQuestionResource(ExperimentResource):
    id = models.IntegerField(primary_key=True, editable=False)
    info = fields.ToOneField('experiments.api.resources.TextQuestionInfoResource', 'text_question_info', full=True)

    class Meta:
        queryset = TextQuestion.objects.all()
        resource_name = 'text_question'
        include_resource_uri = False
        users = fields.ToManyField(UserResource, 'notes', full=True)
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post']
        authentication = BasicAuthentication()
        authorization = ReadOnlyAuthorization()

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(users=request.user)
