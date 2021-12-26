# Generated by Django 4.0 on 2021-12-25 16:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0003_alter_reservation_room_alter_room_house'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservation.room'),
        ),
        migrations.AlterField(
            model_name='room',
            name='house',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservation.house'),
        ),
    ]