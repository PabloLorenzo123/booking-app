# Generated by Django 4.2.7 on 2023-12-02 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0023_rename_icona_feature_feature'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feature',
            name='feature',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='feature',
            name='icon',
            field=models.CharField(default='', max_length=100),
        ),
    ]
