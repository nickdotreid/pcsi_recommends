# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Subject'
        db.create_table('notes_subject', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('notes', ['Subject'])

        # Deleting field 'Note.note_type'
        db.delete_column('notes_note', 'note_type')

        # Adding field 'Note.subject'
        db.add_column('notes_note', 'subject',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['notes.Subject']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Subject'
        db.delete_table('notes_subject')

        # Adding field 'Note.note_type'
        db.add_column('notes_note', 'note_type',
                      self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Note.subject'
        db.delete_column('notes_note', 'subject_id')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'notes.note': {
            'Meta': {'object_name': 'Note'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notes.Subject']"}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'weight': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'notes.subject': {
            'Meta': {'object_name': 'Subject'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
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
            'country': ('django_countries.fields.CountryField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inclusive': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'max_age': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'min_age': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'populations': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['populations.Population']", 'symmetrical': 'False', 'blank': 'True'})
        }
    }

    complete_apps = ['notes']