from django.conf.urls.defaults import *

urlpatterns = patterns('experiments.views',
    url(r'^budgetline_experiment/', 'budgetline_experiment')
)