# Generated by Django 4.1.7 on 2023-03-31 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_alter_schedule_start_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='CallAnalitics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('phones', models.IntegerField()),
                ('date', models.DateTimeField()),
                ('time', models.TimeField()),
                ('status', models.CharField(max_length=20)),
            ],
        ),
    ]