# Generated by Django 3.1.6 on 2021-02-10 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enrollee', '0006_auto_20210210_0912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enrollee',
            name='latitude',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='enrollee',
            name='longitude',
            field=models.FloatField(default=0),
        ),
    ]
