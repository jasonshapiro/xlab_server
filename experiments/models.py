import datetime

from django.db import models
from django.contrib.auth.models import User

#ISO 4217: http://www.iso.org/iso/support/faqs/faqs_widely_used_standards/widely_used_standards_other/currency_codes/currency_codes_list-1.htm
#class Currency(models.Model):
#    fullName = models.CharField('ISO 4217 Code', max_length = 3, primary_key=True, help_text='e.g. USD or ZAR');
#    singular = models.CharField('Singular lowercase currency name', max_length = 32, help_text='e.g. dollar or rand')
#    plural = models.CharField('Plural lowercase currency name', max_length = 32, help_text='e.g. dollars or rand')
#    symbol = models.CharField('Currency symbol', max_length = 4, help_text='What goes before a numeric amount, e.g. $ or R, leave a trailing space if you use a three-letter code like \"CNY\"')
#    LEFT_RIGHT_CHOICES = (
#                               (0, 'Left'),
#                               (1, 'Right'),
#                               )
#    leftRight = models.IntegerField(max_length = 1, verbose_name = "Left or right of figure", help_text="Should symbol be left or right of the figure", choices = LEFT_RIGHT_CHOICES, default=0)
#    
#    class Meta:
#       verbose_name_plural = "Currencies"
#    
#    def __unicode__(self):
#        return "%s" % (self.fullName)
     
class Timer(models.Model):
    
    title = models.CharField(max_length=128, unique=True)
    TIMER_TYPE_CHOICES = (
                               (0, 'Static'),
                               (1, 'Dynamic'),
                               )
    timer_type = models.IntegerField(max_length = 1, verbose_name = "Type", help_text="static fixes times, dynamic waits for responses", choices = TIMER_TYPE_CHOICES)
            
    min_interval = models.IntegerField(help_text="In minutes. Applies to dynamic only.",editable = True)
    max_interval = models.IntegerField(help_text="In minutes. Applies to dynamic only.",editable = True)
    
    boolMonday = models.BooleanField(default=False, editable=True, verbose_name = "Active Monday", help_text="Applies to static only.")
    boolTuesday = models.BooleanField(default=False,editable=True, verbose_name = "Active Tuesday", help_text="Applies to static only.")
    boolWednesday = models.BooleanField(default=False, editable=True, verbose_name = "Active Wednesday", help_text="Applies to static only.")
    boolThursday = models.BooleanField(default=False, editable=True, verbose_name = "Active Thursday", help_text="Applies to static only.")
    boolFriday = models.BooleanField(default=False, editable=True, verbose_name = "Active Friday", help_text="Applies to static only.")
    boolSaturday = models.BooleanField(default=False, editable = True, verbose_name = "Active Saturday", help_text="Applies to static only.")
    boolSunday = models.BooleanField(default=False, editable = True, verbose_name = "Active Sunday", help_text="Applies to static only.")
    
    startDate = models.DateField(editable = True, help_text="Applies to static only.")
    endDate = models.DateField(editable = True, help_text="Applies to static only.")
    startTime = models.IntegerField(help_text="In minutes since midnight, applied daily. Applies to static only.", editable = True)
    endTime = models.IntegerField(help_text="In minutes since midnight, applied daily. Applies to static only.", editable = True)
    
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
    number_sessions = models.IntegerField(help_text="Any integer greater than 0. TimerStatic not supported if greater than 1.")    
    lines_per_session = models.IntegerField()
    
    probabilistic = models.BooleanField(default=False)
    
    MONETARY_CHOICES = (
        ('-','-'),
        ('$','$'),
        (u"\u20AA",u"\u20AA"),
        (u"\u20AC",u"\u20AC"),
        (u"\u00A3",u"\u00A3"),
        (u"\u00A5",u"\u00A5"),
        ('CNY ','CNY '),
        ('Rs ','Rs '),
        ('R','R'),
    )
    
    currency = models.CharField(max_length=4, choices=MONETARY_CHOICES, default = '-')

    x_label = models.CharField(max_length=16, blank=True, help_text="e.g. apples")
    x_units = models.CharField(max_length=8, help_text="e.g. pounds")
    x_max = models.FloatField(help_text="in x units")
    x_min = models.FloatField(help_text="in x units")
    
    y_label = models.CharField(max_length=16, blank=True, help_text="e.g. oranges")
    y_units = models.CharField(max_length=8, help_text="e.g. pounds")
    y_max = models.FloatField(help_text="in y units")
    y_min = models.FloatField(help_text="in y units")
    
    prob_x = models.DecimalField(max_digits=7,decimal_places=6,default=0.5, help_text="pertains to probabilistic experiments only")

    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Budget line info"

    def __unicode__(self):
        return "%s" % (self.title)
        
class BudgetLine(models.Model):
#        user = models.ForeignKey(User)
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
    #user = models.ManyToManyField(User, null = True, blank = True, help_text = "Currently a meaningless field.")

    def __unicode__(self):
        return "%s - %s at %s on %s" % (self.id, self.budget_line_info, self.geofence, self.timer)
    
    def save(self, *args, **kwargs):
        if not self.id:
            maxID = 0
            for bl in BudgetLine.objects.all():
                maxID = max(maxID, bl.id)
            for tq in TextQuestion.objects.all():
                maxID = max(maxID, tq.id)
            self.id = maxID + 1
        super(BudgetLine, self).save(*args, **kwargs)

class BudgetLineResult(models.Model):
    user = models.ForeignKey(User, editable=False)
    budget_line_info = models.ForeignKey(BudgetLine, editable=False, null=True)
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
        return "%s - %s" % (self.user, self.budget_line_info)
    
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
    #user = models.ManyToManyField(User)
    
    def __unicode__(self):
        return "%s - %s at %s" % (self.id, self.text_question_info, self.geofence)
    
    def save(self, *args, **kwargs):
        if not self.id:
            maxID = 0
            for bl in BudgetLine.objects.all():
                maxID = max(maxID, bl.id)
            for tq in TextQuestion.objects.all():
                maxID = max(maxID, tq.id)
            self.id = maxID + 1
        super(TextQuestion, self).save(*args, **kwargs)

class TextQuestionResult(models.Model):
    user = models.ForeignKey(User, editable=False)
    text_question_info = models.ForeignKey(TextQuestion, editable=False)
    lat = models.DecimalField(null=True,max_digits=8,decimal_places=6,editable=False)
    lon = models.DecimalField(null=True,max_digits=9,decimal_places=6,editable=False)
    response = models.TextField(editable=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s - %s" % (self.id, self.user)