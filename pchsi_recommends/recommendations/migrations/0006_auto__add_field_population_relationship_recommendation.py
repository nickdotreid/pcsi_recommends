# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing M2M table for field population_relations on 'Recommendation'
        db.delete_table('recommendations_recommendation_population_relations')

        # Adding field 'Population_Relationship.recommendation'
        db.add_column('recommendations_population_relationship', 'recommendation',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['recommendations.Recommendation']),
                      keep_default=False)


    def backwards(self, orm):
        # Adding M2M table for field population_relations on 'Recommendation'
        db.create_table('recommendations_recommendation_population_relations', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('recommendation', models.ForeignKey(orm['recommendations.recommendation'], null=False)),
            ('population_relationship', models.ForeignKey(orm['recommendations.population_relationship'], null=False))
        ))
        db.create_unique('recommendations_recommendation_population_relations', ['recommendation_id', 'population_relationship_id'])

        # Deleting field 'Population_Relationship.recommendation'
        db.delete_column('recommendations_population_relationship', 'recommendation_id')


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
            'populations': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['recommendations.Population']", 'symmetrical': 'False', 'blank': 'True'}),
            'recommendation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['recommendations.Recommendation']"})
        },
        'recommendations.recommendation': {
            'Meta': {'object_name': 'Recommendation'},
            'frequency': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_age': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'min_age': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
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