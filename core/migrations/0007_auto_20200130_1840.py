# Generated by Django 3.0.2 on 2020-01-30 13:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20200130_1833'),
    ]

    operations = [
        migrations.RenameField(
            model_name='search',
            old_name='name',
            new_name='name_song',
        ),
    ]
