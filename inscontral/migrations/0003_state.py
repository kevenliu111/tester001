# Generated by Django 2.0.6 on 2018-06-19 14:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('inscontral', '0002_delete_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='state',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(max_length=10000)),
                ('add_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='add_date')),
            ],
        ),
    ]