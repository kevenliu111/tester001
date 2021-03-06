# Generated by Django 2.0.6 on 2018-06-18 14:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='uploadlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to='uploadlist')),
                ('add_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='add_date')),
            ],
        ),
        migrations.CreateModel(
            name='user',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30, unique=True)),
                ('poststate', models.IntegerField(default=0)),
                ('creatstep', models.IntegerField(default=0)),
                ('errortimes', models.IntegerField(default=0)),
                ('lastsrc', models.CharField(max_length=50)),
                ('pwd', models.CharField(max_length=20)),
                ('profile', models.IntegerField(default=0)),
                ('emailverify', models.IntegerField(default=0)),
                ('phoneverify', models.IntegerField(default=0)),
                ('phonenum', models.CharField(max_length=20)),
                ('cookielogin', models.CharField(max_length=2000)),
            ],
        ),
    ]
