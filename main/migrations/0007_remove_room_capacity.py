# Generated by Django 4.2.2 on 2023-06-12 06:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_ticket_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='capacity',
        ),
    ]
