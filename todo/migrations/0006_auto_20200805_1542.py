# Generated by Django 3.0.7 on 2020-08-05 22:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0005_auto_20200805_1317'),
    ]

    operations = [
        migrations.RenameField(
            model_name='todo',
            old_name='operator',
            new_name='user',
        ),
    ]