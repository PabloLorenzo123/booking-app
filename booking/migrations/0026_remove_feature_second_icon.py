# Generated by Django 4.2.7 on 2023-12-02 18:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0025_feature_second_icon'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feature',
            name='second_icon',
        ),
    ]
