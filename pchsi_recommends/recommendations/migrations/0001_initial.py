# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Screen'
        db.create_table('recommendations_screen', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=120)),
        ))
        db.send_create_signal('recommendations', ['Screen'])

        # Adding model 'Population'
        db.create_table('recommendations_population', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=120)),
        ))
        db.send_create_signal('recommendations', ['Population'])

        # Adding model 'Recommendation'
        db.create_table('recommendations_recommendation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('screen', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['recommendations.Screen'])),
            ('text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('frequency', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('weight', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('min_age', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('max_age', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('recommendations', ['Recommendation'])

        # Adding M2M table for field populations on 'Recommendation'
        db.create_table('recommendations_recommendation_populations', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('recommendation', models.ForeignKey(orm['recommendations.recommendation'], null=False)),
            ('population', models.ForeignKey(orm['recommendations.population'], null=False))
        ))
        db.create_unique('recommendations_recommendation_populations', ['recommendation_id', 'population_id'])


    def backwards(self, orm):
        # Deleting model 'Screen'
        db.delete_table('recommendations_screen')

        # Deleting model 'Population'
        db.delete_table('recommendations_population')

        # Deleting model 'Recommendation'
        db.delete_table('recommendations_recommendation')

        # Removing M2M table for field populations on 'Recommendation'
        db.delete_table('recommendations_recommendation_populations')


    models = {
        'recommendations.population': {
            'Meta': {'object_name': 'Population'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '120'})
        },
        'recommendations.recommendation': {
            'Meta': {'object_name': 'Recommendation'},
            'frequency': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_age': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'min_age': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'populations': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['recommendations.Population']", 'symmetrical': 'False'}),
            'screen': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['recommendations.Screen']"}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'weight': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'recommendations.screen': {
            'Meta': {'object_name': 'Screen'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '120'})
        }
    }

    complete_apps = ['recommendations']