# Generated by Django 4.2.7 on 2023-12-02 20:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0027_remove_roomfeature_feature_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature', models.CharField(max_length=100)),
                ('icon', models.CharField(default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='RoomFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room_types', to='booking.feature')),
                ('room_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='features', to='booking.roomtype')),
            ],
        ),
    ]
