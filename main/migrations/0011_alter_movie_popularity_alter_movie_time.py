# Generated by Django 4.2.2 on 2023-06-19 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_alter_movie_ticket_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='popularity',
            field=models.DecimalField(decimal_places=2, max_digits=6, null=0),
        ),
        migrations.AlterField(
            model_name='movie',
            name='time',
            field=models.TimeField(null=True),
        ),
    ]
