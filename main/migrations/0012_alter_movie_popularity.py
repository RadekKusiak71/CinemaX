# Generated by Django 4.2.2 on 2023-06-19 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_alter_movie_popularity_alter_movie_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='popularity',
            field=models.DecimalField(decimal_places=2, max_digits=6, null=True),
        ),
    ]
