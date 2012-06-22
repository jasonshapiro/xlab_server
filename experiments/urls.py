from django.conf.urls.defaults import *

urlpatterns = patterns('experiments.views',
    url(r'^budgetline_experiment/', 'budgetline_experiment'),
    url(r'^budgetline_consent/', 'budgetline_consent'),
    url(r'^budgetline_instructions/', 'budgetline_instructions')
)