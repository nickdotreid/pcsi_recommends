# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Population'
        db.create_table('populations_population', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('short', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=120)),
        ))
        db.send_create_signal('populations', ['Population'])

        # Adding model 'Population_Relationship'
        db.create_table('populations_population_relationship', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('inclusive', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('min_age', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('max_age', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('populations', ['Population_Relationship'])

        # Adding M2M table for field populations on 'Population_Relationship'
        db.create_table('populations_population_relationship_populations', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('population_relationship', models.ForeignKey(orm['populations.population_relationship'], null=False)),
            ('population', models.ForeignKey(orm['populations.population'], null=False))
        ))
        db.create_unique('populations_population_relationship_populations', ['population_relationship_id', 'population_id'])


    def backwards(self, orm):
        # Deleting model 'Population'
        db.delete_table('populations_population')

        # Deleting model 'Population_Relationship'
        db.delete_table('populations_population_relationship')

        # Removing M2M table for field populations on 'Population_Relationship'
        db.delete_table('populations_population_relationship_populations')


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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inclusive': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'max_age': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'min_age': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'populations': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['populations.Population']", 'symmetrical': 'False', 'blank': 'True'})
        }
    }

    complete_apps = ['populations']