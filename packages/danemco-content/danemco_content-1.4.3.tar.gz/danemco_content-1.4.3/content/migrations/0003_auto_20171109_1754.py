# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0002_auto_20151208_1228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='template_name',
            field=models.CharField(help_text="Example: 'content/contact_page.html'. If this isn't provided, the system will use 'content/page.html'.", max_length=200, verbose_name='template name', blank=True),
        ),
    ]
