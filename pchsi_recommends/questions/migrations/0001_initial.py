# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Questionnaire'
        db.create_table('questions_questionnaire', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('short', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('directions', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('questions', ['Questionnaire'])

        # Adding model 'Question'
        db.create_table('questions_question', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('questionnaire', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['questions.Questionnaire'])),
            ('short', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
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
            ('population', models.ForeignKey(orm['recommendations.population'], null=False))
        ))
        db.create_unique('questions_answer_populations', ['answer_id', 'population_id'])


    def backwards(self, orm):
        # Deleting model 'Questionnaire'
        db.delete_table('questions_questionnaire')

        # Deleting model 'Question'
        db.delete_table('questions_question')

        # Deleting model 'Answer'
        db.delete_table('questions_answer')

        # Removing M2M table for field populations on 'Answer'
        db.delete_table('questions_answer_populations')


    models = {
        'questions.answer': {
            'Meta': {'ordering': "['position']", 'object_name': 'Answer'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'populations': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['recommendations.Population']", 'symmetrical': 'False'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questions.Question']"}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        'questions.question': {
            'Meta': {'ordering': "['position']", 'object_name': 'Question'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'questionnaire': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questions.Questionnaire']"}),
            'short': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        'questions.questionnaire': {
            'Meta': {'object_name': 'Questionnaire'},
            'directions': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'short': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        'recommendations.population': {
            'Meta': {'object_name': 'Population'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '120'})
        }
    }

    complete_apps = ['questions']