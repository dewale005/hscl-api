# Generated by Django 3.1.6 on 2021-02-10 09:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('enrollee', '0008_auto_20210210_0914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enrollee',
            name='registeration_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]