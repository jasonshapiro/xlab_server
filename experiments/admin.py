from experiments.models import *
from django.contrib import admin

class TimerAdmin(admin.ModelAdmin):
    list_display = ('title', 'timer_type', 'min_interval', 'max_interval', 'boolMonday', 'boolTuesday',
                'boolWednesday', 'boolThursday', 'boolFriday', 'boolSaturday', 'boolSunday', 'startDate', 
                'endDate', 'startTime', 'endTime')

class GeoFenceAdmin(admin.ModelAdmin):
    list_display = ('id',  'title', 'lat', 'lon', 'radius', 'description', 'created_date')

class BudgetLineAdmin(admin.ModelAdmin):
    list_display = ('id', 'budget_line_info', 'number_sessions', 'geofence', 'timer', 'timer_status', 'usernames')

class TextQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'text_question_info', 'number_sessions', 'geofence', 'timer', 'timer_status', 'usernames')

class BudgetLineInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',
                    'probabilistic', 'currency',
                    'x_label', 'x_units', 'x_max', 'x_min',
                    'y_label', 'y_units', 'y_max', 'y_min',
                    'prob_x',
                    'created_date')

class BudgetLineResponseAdmin(admin.ModelAdmin):
    list_display = ('id',  'user',  'created_date', 'lat', 'lon', 'budget_line', 'session', 'x', 'y', 'x_intercept', 'y_intercept', "winner", "line_chosen_boolean",
                    'eligible_for_answer')

class TextQuestionInfoAdmin(admin.ModelAdmin):
    list_display = ('id',  'question', 'created_date')

class TextQuestionResponseAdmin(admin.ModelAdmin):
    list_display = ('id',  'user', 'created_date', 'lat', 'lon', 'text_question', 'session', 'answer', 'eligible_for_answer')

class TextQuestionInputAdmin(admin.ModelAdmin):
    list_display = ('id',  'user', 'created_date', 'lat', 'lon', 'text_question_response', 'answer')

admin.site.register(Timer, TimerAdmin)
admin.site.register(Geofence, GeoFenceAdmin)
admin.site.register(BudgetLine,BudgetLineAdmin)
admin.site.register(BudgetLineInfo,BudgetLineInfoAdmin)
admin.site.register(BudgetLineResponse,BudgetLineResponseAdmin)
admin.site.register(TextQuestion,TextQuestionAdmin)
admin.site.register(TextQuestionInfo,TextQuestionInfoAdmin)
admin.site.register(TextQuestionResponse, TextQuestionResponseAdmin)
admin.site.register(TextQuestionInput, TextQuestionInputAdmin)