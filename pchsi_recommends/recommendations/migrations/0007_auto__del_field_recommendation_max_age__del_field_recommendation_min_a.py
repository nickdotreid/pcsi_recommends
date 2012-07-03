# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Recommendation.max_age'
        db.delete_column('recommendations_recommendation', 'max_age')

        # Deleting field 'Recommendation.min_age'
        db.delete_column('recommendations_recommendation', 'min_age')

        # Adding field 'Population_Relationship.min_age'
        db.add_column('recommendations_population_relationship', 'min_age',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Population_Relationship.max_age'
        db.add_column('recommendations_population_relationship', 'max_age',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Recommendation.max_age'
        db.add_column('recommendations_recommendation', 'max_age',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Recommendation.min_age'
        db.add_column('recommendations_recommendation', 'min_age',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Population_Relationship.min_age'
        db.delete_column('recommendations_population_relationship', 'min_age')

        # Deleting field 'Population_Relationship.max_age'
        db.delete_column('recommendations_population_relationship', 'max_age')


    models = {
        'recommendations.population': {
            'Meta': {'object_name': 'Population'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '120'})
        },
        'recommendations.population_relationship': {
            'Meta': {'object_name': 'Population_Relationship'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inclusive': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'max_age': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'min_age': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'populations': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['recommendations.Population']", 'symmetrical': 'False', 'blank': 'True'}),
            'recommendation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['recommendations.Recommendation']"})
        },
        'recommendations.recommendation': {
            'Meta': {'object_name': 'Recommendation'},
            'frequency': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'not_recommended': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'screen': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['recommendations.Screen']"}),
            'weight': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        },
        'recommendations.screen': {
            'Meta': {'object_name': 'Screen'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '120'})
        }
    }

    complete_apps = ['recommendations']