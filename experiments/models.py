import datetime

from django.db import models
from django.contrib.auth.models import User


#PATRICK: Add Timer class here

class Timer(models.Model):
    
    title = models.CharField(max_length=128, unique=True)
    TIMER_TYPE_CHOICES = (
                               (0, 'Static'),
                               (1, 'Dynamic'),
                               )
    experimentType = models.IntegerField(max_length = 1, verbose_name = "Type", help_text="static fixes times, dynamic waits for responses", choices = TIMER_TYPE_CHOICES)
            
    min_interval = models.IntegerField(help_text="In minutes.",editable = True)
    max_interval = models.IntegerField(help_text="In minutes.",editable = True)
    
    boolMonday = models.BooleanField(default=False, editable=True, verbose_name = "Active Monday")
    boolTuesday = models.BooleanField(default=False,editable=True, verbose_name = "Active Tuesday")
    boolWednesday = models.BooleanField(default=False, editable=True, verbose_name = "Active Wednesday")
    boolThursday = models.BooleanField(default=False, editable=True, verbose_name = "Active Thursday")
    boolFriday = models.BooleanField(default=False, editable=True, verbose_name = "Active Friday")
    boolSaturday = models.BooleanField(default=False, editable = True, verbose_name = "Active Saturday")
    boolSunday = models.BooleanField(default=False, editable = True, verbose_name = "Active Sunday")
    
    startDate = models.DateField(editable = True)
    endDate = models.DateField(editable = True)
    startTime = models.IntegerField(help_text="In minutes since midnight, applied daily.", editable = True)
    endTime = models.IntegerField(help_text="In minutes since midnight, applied daily.", editable = True)
    
    def __unicode__(self):
        return "%s" % (self.title)

class Geofence(models.Model):
    
    title = models.CharField(max_length=128, unique=True)
    lat = models.FloatField()
    lon = models.FloatField()
    radius = models.IntegerField(help_text="In meters.")
    description  = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s" % (self.title)

class BudgetLineInfo(models.Model):
    
    title = models.CharField(max_length=128)
    number_sessions = models.IntegerField()    
    lines_per_session = models.IntegerField()
    
    probabilistic = models.BooleanField(default=False)
    
    x_label = models.CharField(max_length=16, blank=True)
    x_units = models.CharField(max_length=8)
    x_max = models.FloatField()
    x_min = models.FloatField()
    
    y_label = models.CharField(max_length=16, blank=True)
    y_units = models.CharField(max_length=8)
    y_max = models.FloatField()
    y_min = models.FloatField()
    
    prob_x = models.DecimalField(max_digits=7,decimal_places=6,default=0.5)

    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Budget line info"

    def __unicode__(self):
        return "%s" % (self.title)
        
class BudgetLine(models.Model):
    id = models.IntegerField(primary_key=True, editable=False)
    geofence = models.ForeignKey(Geofence, blank=True, null=True,help_text = "For reminders only. Can be blank")
    budget_line_info = models.ForeignKey(BudgetLineInfo)
    timer = models.ForeignKey(Timer, help_text = "Must select always, but irrelevant if timer status is None.")
    TIMER_STATUS_CHOICES = (
                            (0, 'None'),
                            (1, 'Reminder Only'),
                            (2, 'Restrictive'),
                            )
    timer_status = models.IntegerField(max_length = 1, verbose_name = "timer status", help_text = "Restrictive timers make a subject wait to complete an experiment segment", choices = TIMER_STATUS_CHOICES)
    user = models.ManyToManyField(User, null = True, blank = True, help_text = "Currently a meaningless field.")

    def __unicode__(self):
        return "%s - %s at %s on %s" % (self.id, self.budget_line_info, self.geofence, self.timer)
    
    def save(self):
        if not self.id:
            maxID = 0
            for bl in BudgetLine.objects.all():
                maxID = max(maxID, bl.id)
            for tq in TextQuestion.objects.all():
                maxID = max(maxID, tq.id)
            self.id = maxID + 1
        super(BudgetLine, self).save()

class BudgetLineResult(models.Model):
    user = models.ForeignKey(User, editable=False)
    budget_line_info = models.ForeignKey(BudgetLine, editable=False)
    session = models.IntegerField(editable=False, default=-1)
    line = models.IntegerField(editable=False, default=-1)
    x = models.DecimalField(max_digits=6,decimal_places=2,editable=False)
    y = models.DecimalField(max_digits=6,decimal_places=2,editable=False)
    x_intercept = models.DecimalField(max_digits=6,decimal_places=2,editable=False)
    y_intercept = models.DecimalField(max_digits=6,decimal_places=2,editable=False)
    lat = models.DecimalField(null=True,max_digits=8,decimal_places=6,editable=False)
    lon = models.DecimalField(null=True,max_digits=9,decimal_places=6,editable=False)
    created_date = models.DateTimeField(auto_now_add=True)
    winner = models.CharField(max_length = 1, default="-", editable=False)
    line_chosen_boolean = models.BooleanField(editable=False)

    def __unicode__(self):
        return "%s - %s" % (self.user, self.queryLocationPair)
    
class TextQuestionInfo(models.Model):
    question = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s" % (self.question)
    
    class Meta:
        verbose_name_plural = "text question info"
    
class TextQuestion (models.Model):
    id = models.IntegerField(primary_key=True,editable=False)
    geofence = models.ForeignKey(Geofence)
    text_question_info = models.ForeignKey(TextQuestionInfo)
    user = models.ManyToManyField(User)
    
    def __unicode__(self):
        return "%s - %s at %s" % (self.id, self.text_question_info, self.geofence)
    
    def save(self):
        if not self.id:
            maxID = 0
            for bl in BudgetLine.objects.all():
                maxID = max(maxID, bl.id)
            for tq in TextQuestion.objects.all():
                maxID = max(maxID, tq.id)
            self.id = maxID + 1
        super(TextQuestion, self).save()

class TextQuestionResult(models.Model):
    user = models.ForeignKey(User, editable=False)
    text_question_info = models.ForeignKey(TextQuestion, editable=False)
    lat = models.DecimalField(null=True,max_digits=8,decimal_places=6,editable=False)
    lon = models.DecimalField(null=True,max_digits=9,decimal_places=6,editable=False)
    response = models.TextField(editable=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s - %s" % (self.id, self.user)