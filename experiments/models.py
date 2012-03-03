import datetime

from django.db import models
from django.contrib.auth.models import User


#PATRICK: Add Timer class here

class Timer(models.Model):
    
    title = models.CharField(max_length=128, unique=True)
    EXPERIMENT_TYPE_CHOICES = (
    ('0', 'Static'),
    ('1', 'Dynamic'),
    )    
    min_interval = models.IntegerField(help_text="In minutes",editable = True)
    max_interval = models.IntegerField(help_text="In minutes",editable = True)
    
    boolMonday = models.BooleanField(default=False, editable=True)
    boolTuesday = models.BooleanField(default=False,editable=True)
    boolWednesday = models.BooleanField(default=False, editable=True)
    boolThursday = models.BooleanField(default=False, editable=True)
    boolFriday = models.BooleanField(default=False, editable=True)    
    boolSaturday = models.BooleanField(default=False, editable = True)
    boolSunday = models.BooleanField(default=False, editable = True)
    
    startDate = models.DateField(editable = True)
    endDate = models.DateField(editable = True)
    startTime = models.IntegerField(help_text="In minutes", editable = True)
    endTime = models.IntegerField(help_text="In minutes", editable = True)
    
    def __unicode__(self):
        return "%s" % (self.title)

class Geofence(models.Model):
    
    title = models.CharField(max_length=128, unique=True)
    lat = models.FloatField(null=True)
    lon = models.FloatField(null=True)
    radius = models.IntegerField(help_text="In meters.")
    description  = models.TextField(null=True, blank=True)
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
    geofence = models.ForeignKey(Geofence)
    budget_line_info = models.ForeignKey(BudgetLineInfo)
    #PATRICK: Uncomment this:
    timer = models.ForeignKey(Timer)
    user = models.ManyToManyField(User)

    def __unicode__(self):
        return "%s - %s at %s" % (self.id, self.budget_line_info, self.geofence, self.timer)
    
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