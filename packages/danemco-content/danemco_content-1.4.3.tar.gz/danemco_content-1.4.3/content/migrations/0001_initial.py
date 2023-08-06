# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.CharField(help_text=b'Be sure to include slashes at the beginning and at the end', max_length=300, verbose_name='URL', db_index=True)),
                ('title', models.CharField(max_length=200, verbose_name='title')),
                ('content', models.TextField(verbose_name='content', blank=True)),
                ('template_name', models.CharField(help_text="Example: 'flatpages/contact_page.html'. If this isn't provided, the system will use 'flatpages/default.html'.", max_length=200, verbose_name='template name', blank=True)),
                ('keywords', models.TextField(blank=True)),
                ('description', models.TextField(blank=True)),
                ('sites', models.ManyToManyField(to='sites.Site')),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Snippet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.CharField(default=b'/', max_length=200, db_index=True, blank=True)),
                ('exact_url', models.BooleanField(default=False, help_text=b'Check to only match this url (no sub-urls).', db_index=True, verbose_name=b'Exact URL')),
                ('publish', models.DateTimeField(null=True, blank=True)),
                ('expire', models.DateTimeField(null=True, blank=True)),
                ('content', models.TextField(blank=True)),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='snippets', to='content.Section')),
            ],
        ),
    ]
