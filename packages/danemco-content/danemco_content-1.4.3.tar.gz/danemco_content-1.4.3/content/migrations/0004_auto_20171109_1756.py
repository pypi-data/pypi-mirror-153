# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0003_auto_20171109_1754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snippet',
            name='url',
            field=models.CharField(default=b'/', max_length=200, verbose_name='URL', db_index=True, blank=True),
        ),
    ]
