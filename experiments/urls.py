from django.conf.urls.defaults import *

urlpatterns = patterns('experiments.views',
    url(r'^api/budget/', 'budget_lines'),
    url(r'^api/text/', 'text_questions'),
)