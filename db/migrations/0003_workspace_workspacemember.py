# Generated by Django 5.0.4 on 2024-04-09 11:00

import db.models.workspace
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0002_verificationcode'),
    ]

    operations = [
        migrations.CreateModel(
            name='Workspace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, verbose_name='Workspace Name')),
                ('logo', models.URLField(blank=True, null=True, verbose_name='Logo')),
                ('slug', models.SlugField(max_length=48, unique=True)),
                ('organization_size', models.CharField(max_length=20)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner_workspace', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Workspace',
                'verbose_name_plural': 'Workspaces',
                'db_table': 'workspaces',
            },
        ),
        migrations.CreateModel(
            name='WorkspaceMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.PositiveSmallIntegerField(choices=[(20, 'Owner'), (15, 'Admin'), (10, 'Member'), (5, 'Guest')], default=10)),
                ('company_role', models.TextField(blank=True, null=True)),
                ('view_props', models.JSONField(default=db.models.workspace.get_default_props)),
                ('default_props', models.JSONField(default=db.models.workspace.get_default_props)),
                ('issue_props', models.JSONField(default=db.models.workspace.get_issue_props)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='member_workspace', to=settings.AUTH_USER_MODEL)),
                ('workspace', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workspace_member', to='db.workspace')),
            ],
            options={
                'verbose_name': 'Workspace Member',
                'verbose_name_plural': 'Workspace Members',
                'db_table': 'workspace_members',
                'unique_together': {('workspace', 'member')},
            },
        ),
    ]
