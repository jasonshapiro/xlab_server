from django.conf.urls.defaults import *
from api import BudgetLineResource

urlpatterns = patterns('experiments.views',
    url('/', include(BudgetLineResource().urls)),
    url(r'^api/budget/', 'budget_lines'),
    url(r'^api/text/', 'text_questions'),
    
)