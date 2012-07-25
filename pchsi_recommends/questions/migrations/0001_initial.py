# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Question'
        db.create_table('questions_question', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('multiple_choice', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('position', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal('questions', ['Question'])

        # Adding model 'Answer'
        db.create_table('questions_answer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['questions.Question'])),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('position', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal('questions', ['Answer'])

        # Adding M2M table for field populations on 'Answer'
        db.create_table('questions_answer_populations', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('answer', models.ForeignKey(orm['questions.answer'], null=False)),
            ('population', models.ForeignKey(orm['populations.population'], null=False))
        ))
        db.create_unique('questions_answer_populations', ['answer_id', 'population_id'])


    def backwards(self, orm):
        # Deleting model 'Question'
        db.delete_table('questions_question')

        # Deleting model 'Answer'
        db.delete_table('questions_answer')

        # Removing M2M table for field populations on 'Answer'
        db.delete_table('questions_answer_populations')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'populations.population': {
            'Meta': {'object_name': 'Population'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'short': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        'populations.population_relationship': {
            'Meta': {'object_name': 'Population_Relationship'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'country': ('django_countries.fields.CountryField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inclusive': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'max_age': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'min_age': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'populations': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['populations.Population']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'questions.answer': {
            'Meta': {'ordering': "['position']", 'object_name': 'Answer'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'populations': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['populations.Population']", 'symmetrical': 'False', 'blank': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questions.Question']"}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        'questions.question': {
            'Meta': {'ordering': "['position']", 'object_name': 'Question'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'multiple_choice': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        }
    }

    complete_apps = ['questions']