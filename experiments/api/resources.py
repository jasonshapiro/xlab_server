import simplejson as json

from django.contrib.auth.models import User
from django.forms.models import model_to_dict

from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import Authorization
from tastypie.serializers import Serializer

from experiments.api.authentication import ThejoAuthentication
from experiments.models import *

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        
class TimerResource(ModelResource):
    
    class Meta:
        queryset = Timer.objects.all()
        include_resource_uri = False
        authentication = ThejoAuthentication()
        
    def dehydrate_startDate(self, bundle):
        return {'year': bundle.data['startDate'].year, 'month': bundle.data['startDate'].month, 'date': bundle.data['startDate'].day}

    def dehydrate_endDate(self, bundle):
        return {'year': bundle.data['endDate'].year, 'month': bundle.data['endDate'].month, 'date': bundle.data['endDate'].day}


class GeofenceResource(ModelResource):
    
    class Meta:
        queryset = Geofence.objects.all()
        include_resource_uri = False
        authentication = ThejoAuthentication()

class BudgetLineInfoResource(ModelResource):
    
    class Meta:
        queryset = BudgetLineInfo.objects.all()
        excludes = ['created_date']
        include_resource_uri = False
        authentication = ThejoAuthentication()

class BudgetLineResource(ModelResource):
    
    info = fields.ToOneField('experiments.api.resources.BudgetLineInfoResource', 'budget_line_info', full=True)
    timer = fields.ToOneField('experiments.api.resources.TimerResource', 'timer', full=True, null=True)
    geofence = fields.ToOneField('experiments.api.resources.GeofenseResource', 'geofence', full=True, null=True)

    class Meta:
        queryset = BudgetLine.objects.all()
        include_resource_uri = False
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post']
        resource_name = 'budget_line'
        authentication = ThejoAuthentication()

class TextQuestionInfoResource(ModelResource):
    
    class Meta:
        queryset = BudgetLineInfo.objects.all()
        include_resource_uri = False
        authentication = ThejoAuthentication()

class TextQuestionResource(ModelResource):
    #user = fields.ForeignKey(UserResource, 'user')

    class Meta:
        queryset = TextQuestion.objects.all()
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post']
        resource_name = 'text_question'
        authentication = ThejoAuthentication()
        #filtering = {
        #    'user': ALL_WITH_RELATIONS,
        #    }