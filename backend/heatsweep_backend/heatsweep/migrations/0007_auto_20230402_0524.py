# Generated by Django 2.2.28 on 2023-04-02 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('heatsweep', '0006_auto_20230402_0328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tile',
            name='heat_value',
            field=models.CharField(default='#000000', max_length=7),
        ),
    ]
