# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Population_Relationship'
        db.create_table('recommendations_population_relationship', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('inclusive', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('recommendations', ['Population_Relationship'])

        # Adding M2M table for field populations on 'Population_Relationship'
        db.create_table('recommendations_population_relationship_populations', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('population_relationship', models.ForeignKey(orm['recommendations.population_relationship'], null=False)),
            ('population', models.ForeignKey(orm['recommendations.population'], null=False))
        ))
        db.create_unique('recommendations_population_relationship_populations', ['population_relationship_id', 'population_id'])

        # Removing M2M table for field populations on 'Recommendation'
        db.delete_table('recommendations_recommendation_populations')

        # Adding M2M table for field population_relations on 'Recommendation'
        db.create_table('recommendations_recommendation_population_relations', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('recommendation', models.ForeignKey(orm['recommendations.recommendation'], null=False)),
            ('population_relationship', models.ForeignKey(orm['recommendations.population_relationship'], null=False))
        ))
        db.create_unique('recommendations_recommendation_population_relations', ['recommendation_id', 'population_relationship_id'])


    def backwards(self, orm):
        # Deleting model 'Population_Relationship'
        db.delete_table('recommendations_population_relationship')

        # Removing M2M table for field populations on 'Population_Relationship'
        db.delete_table('recommendations_population_relationship_populations')

        # Adding M2M table for field populations on 'Recommendation'
        db.create_table('recommendations_recommendation_populations', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('recommendation', models.ForeignKey(orm['recommendations.recommendation'], null=False)),
            ('population', models.ForeignKey(orm['recommendations.population'], null=False))
        ))
        db.create_unique('recommendations_recommendation_populations', ['recommendation_id', 'population_id'])

        # Removing M2M table for field population_relations on 'Recommendation'
        db.delete_table('recommendations_recommendation_population_relations')


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
            'populations': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['recommendations.Population']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'recommendations.recommendation': {
            'Meta': {'object_name': 'Recommendation'},
            'add_populations': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'frequency': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_age': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'min_age': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'not_recommended': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'population_relations': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['recommendations.Population_Relationship']", 'symmetrical': 'False', 'blank': 'True'}),
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