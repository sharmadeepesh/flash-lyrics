# Generated by Django 3.0.2 on 2020-01-30 13:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20200130_1841'),
    ]

    operations = [
        migrations.RenameField(
            model_name='result',
            old_name='name_song',
            new_name='name',
        ),
    ]
