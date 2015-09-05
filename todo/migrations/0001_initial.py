# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=300, verbose_name='\u30bf\u30a4\u30c8\u30eb', blank=True)),
                ('task', models.TextField(null=True, verbose_name='\u5bfe\u5fdc\u5185\u5bb9', blank=True)),
                ('taskdetail', models.TextField(null=True, verbose_name='\u30bf\u30b9\u30af', blank=True)),
                ('priority', models.CharField(max_length=1, verbose_name='\u512a\u5148\u5ea6', choices=[('0', '\u6700\u9ad8'), ('1', '\u9ad8'), ('2', '\u4e2d'), ('3', '\u4f4e')])),
                ('status', models.CharField(max_length=1, verbose_name='STS', choices=[('0', '\u672a\u7740\u624b'), ('1', '\u5bfe\u5fdc\u4e2d(\u9806\u8abf)'), ('2', '\u5bfe\u5fdc\u4e2d(\u9045\u5ef6)'), ('3', '\u5b8c\u4e86\u5f85\u3061'), ('4', '\u5b8c\u4e86'), ('5', '\u4fdd\u7559'), ('6', '\u4e2d\u6b62')])),
                ('limitdate', models.DateField(null=True, verbose_name='\u2605\u671f\u9650', blank=True)),
                ('startdate', models.DateField(null=True, verbose_name='\u958b\u59cb\u65e5', blank=True)),
                ('finishdate', models.DateField(null=True, verbose_name='\u5b8c\u4e86\u65e5', blank=True)),
                ('memo', models.TextField(null=True, verbose_name='\u30e1\u30e2', blank=True)),
            ],
            options={
                'verbose_name': '\u30bf\u30b9\u30af',
                'verbose_name_plural': '\u30bf\u30b9\u30af\u4e00\u89a7',
            },
            bases=(models.Model,),
        ),
    ]
