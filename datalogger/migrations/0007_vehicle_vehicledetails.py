# Generated by Django 3.2.2 on 2021-05-16 07:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('datalogger', '0006_auto_20210516_0616'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='vehicleDetails',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='datalogger.vehicledata'),
        ),
    ]
