# Generated by Django 4.2.7 on 2023-12-02 00:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ReservationCart',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('check_in_date', models.DateField()),
                ('check_out_date', models.DateField()),
                ('user', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='cart', to=settings.AUTH_USER_MODEL, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('room_id', models.AutoField(primary_key=True, serialize=False)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('number', models.IntegerField()),
                ('building', models.IntegerField(default=1)),
                ('avaibility', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='RoomType',
            fields=[
                ('room_type_id', models.AutoField(primary_key=True, serialize=False)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('type', models.CharField(max_length=255, unique=True)),
                ('short_description', models.TextField(blank=True, null=True)),
                ('description', models.TextField()),
                ('max_adults', models.IntegerField(blank=True, null=True)),
                ('max_children', models.IntegerField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='RoomReserved',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('adults', models.IntegerField()),
                ('children', models.IntegerField()),
                ('total_price', models.IntegerField()),
                ('check_in_date', models.DateField(null=True)),
                ('check_out_date', models.DateField(null=True)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room_reserved', to='booking.reservationcart')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.room')),
            ],
        ),
        migrations.AddField(
            model_name='room',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room_type', to='booking.roomtype'),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('image', models.ImageField(blank=True, upload_to='rooms/')),
                ('alt', models.CharField(max_length=255)),
                ('room_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='booking.roomtype')),
            ],
        ),
    ]
