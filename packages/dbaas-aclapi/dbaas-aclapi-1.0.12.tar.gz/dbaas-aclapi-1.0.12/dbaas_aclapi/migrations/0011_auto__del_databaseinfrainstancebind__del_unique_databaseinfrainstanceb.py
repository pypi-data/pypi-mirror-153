# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'DatabaseBind', fields ['database', 'bind_address']
        db.delete_unique(u'dbaas_aclapi_databasebind', ['database_id', 'bind_address'])

        # Removing unique constraint on 'AclApiJob', fields ['job_id', 'job_operation']
        db.delete_unique(u'dbaas_aclapi_aclapijob', ['job_id', 'job_operation'])

        # Removing unique constraint on 'DatabaseInfraInstanceBind', fields ['instance', 'instance_port', 'bind_address', 'databaseinfra']
        db.delete_unique(u'dbaas_aclapi_databaseinfrainstancebind', ['instance', 'instance_port', 'bind_address', 'databaseinfra_id'])

        # Deleting model 'DatabaseInfraInstanceBind'
        db.delete_table(u'dbaas_aclapi_databaseinfrainstancebind')

        # Deleting model 'AclApiJob'
        db.delete_table(u'dbaas_aclapi_aclapijob')

        # Deleting model 'DatabaseBind'
        db.delete_table(u'dbaas_aclapi_databasebind')


    def backwards(self, orm):
        # Adding model 'DatabaseInfraInstanceBind'
        db.create_table(u'dbaas_aclapi_databaseinfrainstancebind', (
            ('instance_port', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('instance', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39)),
            ('bind_address', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39)),
            ('bind_status', self.gf('django.db.models.fields.IntegerField')(default=2)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('databaseinfra', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'acl_binds', to=orm['physical.DatabaseInfra'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'dbaas_aclapi', ['DatabaseInfraInstanceBind'])

        # Adding unique constraint on 'DatabaseInfraInstanceBind', fields ['instance', 'instance_port', 'bind_address', 'databaseinfra']
        db.create_unique(u'dbaas_aclapi_databaseinfrainstancebind', ['instance', 'instance_port', 'bind_address', 'databaseinfra_id'])

        # Adding model 'AclApiJob'
        db.create_table(u'dbaas_aclapi_aclapijob', (
            ('environment', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'aclapi_jobs', to=orm['physical.Environment'])),
            ('job_status', self.gf('django.db.models.fields.PositiveSmallIntegerField')(db_index=True)),
            ('job_operation', self.gf('django.db.models.fields.PositiveSmallIntegerField')(db_index=True)),
            ('job_id', self.gf('django.db.models.fields.PositiveIntegerField')(unique=True)),
            ('database', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'acl_jobs', null=True, on_delete=models.SET_NULL, to=orm['logical.Database'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'dbaas_aclapi', ['AclApiJob'])

        # Adding unique constraint on 'AclApiJob', fields ['job_id', 'job_operation']
        db.create_unique(u'dbaas_aclapi_aclapijob', ['job_id', 'job_operation'])

        # Adding model 'DatabaseBind'
        db.create_table(u'dbaas_aclapi_databasebind', (
            ('bind_address', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39)),
            ('bind_status', self.gf('django.db.models.fields.IntegerField')(default=2)),
            ('database', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'acl_binds', null=True, on_delete=models.SET_NULL, to=orm['logical.Database'])),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('binds_requested', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'dbaas_aclapi', ['DatabaseBind'])

        # Adding unique constraint on 'DatabaseBind', fields ['database', 'bind_address']
        db.create_unique(u'dbaas_aclapi_databasebind', ['database_id', 'bind_address'])


    models = {
        
    }

    complete_apps = ['dbaas_aclapi']