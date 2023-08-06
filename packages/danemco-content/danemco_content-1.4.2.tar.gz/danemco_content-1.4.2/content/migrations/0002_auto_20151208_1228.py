# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='enable_comments',
            field=models.BooleanField(default=False, verbose_name='enable comments'),
        ),
        migrations.AddField(
            model_name='page',
            name='registration_required',
            field=models.BooleanField(default=False, help_text='If this is checked, only logged-in users will be able to view the page.', verbose_name='registration required'),
        ),
    ]
