# Generated by Django 4.1 on 2022-08-24 16:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courts', '0001_initial'),
        ('sports', '0005_booked_slot_booked_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='slot',
            name='court',
        ),
        migrations.RemoveField(
            model_name='slot',
            name='sport',
        ),
        migrations.AddField(
            model_name='slot',
            name='court',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='courts.court'),
        ),
        migrations.AddField(
            model_name='slot',
            name='sport',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='sports.sport'),
        ),
    ]