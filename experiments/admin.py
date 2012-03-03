from experiments.models import *
from django.contrib import admin

class TimerAdmin(admin.ModelAdmin):
    list_display = ('title', 'EXPERIMENT_TYPE_CHOICES', 'min_interval', 'max_interval', 'boolMonday', 'boolTuesday',
                'boolWednesday', 'boolThursday', 'boolFriday', 'boolSaturday', 'boolSunday', 'startDate', 
                'endDate', 'startTime', 'endTime')

class GeoFenceAdmin(admin.ModelAdmin):
    list_display = ('id',  'title', 'lat', 'lon', 'radius', 'description', 'created_date')

class BudgetLineAdmin(admin.ModelAdmin):
    list_display = ('id', 'budget_line_info', 'geofence')

class BudgetLineInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'number_sessions', 'lines_per_session',
                    'probabilistic',
                    'x_label', 'x_units', 'x_max', 'x_min',
                    'y_label', 'y_units', 'y_max', 'y_min',
                    'prob_x',
                    'created_date')
"""    
    fieldsets = (
                 (None,
                    {'fields':('title', 'number_sessions', 'lines_per_session',
                    'probabilistic',
                    'x_label', 'x_units', 'x_max', 'x_min',
                    'y_label', 'y_units', 'y_max', 'y_min',
                    'prob_x')}),
                 )
"""
class BudgetLineResultAdmin(admin.ModelAdmin):
    list_display = ('user',  'budget_line_info', 'session', 'line', 'x', 'y', 'x_intercept', 'y_intercept', "winner", "line_chosen_boolean",
                    'lat', 'lon', 'created_date')

class TextQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'text_question_info', 'geofence')

class TextQuestionInfoAdmin(admin.ModelAdmin):
    list_display = ('id',  'question', 'created_date')

class TextQuestionResultAdmin(admin.ModelAdmin):
    list_display = ('id',  'user', 'text_question_info', 'response', 'created_date')

admin.site.register(Timer, TimerAdmin)
admin.site.register(Geofence, GeoFenceAdmin)
admin.site.register(BudgetLine,BudgetLineAdmin)
admin.site.register(BudgetLineInfo,BudgetLineInfoAdmin)
admin.site.register(BudgetLineResult,BudgetLineResultAdmin)
admin.site.register(TextQuestion, TextQuestionAdmin)
admin.site.register(TextQuestionInfo,TextQuestionInfoAdmin)
admin.site.register(TextQuestionResult, TextQuestionResultAdmin)