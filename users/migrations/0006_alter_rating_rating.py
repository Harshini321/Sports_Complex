# Generated by Django 4.1 on 2022-09-02 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='rating',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Poor'), (2, 'Unsatisfactory'), (3, 'Satisfactory'), (4, 'Very Satisfactory'), (5, 'Outstanding')]),
        ),
    ]
