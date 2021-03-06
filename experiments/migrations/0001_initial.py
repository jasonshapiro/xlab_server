# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Timer'
        db.create_table('experiments_timer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('timer_type', self.gf('django.db.models.fields.IntegerField')(max_length=1)),
            ('min_interval', self.gf('django.db.models.fields.IntegerField')()),
            ('max_interval', self.gf('django.db.models.fields.IntegerField')()),
            ('boolMonday', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('boolTuesday', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('boolWednesday', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('boolThursday', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('boolFriday', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('boolSaturday', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('boolSunday', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('startDate', self.gf('django.db.models.fields.DateField')()),
            ('endDate', self.gf('django.db.models.fields.DateField')()),
            ('startTime', self.gf('django.db.models.fields.IntegerField')()),
            ('endTime', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('experiments', ['Timer'])

        # Adding model 'Geofence'
        db.create_table('experiments_geofence', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('lat', self.gf('django.db.models.fields.FloatField')()),
            ('lon', self.gf('django.db.models.fields.FloatField')()),
            ('radius', self.gf('django.db.models.fields.IntegerField')()),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('experiments', ['Geofence'])

        # Adding model 'TextQuestionInfo'
        db.create_table('experiments_textquestioninfo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('experiments', ['TextQuestionInfo'])

        # Adding model 'BudgetLineInfo'
        db.create_table('experiments_budgetlineinfo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('probabilistic', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('currency', self.gf('django.db.models.fields.CharField')(default='-', max_length=4)),
            ('x_label', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('x_units', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('x_max', self.gf('django.db.models.fields.FloatField')()),
            ('x_min', self.gf('django.db.models.fields.FloatField')()),
            ('y_label', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('y_units', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('y_max', self.gf('django.db.models.fields.FloatField')()),
            ('y_min', self.gf('django.db.models.fields.FloatField')()),
            ('prob_x', self.gf('django.db.models.fields.DecimalField')(default=0.5, max_digits=7, decimal_places=6)),
        ))
        db.send_create_signal('experiments', ['BudgetLineInfo'])

        # Adding model 'BudgetLine'
        db.create_table('experiments_budgetline', (
            ('geofence', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['experiments.Geofence'], null=True, blank=True)),
            ('number_sessions', self.gf('django.db.models.fields.IntegerField')()),
            ('timer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['experiments.Timer'], null=True, blank=True)),
            ('timer_status', self.gf('django.db.models.fields.IntegerField')(max_length=1)),
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('budget_line_info', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['experiments.BudgetLineInfo'])),
        ))
        db.send_create_signal('experiments', ['BudgetLine'])

        # Adding M2M table for field users on 'BudgetLine'
        db.create_table('experiments_budgetline_users', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('budgetline', models.ForeignKey(orm['experiments.budgetline'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('experiments_budgetline_users', ['budgetline_id', 'user_id'])

        # Adding model 'TextQuestion'
        db.create_table('experiments_textquestion', (
            ('geofence', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['experiments.Geofence'], null=True, blank=True)),
            ('number_sessions', self.gf('django.db.models.fields.IntegerField')()),
            ('timer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['experiments.Timer'], null=True, blank=True)),
            ('timer_status', self.gf('django.db.models.fields.IntegerField')(max_length=1)),
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('text_question_info', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['experiments.TextQuestionInfo'])),
        ))
        db.send_create_signal('experiments', ['TextQuestion'])

        # Adding M2M table for field users on 'TextQuestion'
        db.create_table('experiments_textquestion_users', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('textquestion', models.ForeignKey(orm['experiments.textquestion'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('experiments_textquestion_users', ['textquestion_id', 'user_id'])

        # Adding model 'BudgetLineResponse'
        db.create_table('experiments_budgetlineresponse', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('eligible_for_answer', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('lat', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=6)),
            ('lon', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=9, decimal_places=6)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('session', self.gf('django.db.models.fields.IntegerField')(default=-1)),
            ('budget_line', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['experiments.BudgetLine'])),
            ('x', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=6, decimal_places=2)),
            ('y', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=6, decimal_places=2)),
            ('x_intercept', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
            ('y_intercept', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
            ('winner', self.gf('django.db.models.fields.CharField')(default='-', max_length=1)),
            ('line_chosen_boolean', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
        ))
        db.send_create_signal('experiments', ['BudgetLineResponse'])

        # Adding model 'TextQuestionResponse'
        db.create_table('experiments_textquestionresponse', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('eligible_for_answer', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('lat', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=6)),
            ('lon', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=9, decimal_places=6)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('session', self.gf('django.db.models.fields.IntegerField')(default=-1)),
            ('text_question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['experiments.TextQuestion'])),
            ('answer', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('experiments', ['TextQuestionResponse'])

        # Adding model 'BudgetLineInput'
        db.create_table('experiments_budgetlineinput', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('lat', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=6)),
            ('lon', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=9, decimal_places=6)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('budget_line_response', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['experiments.BudgetLineResponse'])),
            ('progress', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal('experiments', ['BudgetLineInput'])

        # Adding model 'TextQuestionInput'
        db.create_table('experiments_textquestioninput', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('lat', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=6)),
            ('lon', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=9, decimal_places=6)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('text_question_response', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['experiments.TextQuestionResponse'])),
            ('answer', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal('experiments', ['TextQuestionInput'])


    def backwards(self, orm):
        
        # Deleting model 'Timer'
        db.delete_table('experiments_timer')

        # Deleting model 'Geofence'
        db.delete_table('experiments_geofence')

        # Deleting model 'TextQuestionInfo'
        db.delete_table('experiments_textquestioninfo')

        # Deleting model 'BudgetLineInfo'
        db.delete_table('experiments_budgetlineinfo')

        # Deleting model 'BudgetLine'
        db.delete_table('experiments_budgetline')

        # Removing M2M table for field users on 'BudgetLine'
        db.delete_table('experiments_budgetline_users')

        # Deleting model 'TextQuestion'
        db.delete_table('experiments_textquestion')

        # Removing M2M table for field users on 'TextQuestion'
        db.delete_table('experiments_textquestion_users')

        # Deleting model 'BudgetLineResponse'
        db.delete_table('experiments_budgetlineresponse')

        # Deleting model 'TextQuestionResponse'
        db.delete_table('experiments_textquestionresponse')

        # Deleting model 'BudgetLineInput'
        db.delete_table('experiments_budgetlineinput')

        # Deleting model 'TextQuestionInput'
        db.delete_table('experiments_textquestioninput')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'experiments.budgetline': {
            'Meta': {'object_name': 'BudgetLine'},
            'budget_line_info': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['experiments.BudgetLineInfo']"}),
            'geofence': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['experiments.Geofence']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'number_sessions': ('django.db.models.fields.IntegerField', [], {}),
            'timer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['experiments.Timer']", 'null': 'True', 'blank': 'True'}),
            'timer_status': ('django.db.models.fields.IntegerField', [], {'max_length': '1'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'experiments.budgetlineinfo': {
            'Meta': {'object_name': 'BudgetLineInfo'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'currency': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '4'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'prob_x': ('django.db.models.fields.DecimalField', [], {'default': '0.5', 'max_digits': '7', 'decimal_places': '6'}),
            'probabilistic': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'x_label': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'x_max': ('django.db.models.fields.FloatField', [], {}),
            'x_min': ('django.db.models.fields.FloatField', [], {}),
            'x_units': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'y_label': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'y_max': ('django.db.models.fields.FloatField', [], {}),
            'y_min': ('django.db.models.fields.FloatField', [], {}),
            'y_units': ('django.db.models.fields.CharField', [], {'max_length': '8'})
        },
        'experiments.budgetlineinput': {
            'Meta': {'object_name': 'BudgetLineInput'},
            'budget_line_response': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['experiments.BudgetLineResponse']"}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '6'}),
            'lon': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '6'}),
            'progress': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'experiments.budgetlineresponse': {
            'Meta': {'object_name': 'BudgetLineResponse'},
            'budget_line': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['experiments.BudgetLine']"}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'eligible_for_answer': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '6'}),
            'line_chosen_boolean': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'lon': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '6'}),
            'session': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'winner': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '1'}),
            'x': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '2'}),
            'x_intercept': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'y': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '2'}),
            'y_intercept': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'})
        },
        'experiments.geofence': {
            'Meta': {'object_name': 'Geofence'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {}),
            'lon': ('django.db.models.fields.FloatField', [], {}),
            'radius': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        'experiments.textquestion': {
            'Meta': {'object_name': 'TextQuestion'},
            'geofence': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['experiments.Geofence']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'number_sessions': ('django.db.models.fields.IntegerField', [], {}),
            'text_question_info': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['experiments.TextQuestionInfo']"}),
            'timer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['experiments.Timer']", 'null': 'True', 'blank': 'True'}),
            'timer_status': ('django.db.models.fields.IntegerField', [], {'max_length': '1'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'experiments.textquestioninfo': {
            'Meta': {'object_name': 'TextQuestionInfo'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        'experiments.textquestioninput': {
            'Meta': {'object_name': 'TextQuestionInput'},
            'answer': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '6'}),
            'lon': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '6'}),
            'text_question_response': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['experiments.TextQuestionResponse']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'experiments.textquestionresponse': {
            'Meta': {'object_name': 'TextQuestionResponse'},
            'answer': ('django.db.models.fields.TextField', [], {}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'eligible_for_answer': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '6'}),
            'lon': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '6'}),
            'session': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'text_question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['experiments.TextQuestion']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'experiments.timer': {
            'Meta': {'object_name': 'Timer'},
            'boolFriday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'boolMonday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'boolSaturday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'boolSunday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'boolThursday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'boolTuesday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'boolWednesday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'endDate': ('django.db.models.fields.DateField', [], {}),
            'endTime': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_interval': ('django.db.models.fields.IntegerField', [], {}),
            'min_interval': ('django.db.models.fields.IntegerField', [], {}),
            'startDate': ('django.db.models.fields.DateField', [], {}),
            'startTime': ('django.db.models.fields.IntegerField', [], {}),
            'timer_type': ('django.db.models.fields.IntegerField', [], {'max_length': '1'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        }
    }

    complete_apps = ['experiments']
