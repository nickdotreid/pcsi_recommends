# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'RegionCollection'
        db.create_table('populations_regioncollection', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('exclude', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('populations', ['RegionCollection'])

        # Adding M2M table for field regions on 'RegionCollection'
        db.create_table('populations_regioncollection_regions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('regioncollection', models.ForeignKey(orm['populations.regioncollection'], null=False)),
            ('region', models.ForeignKey(orm['populations.region'], null=False))
        ))
        db.create_unique('populations_regioncollection_regions', ['regioncollection_id', 'region_id'])

        # Adding model 'Region'
        db.create_table('populations_region', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('country', self.gf('django_countries.fields.CountryField')(max_length=2, null=True, blank=True)),
        ))
        db.send_create_signal('populations', ['Region'])

        # Deleting field 'Population_Relationship.country'
        db.delete_column('populations_population_relationship', 'country')

        # Adding M2M table for field regions on 'Population_Relationship'
        db.create_table('populations_population_relationship_regions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('population_relationship', models.ForeignKey(orm['populations.population_relationship'], null=False)),
            ('regioncollection', models.ForeignKey(orm['populations.regioncollection'], null=False))
        ))
        db.create_unique('populations_population_relationship_regions', ['population_relationship_id', 'regioncollection_id'])


    def backwards(self, orm):
        # Deleting model 'RegionCollection'
        db.delete_table('populations_regioncollection')

        # Removing M2M table for field regions on 'RegionCollection'
        db.delete_table('populations_regioncollection_regions')

        # Deleting model 'Region'
        db.delete_table('populations_region')

        # Adding field 'Population_Relationship.country'
        db.add_column('populations_population_relationship', 'country',
                      self.gf('django_countries.fields.CountryField')(max_length=2, null=True, blank=True),
                      keep_default=False)

        # Removing M2M table for field regions on 'Population_Relationship'
        db.delete_table('populations_population_relationship_regions')


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
            'min_age': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'populations': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['populations.Population']", 'symmetrical': 'False', 'blank': 'True'}),
            'regions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['populations.RegionCollection']", 'symmetrical': 'False'})
        },
        'populations.region': {
            'Meta': {'object_name': 'Region'},
            'country': ('django_countries.fields.CountryField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'populations.regioncollection': {
            'Meta': {'object_name': 'RegionCollection'},
            'exclude': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'regions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['populations.Region']", 'symmetrical': 'False'})
        }
    }

    complete_apps = ['populations']