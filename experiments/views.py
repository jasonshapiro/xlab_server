import decimal
import logging
import random
import simplejson as json

from experiments.models import *
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core import serializers
from django.forms.models import model_to_dict
from decimal import Decimal
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from tastypie.models import create_api_key

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        if isinstance(o, datetime.date):
            return {'year': o.year, 'month': o.month, 'date': o.day}
        super(DecimalEncoder, self).default(o)
        

def index(request):
   
   return render_to_response('experiments/index.html',context_instance=RequestContext(request))

@login_required
def budgetline_experiment(request):
    
    return render_to_response('budgetline/budgetline_experiment.html',context_instance=RequestContext(request))