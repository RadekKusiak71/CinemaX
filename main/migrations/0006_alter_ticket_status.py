# Generated by Django 4.2.2 on 2023-06-12 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_ticket_ticket_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='status',
            field=models.CharField(choices=[('Student', 'Student'), ('Junior', 'Junior'), ('Senior', 'Senior'), ('Normal', 'Normal')], default='Normal', max_length=7),
        ),
    ]
