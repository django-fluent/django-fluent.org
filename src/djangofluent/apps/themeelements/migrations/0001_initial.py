# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import any_urlfield.models.fields
import fluent_contents.extensions.model_fields
import any_imagefield.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('fluent_contents', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Col12Item',
            fields=[
                ('contentitem_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='fluent_contents.ContentItem', on_delete=models.CASCADE)),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('icon', any_imagefield.models.fields.AnyImageField(max_length=100, verbose_name='Icon', blank=True)),
                ('body', fluent_contents.extensions.model_fields.PluginHtmlField(verbose_name='Body')),
            ],
            options={
                'db_table': 'contentitem_themeelements_col12item',
                'verbose_name': 'Column (1/2)',
                'verbose_name_plural': 'Columns (1/2)',
            },
            bases=('fluent_contents.contentitem',),
        ),
        migrations.CreateModel(
            name='ContentBoxItem',
            fields=[
                ('contentitem_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='fluent_contents.ContentItem', on_delete=models.CASCADE)),
            ],
            options={
                'db_table': 'contentitem_themeelements_contentboxitem',
                'verbose_name': 'Content box splitter',
                'verbose_name_plural': 'Content box splitters',
            },
            bases=('fluent_contents.contentitem',),
        ),
        migrations.CreateModel(
            name='ImageTextItem',
            fields=[
                ('contentitem_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='fluent_contents.ContentItem', on_delete=models.CASCADE)),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('image', any_imagefield.models.fields.AnyImageField(max_length=100, verbose_name='Image')),
                ('align', models.CharField(default=b'left', max_length=10, verbose_name='Align', choices=[(b'left', 'Left'), (b'right', 'Right')])),
                ('body', fluent_contents.extensions.model_fields.PluginHtmlField(verbose_name='Body')),
                ('url', any_urlfield.models.fields.AnyUrlField(max_length=300, verbose_name='URL', blank=True)),
                ('url_text', models.CharField(max_length=200, verbose_name='Text', blank=True)),
            ],
            options={
                'db_table': 'contentitem_themeelements_imagetextitem',
                'verbose_name': 'Image+text',
                'verbose_name_plural': 'Image+text items',
            },
            bases=('fluent_contents.contentitem',),
        ),
        migrations.CreateModel(
            name='PackageItem',
            fields=[
                ('contentitem_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='fluent_contents.ContentItem', on_delete=models.CASCADE)),
                ('slug', models.SlugField(verbose_name='Slug')),
                ('repository_url', models.URLField(verbose_name=b'Repository URL')),
                ('description', models.TextField(verbose_name='Description')),
                ('homepage', models.URLField(help_text='You only have to enter a homepage URL for external packages', verbose_name=b'Homepage', blank=True)),
                ('rtd_html_url', models.URLField(verbose_name='RTD URL', editable=False, blank=True)),
            ],
            options={
                'ordering': ('slug',),
                'db_table': 'contentitem_themeelements_packageitem',
                'verbose_name': 'Python Package item',
                'verbose_name_plural': 'Python Package items',
            },
            bases=('fluent_contents.contentitem',),
        ),
    ]
