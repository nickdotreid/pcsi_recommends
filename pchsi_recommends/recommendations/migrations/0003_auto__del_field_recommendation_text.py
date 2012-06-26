# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Recommendation.text'
        db.delete_column('recommendations_recommendation', 'text')


    def backwards(self, orm):
        # Adding field 'Recommendation.text'
        db.add_column('recommendations_recommendation', 'text',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)


    models = {
        'recommendations.population': {
            'Meta': {'object_name': 'Population'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '120'})
        },
        'recommendations.recommendation': {
            'Meta': {'object_name': 'Recommendation'},
            'add_populations': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'frequency': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_age': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'min_age': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'not_recommended': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'populations': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['recommendations.Population']", 'symmetrical': 'False', 'blank': 'True'}),
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