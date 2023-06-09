# Generated by Django 4.1.7 on 2023-03-30 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_rename_contact_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('number_calls', models.IntegerField()),
                ('retry_count', models.IntegerField()),
                ('repeated_time', models.IntegerField()),
            ],
        ),
    ]
