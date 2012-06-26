# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Question.short'
        db.delete_column('questions_question', 'short')


    def backwards(self, orm):
        # Adding field 'Question.short'
        db.add_column('questions_question', 'short',
                      self.gf('django.db.models.fields.CharField')(default=False, max_length=50, unique=True),
                      keep_default=False)


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