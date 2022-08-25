# Generated by Django 4.1 on 2022-08-25 11:22

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courts', '0001_initial'),
        ('users', '0004_admin_slots_staff_slots'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)])),
                ('court', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courts.court')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.member')),
            ],
        ),
    ]