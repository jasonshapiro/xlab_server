from django.conf.urls.defaults import *

urlpatterns = patterns('experiments.views',
    url(r'^budget/', 'budget_lines'),
    url(r'^text/', 'text_questions'),
    url(r'^budgetline_experiment/', 'budgetline_experiment')
)