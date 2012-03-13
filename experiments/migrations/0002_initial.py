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
            ('experimentType', self.gf('django.db.models.fields.IntegerField')(max_length=1)),
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

        # Adding model 'BudgetLineInfo'
        db.create_table('experiments_budgetlineinfo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('number_sessions', self.gf('django.db.models.fields.IntegerField')()),
            ('lines_per_session', self.gf('django.db.models.fields.IntegerField')()),
            ('probabilistic', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('x_label', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('x_units', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('x_max', self.gf('django.db.models.fields.FloatField')()),
            ('x_min', self.gf('django.db.models.fields.FloatField')()),
            ('y_label', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('y_units', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('y_max', self.gf('django.db.models.fields.FloatField')()),
            ('y_min', self.gf('django.db.models.fields.FloatField')()),
            ('prob_x', self.gf('django.db.models.fields.DecimalField')(default=0.5, max_digits=7, decimal_places=6)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('experiments', ['BudgetLineInfo'])

        # Adding model 'BudgetLine'
        db.create_table('experiments_budgetline', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('geofence', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['experiments.Geofence'], null=True, blank=True)),
            ('budget_line_info', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['experiments.BudgetLineInfo'])),
            ('timer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['experiments.Timer'])),
            ('timer_status', self.gf('django.db.models.fields.IntegerField')(max_length=1)),
        ))
        db.send_create_signal('experiments', ['BudgetLine'])

        # Adding M2M table for field user on 'BudgetLine'
        db.create_table('experiments_budgetline_user', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('budgetline', models.ForeignKey(orm['experiments.budgetline'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('experiments_budgetline_user', ['budgetline_id', 'user_id'])

        # Adding model 'BudgetLineResult'
        db.create_table('experiments_budgetlineresult', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('budget_line_info', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['experiments.BudgetLine'])),
            ('session', self.gf('django.db.models.fields.IntegerField')(default=-1)),
            ('line', self.gf('django.db.models.fields.IntegerField')(default=-1)),
            ('x', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
            ('y', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
            ('x_intercept', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
            ('y_intercept', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
            ('lat', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=6)),
            ('lon', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=9, decimal_places=6)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('winner', self.gf('django.db.models.fields.CharField')(default='-', max_length=1)),
            ('line_chosen_boolean', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('experiments', ['BudgetLineResult'])

        # Adding model 'TextQuestionInfo'
        db.create_table('experiments_textquestioninfo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.TextField')()),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('experiments', ['TextQuestionInfo'])

        # Adding model 'TextQuestion'
        db.create_table('experiments_textquestion', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('geofence', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['experiments.Geofence'])),
            ('text_question_info', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['experiments.TextQuestionInfo'])),
        ))
        db.send_create_signal('experiments', ['TextQuestion'])

        # Adding M2M table for field user on 'TextQuestion'
        db.create_table('experiments_textquestion_user', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('textquestion', models.ForeignKey(orm['experiments.textquestion'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('experiments_textquestion_user', ['textquestion_id', 'user_id'])

        # Adding model 'TextQuestionResult'
        db.create_table('experiments_textquestionresult', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('text_question_info', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['experiments.TextQuestion'])),
            ('lat', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=6)),
            ('lon', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=9, decimal_places=6)),
            ('response', self.gf('django.db.models.fields.TextField')()),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('experiments', ['TextQuestionResult'])


    def backwards(self, orm):
        
        # Deleting model 'Timer'
        db.delete_table('experiments_timer')

        # Deleting model 'Geofence'
        db.delete_table('experiments_geofence')

        # Deleting model 'BudgetLineInfo'
        db.delete_table('experiments_budgetlineinfo')

        # Deleting model 'BudgetLine'
        db.delete_table('experiments_budgetline')

        # Removing M2M table for field user on 'BudgetLine'
        db.delete_table('experiments_budgetline_user')

        # Deleting model 'BudgetLineResult'
        db.delete_table('experiments_budgetlineresult')

        # Deleting model 'TextQuestionInfo'
        db.delete_table('experiments_textquestioninfo')

        # Deleting model 'TextQuestion'
        db.delete_table('experiments_textquestion')

        # Removing M2M table for field user on 'TextQuestion'
        db.delete_table('experiments_textquestion_user')

        # Deleting model 'TextQuestionResult'
        db.delete_table('experiments_textquestionresult')


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
            'timer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['experiments.Timer']"}),
            'timer_status': ('django.db.models.fields.IntegerField', [], {'max_length': '1'}),
            'user': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'experiments.budgetlineinfo': {
            'Meta': {'object_name': 'BudgetLineInfo'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lines_per_session': ('django.db.models.fields.IntegerField', [], {}),
            'number_sessions': ('django.db.models.fields.IntegerField', [], {}),
            'prob_x': ('django.db.models.fields.DecimalField', [], {'default': '0.5', 'max_digits': '7', 'decimal_places': '6'}),
            'probabilistic': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'x_label': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'x_max': ('django.db.models.fields.FloatField', [], {}),
            'x_min': ('django.db.models.fields.FloatField', [], {}),
            'x_units': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'y_label': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'y_max': ('django.db.models.fields.FloatField', [], {}),
            'y_min': ('django.db.models.fields.FloatField', [], {}),
            'y_units': ('django.db.models.fields.CharField', [], {'max_length': '8'})
        },
        'experiments.budgetlineresult': {
            'Meta': {'object_name': 'BudgetLineResult'},
            'budget_line_info': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['experiments.BudgetLine']"}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '6'}),
            'line': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'line_chosen_boolean': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lon': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '6'}),
            'session': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'winner': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '1'}),
            'x': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'x_intercept': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'y': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
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
            'geofence': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['experiments.Geofence']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'text_question_info': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['experiments.TextQuestionInfo']"}),
            'user': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False'})
        },
        'experiments.textquestioninfo': {
            'Meta': {'object_name': 'TextQuestionInfo'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.TextField', [], {})
        },
        'experiments.textquestionresult': {
            'Meta': {'object_name': 'TextQuestionResult'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '6'}),
            'lon': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '6'}),
            'response': ('django.db.models.fields.TextField', [], {}),
            'text_question_info': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['experiments.TextQuestion']"}),
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
            'experimentType': ('django.db.models.fields.IntegerField', [], {'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_interval': ('django.db.models.fields.IntegerField', [], {}),
            'min_interval': ('django.db.models.fields.IntegerField', [], {}),
            'startDate': ('django.db.models.fields.DateField', [], {}),
            'startTime': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        }
    }

    complete_apps = ['experiments']
