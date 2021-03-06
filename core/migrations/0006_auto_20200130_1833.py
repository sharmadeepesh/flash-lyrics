# Generated by Django 3.0.2 on 2020-01-30 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20200129_1648'),
    ]

    operations = [
        migrations.CreateModel(
            name='search',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist', models.CharField(max_length=200)),
                ('image', models.URLField()),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AlterField(
            model_name='song',
            name='artist',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='song',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]
