# Generated by Django 4.0.4 on 2022-06-19 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskcaserelevance',
            name='case',
            field=models.TextField(default='', null=True, verbose_name='关联用例'),
        ),
    ]
