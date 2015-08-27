# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('body', models.TextField(null=True, blank=True)),
                ('image', models.URLField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('color', models.CharField(default=b'#f3f3f3', max_length=50, blank=True)),
                ('order', models.IntegerField(default=0)),
                ('image', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='ContentSource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('link', models.URLField(max_length=255)),
                ('logo', models.CharField(max_length=255, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='RSSArticle',
            fields=[
                ('article_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='content.Article')),
                ('publication_date', models.DateTimeField()),
                ('identifier', models.URLField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
            bases=('content.article',),
        ),
        migrations.CreateModel(
            name='RSSCategory',
            fields=[
                ('category_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='content.Category')),
                ('feed', models.URLField()),
                ('last_update', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('content.category',),
        ),
        migrations.CreateModel(
            name='WikiArticle',
            fields=[
                ('article_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='content.Article')),
                ('identifier', models.CharField(max_length=255)),
                ('identifier_type', models.CharField(default=b'title', max_length=6, blank=True, choices=[(b'pageid', b'pageid'), (b'title', b'title')])),
            ],
            options={
                'abstract': False,
            },
            bases=('content.article',),
        ),
        migrations.CreateModel(
            name='WikiCategory',
            fields=[
                ('category_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='content.Category')),
                ('identifier', models.CharField(max_length=255)),
                ('identifier_type', models.CharField(default=b'title', max_length=6, blank=True, choices=[(b'pageid', b'pageid'), (b'title', b'title')])),
                ('wiki_type', models.CharField(default=b'14', max_length=3, choices=[(b'0', b'Page'), (b'14', b'Category'), (b'100', b'Portal')])),
            ],
            options={
                'verbose_name_plural': 'WikiCategories',
            },
            bases=('content.category',),
        ),
        migrations.AddField(
            model_name='category',
            name='parent',
            field=models.ForeignKey(related_name='children', blank=True, to='content.Category', null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='polymorphic_ctype',
            field=models.ForeignKey(related_name='polymorphic_content.category_set+', editable=False, to='contenttypes.ContentType', null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='source',
            field=models.ForeignKey(blank=True, to='content.ContentSource', null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='categories',
            field=models.ManyToManyField(related_name='articles', to='content.Category'),
        ),
        migrations.AddField(
            model_name='article',
            name='polymorphic_ctype',
            field=models.ForeignKey(related_name='polymorphic_content.article_set+', editable=False, to='contenttypes.ContentType', null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='source',
            field=models.ForeignKey(blank=True, to='content.ContentSource', null=True),
        ),
        migrations.CreateModel(
            name='KidsWeekCategory',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('content.rsscategory',),
        ),
        migrations.CreateModel(
            name='SevenDaysCategory',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('content.rsscategory',),
        ),
    ]
