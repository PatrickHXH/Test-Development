# Generated by Django 4.0.4 on 2022-07-17 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_alter_taskcaserelevance_case'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskcaserelevance',
            name='case_list',
            field=models.TextField(default='', null=True, verbose_name='用例列表'),
        ),
    ]