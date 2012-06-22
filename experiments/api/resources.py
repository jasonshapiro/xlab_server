import simplejson as json
import random
import logging

from django.db import models
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.http import HttpResponse

from tastypie import fields
from tastypie.resources import ModelResource, ALL
from tastypie.authentication import BasicAuthentication, ApiKeyPlusWebAuthentication
from tastypie.authorization import ReadOnlyAuthorization
from tastypie.authorization import Authorization
from tastypie.serializers import Serializer

from experiments.models import *

MAX_PROGRESS = 100

class UserResource(ModelResource):
    
    class Meta:
        queryset = User.objects.all()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        resource_name = 'auth/user'
        excludes = ['email', 'password', 'is_superuser']
        authentication = BasicAuthentication()
        authorization = ReadOnlyAuthorization()
        filtering = {
            "username": ALL,
        }
        
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
    number_sessions = models.IntegerField(editable = False)

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(users=request.user)

    class Meta:
        abstract = True
        include_resource_uri = False
        authentication = ApiKeyPlusWebAuthentication()
        authorization = ReadOnlyAuthorization()
  
class BudgetLineResource(ExperimentResource):
    
    info = fields.ToOneField('experiments.api.resources.BudgetLineInfoResource', 'budget_line_info', full=True)
    intercepts = fields.DictField()

    class Meta(ExperimentResource.Meta):
        queryset = BudgetLine.objects.all()
        resource_name = 'budget_line'
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']

    def dehydrate(self, bundle):
        finished = True
        intercepts_list = list()
        line_chosen_index = random.randrange(bundle.data['number_sessions'])
        for i in range(0, bundle.data['number_sessions']):
            response = BudgetLineResponse.objects.filter(user=bundle.request.user).filter(budget_line=BudgetLine.objects.get(pk=bundle.data['id'])).filter(session=i)
            if len(response) == 0:
                finished = False
                x_int = random.uniform(bundle.data['info'].data['x_min'], bundle.data['info'].data['x_max'])
                y_int = random.uniform(bundle.data['info'].data['y_min'], bundle.data['info'].data['y_max'])
                blr = BudgetLineResponse(user = bundle.request.user, budget_line = BudgetLine.objects.get(pk = bundle.data['id']), session = i, x_intercept = x_int, y_intercept = y_int, winner = 'x' if (random.random() < bundle.data['info'].data['prob_x']) else 'y', line_chosen_boolean = (i == line_chosen_index))
                blr.save()
                bli = BudgetLineInput(id = blr.id, budget_line_response = blr, user = bundle.request.user)
                bli.save()
                intercepts_list.append({"response_id": blr.id, "x_intercept": x_int, "y_intercept": y_int})
            else:
                if response[0].eligible_for_answer:
                    finished = False
                intercepts_list.append({"response_id": response[0].id, "x_intercept": response[0].x_intercept, "y_intercept": response[0].y_intercept})
        if finished:
            bundle.data['id'] = -1
        else:
            bundle.data['intercepts'] = intercepts_list
        return bundle

class TextQuestionResource(ExperimentResource):

    info = fields.ToOneField('experiments.api.resources.TextQuestionInfoResource', 'text_question_info', full=True)
    responses = fields.DictField()

    class Meta(ExperimentResource.Meta):
        queryset = TextQuestion.objects.all()
        resource_name = 'text_question'
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']

    def dehydrate(self, bundle):
        finished = True
        responses_list = list()
        for i in range(0, bundle.data['number_sessions']):
            response = TextQuestionResponse.objects.filter(user=bundle.request.user).filter(text_question=TextQuestion.objects.get(pk=bundle.data['id'])).filter(session=i)
            if len(response) == 0:
                finished = False
                tqr = TextQuestionResponse(user = bundle.request.user, text_question = TextQuestion.objects.get(pk = bundle.data['id']), session = i, answer = "")
                tqr.save()
                tqi = TextQuestionInput(id = tqr.id, text_question_response = tqr, user = bundle.request.user)
                tqi.save()
                responses_list.append({"response_id": tqr.id})
            else:
                if response[0].eligible_for_answer:
                    finished = False
                responses_list.append({"response_id": response[0].id})
        if finished:
            bundle.data['id'] = -1
        else:
            bundle.data['responses'] = responses_list
        return bundle

#abstract
class ExperimentResponseResource(ModelResource):
    
    user = fields.ToOneField(UserResource, 'user')

    class Meta:
        abstract = True
        authentication = ApiKeyPlusWebAuthentication()
        authorization = Authorization()
        
class BudgetLineResponseResource(ExperimentResponseResource):
    
    experiment = fields.ToOneField(BudgetLineResource, 'budget_line')

    class Meta(ExperimentResponseResource.Meta):
        queryset = BudgetLineResponse.objects.all()
        
class TextQuestionResponseResource(ExperimentResponseResource):
    
    experiment = fields.ToOneField(TextQuestionResource, 'text_question')

    class Meta(ExperimentResponseResource.Meta):
        queryset = BudgetLineResponse.objects.all()
        resource_name = 'budget_line_input'
        
#abstract
class ExperimentInputResource(ModelResource):
    
    user = fields.ToOneField(UserResource, 'user')

    class Meta:
        abstract = True
        authentication = ApiKeyPlusWebAuthentication()
        authorization = Authorization()
        
class BudgetLineInputResource(ExperimentResponseResource):
    
    class Meta(ExperimentResponseResource.Meta):
        queryset = BudgetLineInput.objects.all()
        resource_name = 'budget_line_input'
        list_allowed_methods = ['patch','put']
        detail_allowed_methods = ['patch','put']
        
    def hydrate(self, bundle):
        resp = BudgetLineResponse.objects.get(id = bundle.obj.id)
        if ((bundle.request.user == bundle.obj.user) & bundle.obj.budget_line_response.eligible_for_answer):
            if (bundle.data['progress'] >= 0):#ignores non-response due to restrictive timer
                slope = resp.y_intercept / resp.x_intercept
                resp.x = resp.x_intercept * bundle.data['progress'] / MAX_PROGRESS
                resp.y = resp.y_intercept - slope * resp.x_intercept * bundle.data['progress'] / MAX_PROGRESS
            resp.eligible_for_answer = False
            resp.save()
        return bundle

class TextQuestionInputResource(ExperimentResponseResource):
    
    class Meta(ExperimentResponseResource.Meta):
        queryset = TextQuestionInput.objects.all()
        resource_name = 'text_question_input'
        list_allowed_methods = ['patch','put']
        detail_allowed_methods = ['patch','put']

    def hydrate(self, bundle):
        logging.debug("bundle.request.user == bundle.obj.user: %s" % (bundle.request.user == bundle.obj.user))
        resp = TextQuestionResponse.objects.get(id = bundle.obj.id)
        if ((bundle.request.user == bundle.obj.user) & bundle.obj.text_question_response.eligible_for_answer):
            if (bundle.data['answer'] != 'blank_tag'):#ignores non-response due to restrictive timer
                resp.answer = bundle.data['answer']
            resp.eligible_for_answer = False
            resp.save()
        return bundle