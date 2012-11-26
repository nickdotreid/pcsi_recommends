# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Answer.order'
        db.delete_column('questions_answer', 'order')

        # Adding field 'Answer.position'
        db.add_column('questions_answer', 'position',
                      self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Question.order'
        db.delete_column('questions_question', 'order')

        # Adding field 'Question.position'
        db.add_column('questions_question', 'position',
                      self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Answer.order'
        db.add_column('questions_answer', 'order',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=1, db_index=True),
                      keep_default=False)

        # Deleting field 'Answer.position'
        db.delete_column('questions_answer', 'position')

        # Adding field 'Question.order'
        db.add_column('questions_question', 'order',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=1, db_index=True),
                      keep_default=False)

        # Deleting field 'Question.position'
        db.delete_column('questions_question', 'position')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'populations.population': {
            'Meta': {'ordering': "['short']", 'object_name': 'Population'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['populations.PopulationCatagory']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'short': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        'populations.population_relationship': {
            'Meta': {'object_name': 'Population_Relationship'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inclusive': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'max_age': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'max_year': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'min_age': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'min_year': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'populations': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['populations.Population']", 'symmetrical': 'False', 'blank': 'True'}),
            'regions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['populations.RegionCollection']", 'null': 'True', 'blank': 'True'})
        },
        'populations.populationcatagory': {
            'Meta': {'ordering': "['position']", 'object_name': 'PopulationCatagory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'multiple': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'short': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        'populations.region': {
            'Meta': {'object_name': 'Region'},
            'country': ('django_countries.fields.CountryField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '120', 'null': 'True', 'blank': 'True'})
        },
        'populations.regioncollection': {
            'Meta': {'object_name': 'RegionCollection'},
            'exclude': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '120', 'null': 'True', 'blank': 'True'}),
            'regions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['populations.Region']", 'symmetrical': 'False'})
        },
        'questions.answer': {
            'Meta': {'ordering': "['position']", 'object_name': 'Answer'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'populations': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['populations.Population']", 'symmetrical': 'False', 'blank': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questions.Question']"}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        'questions.question': {
            'Meta': {'ordering': "['position']", 'object_name': 'Question'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'multiple_choice': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        }
    }

    complete_apps = ['questions']